# Import necessary libraries
import sqlite3
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
import scipy.sparse as sp


# Function to connect to the SQLite database
def connect_to_database():
    return sqlite3.connect('db.sqlite3')


# Function to fetch user liquor preferences from the database for a specified user
def fetch_user_preferences_from_database(cursor, user_id):
    # Execute SQL command to get the user's liquor preferences
    cursor.execute("""
        SELECT main.user_liquor.liquor_id
        FROM user_liquor
        WHERE main.user_liquor.user_id = ?
        """, (user_id,))
    # Fetch the query results
    preferences_data = cursor.fetchall()
    user_preferences = []

    # Loop over the results to fetch the corresponding liquor names
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


# Function to fetch cocktail data from the database
def fetch_cocktail_data_from_database(cursor, ev_ids):
    # Execute SQL command to get all cocktails and their descriptions
    cursor.execute("""
        SELECT main.cocktail.id, desc
        FROM cocktail
    """)
    # Fetch the query results
    cocktail_data = cursor.fetchall()

    cocktail_ids = []
    cocktail_descriptions = []
    cocktail_categories = []

    # Loop over the results to fetch the liquor types for each cocktail
    for cocktail in cocktail_data:
        if cocktail[0] not in ev_ids:
            cocktail_ids.append(cocktail[0])
            cocktail_descriptions.append(cocktail[1])

            cursor.execute("""
                SELECT main.cocktail_liquor.liquor_id
                FROM cocktail_liquor
                WHERE main.cocktail_liquor.cocktail_id = ?
            """, (cocktail[0],))

            category_ids = cursor.fetchall()

            for category_id in category_ids:
                cursor.execute("""
                    SELECT main.liquor.name
                    FROM liquor
                    WHERE main.liquor.id = ?
                """, (category_id[0],))
                category_name = cursor.fetchone()
                if category_name:
                    cocktail_categories.append(category_name[0])

    return cocktail_ids, cocktail_descriptions, cocktail_categories


# Function to fetch user ratings from the database for the specified user
def fetch_user_ratings_from_database(user_id):
    # Connect to the database
    conn = connect_to_database()
    cursor = conn.cursor()

    # Execute SQL command to get the user's cocktail ratings
    cursor.execute("""
        SELECT main.user_cocktail.cocktail_id, main.user_cocktail.rating 
        FROM user_cocktail 
        WHERE main.user_cocktail.user_id = ?
    """, (user_id,))

    # Fetch the query results
    ratings_data = cursor.fetchall()

    # Convert the results to a dictionary of {cocktail_id: rating}
    if ratings_data:
        user_ratings = {rating[0]: rating[1] for rating in ratings_data}
    else:
        user_ratings = {}

    # Also collect all cocktail_ids that user has rated as 1
    cocktail_ids = []
    for i in range(len(ratings_data)):
        if ratings_data[i][1] == 1:
            cocktail_ids.append(ratings_data[i][0])

    # Close database connection
    cursor.close()
    conn.close()

    return user_ratings, cocktail_ids


# Function to generate recommendations for the specified user
def generate_recommendations(user_id, cursor, N):
    # Fetch the user's liquor preferences, ratings and all cocktail data from the database
    user_preferences = fetch_user_preferences_from_database(cursor, user_id)
    user_ratings, ev_ids = fetch_user_ratings_from_database(user_id)
    cocktail_ids, cocktail_descriptions, cocktail_categories = fetch_cocktail_data_from_database(cursor, ev_ids)

    # Vectorize the cocktail descriptions and user preferences using TF-IDF
    cocktail_descriptions = [desc + ' ' + cat for desc, cat in zip(cocktail_descriptions, cocktail_categories)]
    tfidf_vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=2)
    cocktail_description_matrix = tfidf_vectorizer.fit_transform(cocktail_descriptions)

    user_descriptions = ' '.join(user_preferences)
    user_description_matrix = tfidf_vectorizer.transform([user_descriptions])

    # Initialize a zero vector for cocktail ratings
    cocktail_user_ratings = np.zeros(len(cocktail_ids))

    # Update the ratings vector with the user's ratings
    for cocktail_id in user_ratings.keys():
        if cocktail_id in cocktail_ids:
            cocktail_index = cocktail_ids.index(cocktail_id)
            cocktail_user_ratings[cocktail_index] = user_ratings[cocktail_id]

    # Scale the ratings between 0 and 1
    ratings_scaler = MinMaxScaler()

    # Compute the cosine similarity between the user's preferences and cocktail descriptions
    cocktail_user_similarity_pref = cosine_similarity(user_description_matrix, cocktail_description_matrix) * 0.5
    cocktail_user_ratings = ratings_scaler.fit_transform(cocktail_user_ratings.reshape(-1, 1)).flatten() * 0.5
    event_total_similarity = cocktail_user_similarity_pref.flatten() +  cocktail_user_ratings

    # Get the top N cocktail indices based on total similarity score
    top_n_cocktail_indices = np.argsort(event_total_similarity)[::-1][:N]

    # Get the top N recommended cocktail ids
    recommended_events = [cocktail_ids[i] for i in top_n_cocktail_indices]

    return recommended_events


# Entry point of the script
def m(user_id):
    # Connect to the database
    conn = connect_to_database()
    cursor = conn.cursor()

    # Assuming N is the number of recommendations to generate
    N = 3

    # Generate recommendations for the specified user
    recommended_cocktails = generate_recommendations(user_id, cursor, N)

    # Close the database connection
    cursor.close()
    conn.close()

    return recommended_cocktails


# Call the main function if this script is being run as the main program
if __name__ == '__main__':
    r = m(1)
    print(r)

