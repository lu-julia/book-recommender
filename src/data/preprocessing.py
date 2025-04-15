"""
Preprocessing functions for cleaning the books and ratings datasets.
"""

import re
import pandas as pd
import numpy as np


def remove_punctuation(text: str) -> str:
    """
    Function to remove specific punctuation from a string.
    """
    # Removes ", . and \
    return re.sub(r"[\".\\]", "", text)


def process_books(books: pd.DataFrame) -> pd.DataFrame:
    """
    Function to process the books DataFrame.
    """
    books = books.drop(columns=["Image-URL-S", "Image-URL-M"])
    # Rename columns
    books.rename(
        columns={
            "Book-Title": "title",
            "Book-Author": "author",
            "Year-Of-Publication": "year",
            "Publisher": "publisher",
            "Image-URL-L": "image_url",
        },
        inplace=True,
    )
    # Clean year
    books["year"] = pd.to_numeric(books["year"], errors="coerce")
    books.loc[(books["year"] < 1000) | (books["year"] > 2010)] = np.nan
    # Drop nan values
    books = books.dropna().reset_index(drop=True)
    # Convert year to string
    books["year"] = books["year"].astype(int).astype(str)
    # Remove punctuation and standardize casing
    books["title"] = books["title"].apply(remove_punctuation).str.strip().str.title()
    books["author"] = books["author"].apply(remove_punctuation).str.strip().str.title()
    books["publisher"] = books["publisher"].fillna("").str.strip().str.title()
    return books.reset_index(drop=True)


def process_ratings(ratings: pd.DataFrame) -> pd.DataFrame:
    """
    Function to process the ratings DataFrame.
    """
    ratings.rename(
        columns={"User-ID": "user_id", "Book-Rating": "rating"}, inplace=True
    )
    ratings = ratings[ratings["rating"] != 0]
    return ratings


def filter_ratings(
    ratings: pd.DataFrame, min_users: int = 20, min_books: int = 5
) -> pd.DataFrame:
    """
    Filter the ratings DataFrame to include only:
    - the users who have rated at least 'min_users' books
    - the books with at least 'min_books' ratings

    Args :
        ratings (pd.DataFrame) : DataFrame with columns 'user_id', 'ISBN', and 'rating'.
        min_users (int) : minimal number of ratings for a user.
        min_books (int) : minimal number of ratings for a book.

    Returns :
        pd.DataFrame : Filtered DataFrame
    """
    # Keep only active users
    user_counts = ratings["user_id"].value_counts()
    users_to_keep = user_counts[user_counts >= min_users].index
    ratings = ratings[ratings["user_id"].isin(users_to_keep)]
    # Keep only books with enough ratings
    book_counts = ratings["ISBN"].value_counts()
    books_to_keep = book_counts[book_counts >= min_books].index
    ratings = ratings[ratings["ISBN"].isin(books_to_keep)]
    return ratings.reset_index(drop=True)


def merge_books_ratings(books: pd.DataFrame, ratings: pd.DataFrame) -> pd.DataFrame:
    """
    Function to merge the books and ratings DataFrames and add book statistics columns.
    """
    book_stats = (
        ratings.groupby("ISBN").agg({"rating": ["count", "mean"]}).reset_index()
    )
    book_stats.columns = ["ISBN", "num_ratings", "avg_rating"]
    books_ratings = pd.merge(books, book_stats, on="ISBN", how="inner")
    books_ratings["num_ratings"] = books_ratings["num_ratings"].astype(int)
    books_ratings = books_ratings.round({"avg_rating": 2})
    # Drop duplicate books with the same title and author
    books_ratings = books_ratings.sort_values("num_ratings", ascending=False)
    books_ratings = books_ratings.drop_duplicates(
        subset=["title", "author"], keep="first"
    )
    return books_ratings.reset_index(drop=True)
