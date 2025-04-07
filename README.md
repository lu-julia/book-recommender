# Book Recommendation App

This project aims to build a book recommendation system that provides personalized book suggestions to users based on their reading preferences and ratings. The project includes an interactive web application that allows users to search for books, rate them, and receive recommendations.

## Dataset
The dataset used in this project is the [Kaggle Book Recommendation Dataset](https://www.kaggle.com/datasets/arashnic/book-recommendation-dataset/data).
It consists of 3 CSV files : 
* `Books.csv` : Contains information about books, including their title, author, year of publication.
* `Ratings.csv` : Contains user ratings for books.
* `Users.csv` : Contains inforamtion about users, including their age and location.

## Recommendation systems

Recommendation systems help users discover items, such as movies, books, music, or products, based on their preferences. They are two main approaches to building recommendation systems : 

* **Content-based filtering** recommends books based on their attributes, such as genres, authors, or descriptions. It matches the content of books the user liked in the past to find similar ones.

* **Collaborative filtering** recommends books based on the ratings that users have given to books. It assumes that if two users have rated similar books highly, they will likely enjoy other books rated highly by the other. Matrix factorization techniques, such as Singular Value Decomposition (SVD), can be used to reduce the dimensionality of the user-item rating matrix. 
