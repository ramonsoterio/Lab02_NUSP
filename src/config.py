import os
from pathlib import Path
from dotenv import load_dotenv
import logging

BASE_DIR = Path(__file__).parent.parent
env_path = BASE_DIR / ".env"

load_dotenv(dotenv_path=env_path)

if not os.environ["KAGGLE_USERNAME"] or not os.environ["KAGGLE_KEY"]:
    raise ValueError("ERROR: Kaggle credentials not found in the environment.")

RAW_DIR = BASE_DIR / "data" / "raw"
SILVER_DIR = BASE_DIR / "data" / "silver"
STATS_DIR = SILVER_DIR / "stats"
ASSETS_DIR = BASE_DIR / "assets"

DATASET_NAME = "olistbr/brazilian-ecommerce"

TABLE_MAP = {
    "olist_orders_dataset": "orders",
    "olist_order_items_dataset": "order_items",
    "olist_products_dataset": "products",
    "olist_customers_dataset": "customers",
    "olist_sellers_dataset": "sellers",
    "olist_order_payments_dataset": "order_payments",
    "olist_order_reviews_dataset": "order_reviews",
    "olist_geolocation_dataset": "geolocation",
    "product_category_name_translation": "category_translation"
}

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DB_URL = os.getenv('DB_URL', 'postgresql://admin:admin@localhost:5432/olist_db')