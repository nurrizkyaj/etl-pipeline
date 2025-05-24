import pandas as pd
import logging
from googleapiclient.discovery import build
from google.oauth2 import service_account

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

SPREADSHEET_ID = "1AAvV5eZPc8Ond7ehDJnDjkwNnnQ_Km51ClWP97pcwqM"
SHEET_NAME = "Sheet1"

def authenticate_google_sheets() -> object:
    try:
        creds = service_account.Credentials.from_service_account_file(
            "google-sheets-api.json",
            scopes=["https://www.googleapis.com/auth/spreadsheets"]
        )
        service = build("sheets", "v4", credentials=creds)
        logger.info("Successfully authenticate to the Google Sheets API.")
        return service
    except Exception as e:
        logger.error(f"Error during authentication: {e}")
        raise

def prepare_data_for_upload(df: pd.DataFrame) -> list:
    return [df.columns.tolist()] + df.values.tolist()

def load_to_sheets(df: pd.DataFrame) -> dict:
    if df.empty:
        logger.warning("There is no data to upload to Google Sheets.")
        return None

    try:
        service = authenticate_google_sheets()

        values = prepare_data_for_upload(df)

        request = service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=SHEET_NAME,
            valueInputOption="RAW",
            body={"values": values}
        )

        response = request.execute()

        logger.info("The data was successfully uploaded to Google Sheets.")
        return response

    except Exception as e:
        logger.error(f"An error occurred while uploading to Google Sheets: {e}")
        return None