# Book Recommendation App

This project aims to build a book recommendation system that provides personalized book suggestions to users based on their reading preferences and ratings. The project includes an interactive web application that allows users to search for books, rate them, and receive recommendations.

## Features


## Dataset
The dataset used in this project is the [Kaggle Book Recommendation Dataset](https://www.kaggle.com/datasets/arashnic/book-recommendation-dataset/data).

It consists of 2 main files :
* `Books.csv` : Contains information about the books, including the title, author, publisher, and year of publication.
* `Ratings.csv` : Contains user ratings for the books, including the user id, book id, and rating.

The data is stored in SSP Cloud's S3 storage bucket.


<!-- ## Recommendation systems

Recommendation systems help users discover items, such as movies, books, music, or products, based on their preferences. They are two main approaches to building recommendation systems : 

* **Content-based filtering** recommends books based on their attributes, such as genres, authors, or descriptions. It matches the content of books the user liked in the past to find similar ones.

* **Collaborative filtering** recommends books based on the ratings that users have given to books. It assumes that if two users have rated similar books highly, they will likely enjoy other books rated highly by the other. Matrix factorization techniques, such as Singular Value Decomposition (SVD), can be used to reduce the dimensionality of the user-item rating matrix.  -->


## Project Structure

```plaintext
book_recommender/
├── notebooks/
├── pages/
│   ├── home.py                  
│   ├── my_books.py                
│   └── search.py             
├── src/
│   ├── app_utils/
│   |   ├── functions.py                
│   |   └── session.py                
│   ├── data/
│   │   ├── load_data.py             
│   │   └── preprocessing.py              
│   └── recommendation/
│       ├── collaborative_filtering.py 
│       └── popularity_based.py 
├── app.py
└── requirements.txt       
```


## Installation

To run the app locally, follow these steps :

1. Clone this repository 
```
git clone https://github.com/lu-julia/book-recommendation.git
```

2. Install the required dependencies 
```
pip install -r requirements.txt 
```

3. Set up your environment variables to access the S3 bucket.

Create a `.env` file in the root directory of the project with your [authentification keys](https://datalab.sspcloud.fr/account/storage).
The file should contain the following variables :
```
AWS_ACCESS_KEY_ID=your_access_key_id
AWS_SECRET_ACCESS_KEY=your_secret_access_key
AWS_SESSION_TOKEN=your_session_token
AWS_DEFAULT_REGION=your_region
```

4. Launch the app
```
streamlit run app.py
```

5. Open your web browser and go to `http://localhost:8501` to access the app.


## Contributors

* Julia LU
* Guilhem GRIVAUX
