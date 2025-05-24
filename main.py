import logging
import pandas as pd
from utils.extract_data.extract import scrape_main
from utils.transform_data.transform import transform_data
from utils.load_data.load_csv import load_csv
from utils.load_data.load_postgre import load_to_postgres
from utils.load_data.load_sheet import load_to_sheets

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def main(max_attempts=3):
    for attempt in range(max_attempts):
        try:
            print("\n----------------------------------------------------------------------------------------------------")
            print("Starting the ETL pipeline process")
            print("----------------------------------------------------------------------------------------------------\n")

            print("----------------------------------------------------------------------------------------------------")
            print("Running the Extract process")
            print("----------------------------------------------------------------------------------------------------")
            raw_data = scrape_main()
            if not raw_data:
                raise ValueError("The extract process failed: Data not found")

            print("----------------------------------------------------------------------------------------------------")
            print("Running the Transform process")
            print("----------------------------------------------------------------------------------------------------")
            transformed_df = transform_data(raw_data)
            if transformed_df.empty:
                raise ValueError("The transform process failed: Empty transformed data")

            print("----------------------------------------------------------------------------------------------------")
            print("Run the Load process")
            print("----------------------------------------------------------------------------------------------------")
            load_csv(transformed_df, "fashion_studio.csv")
            load_to_postgres(transformed_df)
            load_to_sheets(transformed_df)

            print(f"\nThe amount of data after the ETL process: {len(transformed_df)}")
            print("\n----------------------------------------------------------------------------------------------------")
            print("ETL pipeline process completed")
            print("----------------------------------------------------------------------------------------------------\n")
            
            return transformed_df

        except ValueError as ve:
            logging.error(f"An error occurred in the ETL process (Trial {attempt + 1}): {ve}\n")
            if attempt == max_attempts - 1:
                logging.error("ETL process failed\n")
                return pd.DataFrame()

if __name__ == "__main__":
    main()