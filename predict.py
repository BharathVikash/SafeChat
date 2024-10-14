import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import joblib

tokenizer = joblib.load('tokenizer.pkl')


# Load the saved model for making predictions
loaded_model = keras.models.load_model('model.h5')

tokenizer = tokenizer  # Replace with your tokenizer
max_sequence_length = 100  # Replace with your max_sequence_length


def predict_text(input_text):
    # Tokenize and preprocess the input text
    input_sequence = tokenizer.texts_to_sequences([input_text])
    input_padded = pad_sequences(input_sequence, maxlen=max_sequence_length)

    # Make predictions
    prediction = loaded_model.predict(input_padded)

    return prediction[0][0]*100


if __name__=='__main__':
    print(predict_text("Hello there"))
