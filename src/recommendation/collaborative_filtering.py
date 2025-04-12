import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import svds


def create_user_item_matrix(ratings: pd.DataFrame):
    """
    Creates a sparse user-book matrix from a DataFrame of ratings.
    
    Args:
        ratings (pd.DataFrame): DataFrame containing userId, ISBN, and rating columns.
    
    Returns:
        user_item_matrix (csr_matrix): Sparse matrix of user-book interactions.
        user_mapper (dict): Dictionary that maps user id's to user indices.
        book_mapper (dict): Dictionary that maps book id's to book indices.
    """
    user_item_df = ratings.pivot(index="user_id", columns="ISBN", values="rating").fillna(0)
    user_mapper = {uid: i for i, uid in enumerate(user_item_df.index)}
    book_mapper = {bid: i for i, bid in enumerate(user_item_df.columns)}
    user_item_matrix = csr_matrix(user_item_df.values, dtype=float)
    return user_item_matrix, user_mapper, book_mapper


def compute_svd(
        matrix: csr_matrix, 
        user_mapper: dict, 
        book_mapper: dict, 
        n_factors: int
    ) -> pd.DataFrame:
    """
    Computes the SVD of the user-book matrix and returns the predicted ratings.

    Args:
        matrix (csr_matrix): Sparse user-book matrix.
        n_factors (int): Number of factors / rank of the latent matrix for factorization.
        user_mapper (dict): Dictionary that maps user id's to their respective indices.
        book_mapper (dict): Dictionary that maps book id's to their respective indices.

    Returns:
        pd.DataFrame : Predicted ratings for all users in the original dataset.     
    """   
    U, sigma, V_t = svds(matrix, k=n_factors)
    sigma = np.diag(sigma)
    pred_ratings = np.dot((U @ sigma), V_t)
    preds_df = pd.DataFrame(pred_ratings, columns=book_mapper.keys(), index=user_mapper.keys())    
    return preds_df


def cf_recommendation(
        ratings: pd.DataFrame, 
        books: pd.DataFrame, 
        user_id: int, 
        n_reco: int, 
        n_factors: int = 50
    ) -> pd.DataFrame:
    """
    Recommends books to a user based on collaborative filtering using SVD.

    Args:
        ratings (pd.DataFrame): DataFrame containing userId, ISBN, and rating columns.
        books (pd.DataFrame): DataFrame containing book metadata.
        user_id (int): The user id of the user we want to make recommandations to.
        n_reco (int): The number of books we want to recommand to the user.
        n_factors (int): The number of factors / rank of the latent matrix for factorization

    Returns:
        pd.DataFrame : DataFrame containing the recommended books for the user.
    """
    # Create user-book matrix
    matrix, user_mapper, book_mapper = create_user_item_matrix(ratings)
    # Compute SVD
    preds_df = compute_svd(matrix, user_mapper, book_mapper, n_factors)
    # Get the user's predicted ratings
    user_preds = preds_df.loc[user_id].sort_values(ascending=False)
    # Books the user already rated
    user_data = ratings[ratings['user_id'] == user_id]
    read_books = set(user_data['ISBN'])
    # Filter books not already rated in the recommendations
    recommendations = user_preds[~user_preds.index.isin(read_books)].head(n_reco)
    # Join with book metadata
    books_reco = books[books["ISBN"].isin(recommendations.index)]
    return books_reco
