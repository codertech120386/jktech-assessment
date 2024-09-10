from fastapi import HTTPException, status
import pandas as pd
from icecream import ic

from src.utils import read_pickle_files_from_s3


def machine_learning_recommendations(rating: int, genre: str):
    try:
        genre_list = ['Fantasy', 'Science Fiction', 'Romance', 'Mystery', 'Horror']
        genre_dict = {i: index + 1 for index, i in enumerate(genre_list)}

        df = pd.read_csv("books_data.csv")
        loaded_model_knn = read_pickle_files_from_s3(file_name="knn_model.pkl")
        loaded_scaler = read_pickle_files_from_s3(file_name="scaler.pkl")

        # Use the loaded scaler to transform new data
        new_data = [[rating]]
        scaled_new_data = loaded_scaler.transform(new_data)

        scaled_rating = scaled_new_data[0][0]

        _, indices = loaded_model_knn.kneighbors([[genre_dict[genre], scaled_rating]])

        # Display the recommended books
        recommended_books = df.iloc[indices[0]]

        return recommended_books[['title']].values.flatten().tolist()

    except Exception as e:
        ic(e)
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Something went wrong .. please try again later.")
