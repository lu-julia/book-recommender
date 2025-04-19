# Book Recommendation App

[![Build and push Docker image](https://github.com/lu-julia/book-recommender/actions/workflows/prod.yml/badge.svg)](https://github.com/lu-julia/book-recommender/actions/workflows/prod.yml)
[![Pylint](https://github.com/lu-julia/book-recommender/actions/workflows/pylint.yml/badge.svg)](https://github.com/lu-julia/book-recommender/actions/workflows/pylint.yml)

## Description

This project is a book recommendation application that helps users discover new books given their reading history. The application is built using Streamlit. It allows users to search for books, rate them, and view their recommendations based on the ratings they have given.
The application makes use of collaborative filtering to provide personalized book suggestions to users. Collaborative filtering is a technique that analyzes user behavior and preferences to recommend items that similar users have liked. 

This project was developed as part of the *Mise en production de projets de Data Science* course at ENSAE Paris.


### Dataset
The dataset used in this project is the [Kaggle Book Recommendation Dataset](https://www.kaggle.com/datasets/arashnic/book-recommendation-dataset/data).

It includes 2 main files :
* `Books.csv` : Contains information about the books, including the title, author, publisher, and year of publication.
* `Ratings.csv` : Contains user ratings for the books, including the user id, book id, and rating.

These files are stored on a S3 bucket in SSP Cloud.


### Project Structure

```plaintext
book_recommender/
├── deployment/                             # Kubernetes configuration files        
├── notebooks/                              # Notebooks for data exploration
├── pages/                                  # Streamlit multi-page components
│   ├── book_info.py                       
│   ├── home.py                             
│   ├── my_books.py                         
│   └── search.py             
├── src/                                    
│   ├── app_utils/                          # Utility functions for the application
│   |   ├── functions.py                    
│   |   ├── logger.py                       
│   |   ├── session.py                     
│   |   └── ui_elements.py                 
│   ├── data/                               # Data loading and preprocessing
│   │   ├── load_data.py                    
│   │   └── preprocessing.py              
│   └── recommendation/                     # Recommendation models
│       ├── collaborative_filtering.py      
│       └── popularity_based.py             
├── Dockerfile                              
├── app.py                                  # Main entry point of the Streamlit application
├── application.yaml                        # ArgoCD deployment configuration
└── requirements.txt                       
```


## Installation

### Environment Setup

To access the S3 bucket, create an `.env` file with your [authentification keys](https://datalab.sspcloud.fr/account/storage). 
The file should contain the following variables :
```
AWS_ACCESS_KEY_ID=your_access_key_id
AWS_SECRET_ACCESS_KEY=your_secret_access_key
AWS_SESSION_TOKEN=your_session_token
```

### Running the app with Python

#### Prerequisites

* Python installed
* An `.env` file with your S3 bucket credentials

To run the application locally using Python, follow these steps :

1. Clone this repository
```
git clone https://github.com/lu-julia/book-recommender.git
cd book-recommender
```

2. Install dependencies 
```
pip install -r requirements.txt 
```

3. Add the `.env` file to the root directory of the project.

4. Launch the app
```
streamlit run app.py
```

5. Open your web browser and go to `http://localhost:8501` to access the app.


### Running the app with Docker

#### Prerequisites

* Docker installed on your machine
* An `.env` file in your working directory with your S3 bucket credentials

Alternatively, the application can be run using an already built Docker image available on Docker Hub. To run the app, follow these steps :

1. Pull the Docker image
```
docker pull lujulia/mise-en-production:v1.0.1
```

2. Run the Docker container
```
docker run -p 8501:8501 --env-file .env lujulia/mise-en-production:v1.0.1
```

The application will be accessible at `http://localhost:8501`.


## Deployment on Kubernetes

The application is deployed on a Kubernetes cluster hosted by SSP Cloud. The deployment is managed using ArgoCD. 
A CI/CD pipeline ensures continuous integration and delivery of the application to the Kubernetes cluster :

**Continuous integration (CI)** : Any change pushed to this repository triggers a GitHub Actions workflow. This workflow automatically builds the Docker image and pushes it to Docker Hub with a versioned tag.

**Continuous deployment (CD)** : When the `deployment/deployment.yml` file is updated (e.g., to reference a new image version), ArgoCD automatically syncs the changes to the Kubernetes cluster.

The deployed application can be accessed at the following URL : 

<div align="center">

https://your-next-read.lab.sspcloud.fr/

<div align="left">



## Demo

![app_demo_1](https://github.com/user-attachments/assets/194953bc-819d-4324-af25-fe37da852b27)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Authors

* Julia LU
* Guilhem GRIVAUX

## Acknowledgements

* [Kaggle Book Recommendation Dataset](https://www.kaggle.com/datasets/arashnic/book-recommendation-dataset/data)
* [Book Recommendation System](https://github.com/RadhikaRM/Bookrecommendersystem.git)
* [Recommandation_Project](https://github.com/davidserruya/Recommandation_Project)

