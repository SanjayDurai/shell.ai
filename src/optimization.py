import pandas as pd
from pulp import LpProblem, LpMinimize, LpVariable, lpSum

def optimize_fleet(data, master_data):
    # Extract necessary data
    carbon_emissions = data['carbon_emissions']
    cost_profiles = data['cost_profiles']
    demand = data['demand']
    fuels = data['fuels']
    vehicles = data['vehicles']
    vehicles_fuels = data['vehicles_fuels']

    # Initialize the problem
    prob = LpProblem("Fleet_Optimization", LpMinimize)

    # Define decision variables
    # Variables for number of vehicles to buy, use, and sell each year
    years = sorted(demand['Year'].dt.year.unique())
    vehicle_ids = vehicles['ID'].unique()
    decisions = {}
    for year in years:
        for vid in vehicle_ids:
            decisions[(year, vid, 'buy')] = LpVariable(f"buy_{year}_{vid}", 0, None, cat='Integer')
            decisions[(year, vid, 'use')] = LpVariable(f"use_{year}_{vid}", 0, None, cat='Integer')
            decisions[(year, vid, 'sell')] = LpVariable(f"sell_{year}_{vid}", 0, None, cat='Integer')

    # Define the objective function (minimize total cost)
    total_cost = lpSum([
        # Purchase cost
        vehicles[vehicles['ID'] == vid]['Cost ($)'].values[0] * decisions[(year, vid, 'buy')]
        for year in years for vid in vehicle_ids
    ])

    # Add operational costs (fuel, maintenance, insurance)
    for year in years:
        for vid in vehicle_ids:
            vehicle = vehicles[vehicles['ID'] == vid].iloc[0]
            fuel_type = vehicles_fuels[vehicles_fuels['ID'] == vid]['Fuel'].values[0]
            fuel_cost = fuels[(fuels['Fuel'] == fuel_type) & (fuels['Year'].dt.year == year)]['Cost ($/unit_fuel)'].values[0]
            fuel_consumption = vehicles_fuels[vehicles_fuels['ID'] == vid]['Consumption (unit_fuel/km)'].values[0]
            yearly_range = vehicle['Yearly range (km)']
            maintenance_cost = cost_profiles[cost_profiles['End of Year'] == year]['Maintenance Cost %'].values[0] / 100
            insurance_cost = cost_profiles[cost_profiles['End of Year'] == year]['Insurance Cost %'].values[0] / 100

            total_cost += (
                fuel_cost * fuel_consumption * yearly_range * decisions[(year, vid, 'use')] +
                maintenance_cost * vehicle['Cost ($)'] * decisions[(year, vid, 'use')] +
                insurance_cost * vehicle['Cost ($)'] * decisions[(year, vid, 'use')]
            )

    prob += total_cost

    # Add constraints
    # Satisfy demand
    for year in years:
        for size in demand['Size'].unique():
            for dist_bucket in demand['Distance'].unique():
                demand_year = demand[(demand['Year'].dt.year == year) & (demand['Size'] == size) & (demand['Distance'] == dist_bucket)]['Demand (km)'].values[0]
                prob += lpSum([
                    decisions[(year, vid, 'use')] * vehicles[vehicles['ID'] == vid]['Yearly range (km)'].values[0]
                    for vid in vehicle_ids if vehicles[vehicles['ID'] == vid]['Vehicle Size'].values[0] == size
                ]) >= demand_year

    # Carbon emission constraints
    for year in years:
        carbon_limit = carbon_emissions[carbon_emissions['Year'].dt.year == year]['Carbon emission CO2/kg'].values[0]
        prob += lpSum([
            decisions[(year, vid, 'use')] * vehicles_fuels[vehicles_fuels['ID'] == vid]['Consumption (unit_fuel/km)'].values[0] *
            fuels[(fuels['Fuel'] == vehicles_fuels[vehicles_fuels['ID'] == vid]['Fuel'].values[0]) & (fuels['Year'].dt.year == year)]['Emissions (CO2/unit_fuel)'].values[0] *
            vehicles[vehicles['ID'] == vid]['Yearly range (km)'].values[0]
            for vid in vehicle_ids
        ]) <= carbon_limit

    # Vehicle lifecycle constraints (10 years)
    for vid in vehicle_ids:
        for year in years:
            purchase_year = int(vid.split('_')[-1])
            if year > purchase_year + 10:
                prob += decisions[(year, vid, 'use')] == 0

    # Solve the problem
    prob.solve()

    # Extract the results
    results = []
    for year in years:
        for vid in vehicle_ids:
            for action in ['buy', 'use', 'sell']:
                var = decisions[(year, vid, action)]
                if var.varValue > 0:
                    results.append({
                        'Year': year,
                        'ID': vid,
                        'Num_Vehicles': var.varValue,
                        'Type': action.capitalize(),
                        'Fuel': vehicles_fuels[vehicles_fuels['ID'] == vid]['Fuel'].values[0],
                        'Distance_bucket': vehicles[vehicles['ID'] == vid]['Distance_bucket'].values[0],
                        'Distance_per_vehicle(km)': vehicles[vehicles['ID'] == vid]['Yearly range (km)'].values[0]
                    })

    results_df = pd.DataFrame(results)
    return results_df
