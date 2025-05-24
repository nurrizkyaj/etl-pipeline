import pandas as pd
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

EXCHANGE_RATE = 16000
REQUIRED_COLUMNS = {"Title", "Price", "Rating", "Colors"}

def check_data_validity(data):
    if not data:
        logger.warning("No data is available for transformation.")
        return False

    try:
        df = pd.DataFrame(data)
        missing_cols = REQUIRED_COLUMNS - set(df.columns)
        
        if missing_cols:
            logger.warning(f"There are missing columns: {missing_cols}")
            return False
        
        return True

    except Exception as e:
        logger.error(f"An error occurred in data validation: {e}")
        return False

def transform_data(data, exchange_rate=EXCHANGE_RATE):
    if not check_data_validity(data):
        return pd.DataFrame()

    try:
        
        df = pd.DataFrame(data)
        df["Price"] = (
            pd.to_numeric(df["Price"], errors="coerce")
            .mul(exchange_rate)
            .round(2)
        )

        df["Rating"] = df["Rating"].astype(str).str.extract(r"([\d.]+)").astype(float)
        df.dropna(subset=["Rating"], inplace=True)

        df["Colors"] = pd.to_numeric(df["Colors"], errors="coerce").fillna(0).astype(int)

        df.drop_duplicates(inplace=True)
        df.dropna(inplace=True)

        df = df[df["Title"] != "Unknown Product"]

        logger.info(f"Data transformation completed. Total data that was successfully processed: {len(df)}")
        return df

    except Exception as e:
        logger.error(f"Errors when performing data transformation: {e}")
        return pd.DataFrame()
