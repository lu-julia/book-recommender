# Book Recommender System

## Dataset
The dataset used in this project is the [Kaggle Book Recommendation Dataset](https://www.kaggle.com/datasets/arashnic/book-recommendation-dataset/data).

## Recommendation system approaches

Recommendation systems help users discover items, such as movies, books, music, or products, based on their preferences. There are several approaches to building recommendation systems, the most widely used being collaborative filtering. Collaborative filtering makes recommendations based on user behavior—in our case, the ratings that users have given to books. It assumes that if two users have rated similar books highly, they will likely enjoy other books rated highly by the other.

Collaborative filtering can be divided into two types:

* Memory-based methods compute similarities between users or items directly from the user-item rating matrix. They often do not scale well to large datasets and are sensitive to data sparsity, making them less effective when users have rated only a few items.

* Model-based methods, like Singular Value Decomposition (SVD), use matrix factorization to transform the original sparse rating matrix into a lower-dimensional representation that captures underlying patterns in user preferences. These approaches are more scalable and handle sparsity better.
