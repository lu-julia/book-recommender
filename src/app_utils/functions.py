import pandas as pd


def get_my_books(df_ratings, user_id):
    result = df_ratings.loc[df_ratings["user_id"] == user_id]
    return result

def get_book_id(df_books, title):
    result = df_books.loc[df_books['title'] == title, 'ISBN']
    return result.iloc[0]

def add_book(df_user, user_id, isbn):
    new_row = {
        'user_id': user_id,
        'ISBN': isbn,
        'rating': 0.0
    }
    df_new_row = pd.DataFrame([new_row])
    df_user = pd.concat([df_user, df_new_row], ignore_index=True)
    return df_user

def add_rating(df_user, row, rating):
    df_user.loc[(df_user['ISBN'] == row['ISBN']) &
                (df_user['user_id'] == row['user_id']), 'rating'] = rating
    return df_user

def update_books(df_user, df_ratings, user_id):
    result = get_my_books(df_ratings, user_id)
    for index in range(len(df_user)):
        row = df_user.iloc[index]
        if row['ISBN'] not in result['ISBN'].tolist():
            new_row = {
                'user_id': user_id,
                'ISBN': row['ISBN'],
                'rating': row['rating']
            }
            df_new_row = pd.DataFrame([new_row])
            df_ratings = pd.concat([df_ratings, df_new_row], ignore_index=True)
        else:
            if not result.isin([row]).all(axis=1).any():
                df_ratings = add_rating(df_ratings, row, row['rating'])
    return df_ratings