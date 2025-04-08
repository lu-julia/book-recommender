"""
This module loads data from an object storage system (S3) and processes it into DataFrames.
"""

import os
import s3fs
from dotenv import load_dotenv
import pandas as pd


load_dotenv()
fs = s3fs.S3FileSystem(
    client_kwargs={"endpoint_url": "https://" + os.environ["AWS_S3_ENDPOINT"]},
    key=os.environ["AWS_ACCESS_KEY_ID"],
    secret=os.environ["AWS_SECRET_ACCESS_KEY"],
    token=os.environ["AWS_SESSION_TOKEN"])


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
    books = books.drop(columns=["Image-URL-S", "Image-URL-M"])
    books.rename(columns={"Book-Title": "title",
                          "Book-Author": "author",
                          "Year-Of-Publication": 'year',
                          "Publisher": "publisher",
                          "Image-URL-L": "image_url"}, inplace=True)
    return books


def load_rating_data() -> pd.DataFrame:
    """
    Reads rating data from S3 and returns it as a DataFrame.
    """
    ratings = read_csv_from_s3("Ratings.csv")
    return ratings


def load_user_data() -> pd.DataFrame:
    """
    Reads user data from S3 and returns it as a DataFrame.
    """
    users = read_csv_from_s3("Users.csv")
    return users


def load_books_with_ratings() -> pd.DataFrame:
    """
    Loads books and ratings, merges them, and returns a DataFrame with book statistics.
    """
    books = load_book_data()
    ratings = load_rating_data()
    ratings = ratings[ratings["Book-Rating"] != 0]
    book_stats = ratings.groupby('ISBN').agg({
        'Book-Rating': ['count', 'mean']
    }).reset_index()
    book_stats.columns = ['ISBN', 'num_ratings', 'avg_rating']
    df = pd.merge(books, book_stats, on='ISBN', how="left").fillna(value={"num_ratings": 0,
                                                                          "avg_rating": 0})
    return df
