"""
This module loads data from an object storage system (S3) and processes it into DataFrames.
"""

import os
import time

import s3fs
from dotenv import load_dotenv
import pandas as pd

from src.app_utils.logger import logger
from src.data.preprocessing import (
    process_books,
    process_ratings,
    filter_ratings,
)


# Load environment variables from .env file
load_dotenv()

# Initialize S3 file system
fs = s3fs.S3FileSystem(
    client_kwargs={"endpoint_url": "https://minio.lab.sspcloud.fr"},
    key=os.environ["AWS_ACCESS_KEY_ID"],
    secret=os.environ["AWS_SECRET_ACCESS_KEY"],
    token=os.environ["AWS_SESSION_TOKEN"],
)


def read_csv_from_s3(file_name: str, **kwargs) -> pd.DataFrame:
    """
    Reads a CSV file from an object storage system.
    """
    logger.info(f"Reading file from S3: {file_name}")
    try:
        with fs.open(f"s3://julialu/diffusion/{file_name}", mode="rb") as file_in:
            df = pd.read_csv(file_in, sep=",", **kwargs)
        logger.success(f"Successfully read {file_name}")
        return df
    except Exception as e:
        logger.error(f"Error reading {file_name}: {e}")
        raise


def load_book_data() -> pd.DataFrame:
    """
    Reads book data from S3 and returns the processed DataFrame.
    """
    start_time = time.time()
    logger.info("Loading book data...")
    books = read_csv_from_s3("Books.csv", dtype={"Year-Of-Publication": str})
    books = process_books(books)
    elapsed = time.time() - start_time
    logger.success(f"Book dataset loaded and processed in {elapsed:.2f} seconds.")
    return books


def load_rating_data(filtered: bool = True) -> pd.DataFrame:
    """
    Reads rating data from S3 and returns the processed DataFrame.
    """
    start_time = time.time()
    logger.info("Loading rating data...")
    ratings = read_csv_from_s3("Ratings.csv")
    ratings = process_ratings(ratings)
    if filtered:
        ratings = filter_ratings(ratings)
    elapsed = time.time() - start_time
    logger.success(f"Rating data loaded and processed in {elapsed:.2f} seconds.")
    return ratings
