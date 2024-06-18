import pandas as pd

def preprocess_data(data):
    # Parse dates
    data['carbon_emissions']['Year'] = pd.to_datetime(data['carbon_emissions']['Year'], format='%Y')
    data['demand']['Year'] = pd.to_datetime(data['demand']['Year'], format='%Y')
    data['fuels']['Year'] = pd.to_datetime(data['fuels']['Year'], format='%Y')
    data['vehicles']['Year'] = pd.to_datetime(data['vehicles']['Year'], format='%Y')
    
    # Merge vehicles and fuels data
    vehicles_fuels_merged = pd.merge(data['vehicles_fuels'], data['vehicles'], on='ID')
    data['vehicles_fuels_merged'] = vehicles_fuels_merged
    
    # Merge all datasets to create a master dataset
    master_data = pd.merge(vehicles_fuels_merged, data['fuels'], how='left', left_on=['Fuel'], right_on=['Fuel'])
    master_data = pd.merge(master_data, data['demand'], how='left', left_on=['Year', 'Vehicle Size'], right_on=['Year', 'Size'])
    master_data = pd.merge(master_data, data['cost_profiles'], how='left', left_on='Year', right_on='End of Year')
    
    # Fill missing values
    master_data.fillna(0, inplace=True)
    
    return data, master_data
