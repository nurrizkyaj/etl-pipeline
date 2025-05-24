import logging
import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def load_csv(df, filename="products.csv"):
    if df.empty:
        logging.warning("There is no data to save.")
        return
    
    try:
        df.to_csv(filename, index=False, encoding='utf-8')
        logging.info(f"Data successfully saved in {filename}")

    except Exception as e:
        logging.error(f"An error occurred while saving the data: {e}")
        raise
