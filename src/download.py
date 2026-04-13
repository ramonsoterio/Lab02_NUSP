import kagglehub
import os
import shutil
from pathlib import Path

from src.config import logger

def download_dataset(kaggle_dataset_id: str, destination: str):
    base_path = Path(__file__).parent if "__file__" in locals() else Path.cwd()
    raw_dir = base_path / destination

    raw_dir.mkdir(parents=True, exist_ok=True)

    logger.info(f"Target: {raw_dir}")

    try:
        cache_path = kagglehub.dataset_download(kaggle_dataset_id)
        logger.info(f"Content downloaded to cache: {cache_path}")
        files = os.listdir(cache_path)

        for file_name in files:
            source = os.path.join(cache_path, file_name)
            file = raw_dir / file_name
            shutil.copy(source, file)
            logger.info(f"File copied: {file_name}")

        logger.info(f"\nSuccess! All files generated in: {raw_dir}")

    except Exception as e:
        logger.error(f"Download error: {e}")
