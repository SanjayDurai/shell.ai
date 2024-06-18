from src.data_loader import load_data
from src.data_preprocessing import preprocess_data
from src.submission import generate_submission
from src.optimization import optimize_fleet

def main():
    data = load_data()
    data, master_data = preprocess_data(data)
    results_df = optimize_fleet(data, master_data)
    generate_submission(results_df)

if __name__ == "__main__":
    main()
