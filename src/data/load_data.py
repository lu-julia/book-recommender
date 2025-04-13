"""
This module loads data from an object storage system (S3) and processes it into DataFrames.
"""

import os
import s3fs
from dotenv import load_dotenv
import pandas as pd

from src.data.preprocessing import (
    process_books,
    process_ratings,
    filter_ratings,
    merge_books_ratings,
)


# Load environment variables from .env file
load_dotenv()
# Initialize S3 file system
fs = s3fs.S3FileSystem(
    client_kwargs={"endpoint_url": "https://minio.lab.sspcloud.fr"},
    key=os.environ["AWS_ACCESS_KEY_ID"],
    secret=os.environ["AWS_SECRET_ACCESS_KEY"],
    token=os.environ["AWS_SESSION_TOKEN"]
)


def read_csv_from_s3(file_name: str, **kwargs) -> pd.DataFrame:
    """
    Reads a CSV file from an object storage system.
    """
    with fs.open(f"s3://julialu/diffusion/{file_name}", mode="rb") as file_in:
        df = pd.read_csv(file_in, sep=",", **kwargs)
    return df


def load_book_data() -> pd.DataFrame:
    """
    Reads book data from S3 and returns the processed DataFrame.
    """
    books = read_csv_from_s3("Books.csv", dtype={"Year-Of-Publication": str})
    books = process_books(books)
    return books


def load_rating_data(filtered: bool = True) -> pd.DataFrame:
    """
    Reads rating data from S3 and returns the processed DataFrame.
    """
    ratings = read_csv_from_s3("Ratings.csv")
    ratings = process_ratings(ratings)
    if filtered:
        ratings = filter_ratings(ratings)
    return ratings


def load_books_ratings() -> pd.DataFrame:
    """
    Loads books and ratings, merges them, and returns a DataFrame with book statistics.
    """
    books = load_book_data()
    ratings = load_rating_data()
    books_ratings = merge_books_ratings(books, ratings)
    return books_ratings
