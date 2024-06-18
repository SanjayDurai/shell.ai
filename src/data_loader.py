import pandas as pd

def load_data():
    # Load datasets
    carbon_emissions = pd.read_csv('../data/carbon_emissions.csv')
    cost_profiles = pd.read_csv('../data/cost_profiles.csv')
    demand = pd.read_csv('../data/demand.csv')
    fuels = pd.read_csv('../data/fuels.csv')
    sample_submission = pd.read_csv('../data/sample_submission.csv')
    vehicles = pd.read_csv('../data/vehicles.csv')
    vehicles_fuels = pd.read_csv('../data/vehicles_fuels.csv')
    
    return {
        'carbon_emissions': carbon_emissions,
        'cost_profiles': cost_profiles,
        'demand': demand,
        'fuels': fuels,
        'sample_submission': sample_submission,
        'vehicles': vehicles,
        'vehicles_fuels': vehicles_fuels
    }
