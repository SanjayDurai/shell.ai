def generate_submission(master_data, file_path='submission.csv'):
    submission = master_data[['Year', 'ID', 'Num_Vehicles', 'Type', 'Fuel', 'Distance_bucket', 'Distance_per_vehicle(km)']]
    submission.to_csv(file_path, index=False)
    print("Submission file generated successfully.")
