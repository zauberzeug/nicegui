# Import the necessary libraries
import sqlite3
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
import scipy.sparse as sp


# Connect to the SQLite database
def connect_to_database():
    return sqlite3.connect('db.sqlite3')


# Fetch user preferences from the database for the specified user
def fetch_user_preferences_from_database(cursor, user_id):
    cursor.execute("""
        SELECT main.user_liquor.liquor_id
        FROM user_liquor
        WHERE main.user_liquor.user_id = ?
        """, (user_id,))
    preferences_data = cursor.fetchall()
    user_preferences = []

    for preference in preferences_data:
        cursor.execute("""
            SELECT main.liquor.name
            FROM liquor
            WHERE main.liquor.id = ?
            """, (preference[0],))
        category_name = cursor.fetchone()
        if category_name:
            user_preferences.append(category_name[0])

    return user_preferences


# Fetch event data from the database
def fetch_event_data_from_database(cursor, ev_ids):
    cursor.execute("""
        SELECT main.cocktail.id, desc
        FROM cocktail
    """)
    event_data = cursor.fetchall()

    event_ids = []
    event_descriptions = []
    event_categories = []

    for event in event_data:
        if event[0] not in ev_ids:
            event_ids.append(event[0])
            event_descriptions.append(event[1])

            cursor.execute("""
                SELECT main.cocktail_liquor.liquor_id
                FROM cocktail_liquor
                WHERE main.cocktail_liquor.cocktail_id = ?
            """, (event[0],))

            category_ids = cursor.fetchall()

            for category_id in category_ids:
                cursor.execute("""
                    SELECT main.liquor.name
                    FROM liquor
                    WHERE main.liquor.id = ?
                """, (category_id[0],))
                category_name = cursor.fetchone()
                if category_name:
                    event_categories.append(category_name[0])

    return event_ids, event_descriptions, event_categories



# Fetch user ratings from the database for the specified user
def fetch_user_ratings_from_database(user_id):
    conn = connect_to_database()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT main.user_cocktail.cocktail_id, main.user_cocktail.rating 
        FROM user_cocktail 
        WHERE main.user_cocktail.user_id = ?
    """, (user_id,))

    ratings_data = cursor.fetchall()

    if ratings_data:
        user_ratings = {rating[0]: rating[1] for rating in ratings_data}
    else:
        user_ratings = {}

    event_ids = []
    for i in range(len(ratings_data)):
        if ratings_data[i][1] == 1:
            event_ids.append(ratings_data[i][0])

    cursor.close()
    conn.close()

    return user_ratings, event_ids

# Generate recommendations for the specified user
def generate_recommendations(user_id, cursor, N):

    user_preferences = fetch_user_preferences_from_database(cursor, user_id)
    user_ratings, ev_ids = fetch_user_ratings_from_database(user_id)
    event_ids, event_descriptions, event_categories = fetch_event_data_from_database(cursor, ev_ids)

    # TF-IDF vectorization of event descriptions and user preferences
    event_descriptions = [desc + ' ' + cat for desc, cat in zip(event_descriptions, event_categories)]
    tfidf_vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=2)
    event_description_matrix = tfidf_vectorizer.fit_transform(event_descriptions)

    user_descriptions = ' '.join(user_preferences)
    user_description_matrix = tfidf_vectorizer.transform([user_descriptions])

    # Ratings
    event_user_ratings = np.zeros(len(event_ids))

    for event_id in user_ratings.keys():
        if event_id in event_ids:
            event_index = event_ids.index(event_id)
            event_user_ratings[event_index] = user_ratings[event_id]

    ratings_scaler = MinMaxScaler()

    # Calculate cosine similarity
    event_user_similarity_pref = cosine_similarity(user_description_matrix, event_description_matrix) * 0.5
    event_user_ratings = ratings_scaler.fit_transform(event_user_ratings.reshape(-1, 1)).flatten() * 0.5
    event_total_similarity = event_user_similarity_pref.flatten() +  event_user_ratings


    # Get the top N event indices based on total similarity score
    top_n_event_indices = np.argsort(event_total_similarity)[::-1][:N]

    # Get the top N recommended event ids
    recommended_events = [event_ids[i] for i in top_n_event_indices]

    return recommended_events


# Entry point of the script
def m(user_id):

    conn = connect_to_database()
    cursor = conn.cursor()

    # Assuming N is the number of recommendations to generate
    N = 3

    # Generate recommendations for the specified user
    recommended_events = generate_recommendations(user_id, cursor, N)

    # Close the database connection
    cursor.close()
    conn.close()

    return recommended_events


if __name__ == '__main__':
    r = m(1)
    print(r)

