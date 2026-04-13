import sys

from src.config import RAW_DIR, DATASET_NAME, logger
from src.download import download_dataset
from src.load_raw_db import load_raw_db


def run_pipeline():
    try:
        logger.info("\n[Step 1] Downloading raw data...")
        download_dataset(DATASET_NAME, RAW_DIR)

        logger.info("\n Loading raw data into postgresql")
        load_raw_db()

        logger.info("\nIngestion pipeline completed successfully.")
    except Exception as e:
        logger.info(f"\n Pipeline error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    run_pipeline()