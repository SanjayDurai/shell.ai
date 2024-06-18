# Carbon Emissions Project

This project analyzes carbon emissions data along with associated cost profiles, demand, and vehicle information.

## Setup

1. Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

2. Install dependencies:
    ```bash
    pip install pandas numpy matplotlib jupyter
    ```

3. Run the main script:
    ```bash
    python src/main.py
    ```

## Project Structure

carbon_emissions_project/
├── data/
│ ├── carbon_emissions.csv
│ ├── cost_profiles.csv
│ ├── demand.csv
│ ├── fuels.csv
│ ├── sample_submission.csv
│ ├── vehicles.csv
│ └── vehicles_fuels.csv
├── notebooks/
│ └── data_analysis.ipynb
├── src/
│ ├── init.py
│ ├── data_loader.py
│ ├── data_preprocessing.py
│ ├── optimization.py
│ └── submission.py
└── README.md