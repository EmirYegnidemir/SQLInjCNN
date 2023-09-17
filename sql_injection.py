#!/bin/bash
import keras
from keras.models import load_model
import pickle
import re
import os
import sys

SAFE_CHARACTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

mymodel = load_model('model_cnn_3.h5')
myvectorizer = pickle.load(open("vectorizer_cnn", 'rb'))

def is_safe_input(user_in):
    return all(char in SAFE_CHARACTERS for char in user_in)

def predict_sqli_attack(input_val):

    # Clean and preprocess the input_val
    input_val = clean_data(input_val)

    input_val = [input_val]
    input_val = myvectorizer.transform(input_val).toarray()
    input_val = input_val.reshape(-1, 64, 64, 1)  # Reshape to (batch_size, 64, 64, 1)

    result = mymodel.predict(input_val)

    if result > 0.8:
        print("ALERT :::: This can be SQL injection")
    else:
        print("It seems to be safe")


def clean_data(user_in):
    patterns = [
        (r'\n', ''),
        (r'%20', ' '),
        (r'=', ' = '),
        (r'\(\(', ' (( '),
        (r'\)\)', ' )) '),
        (r'\(', ' ( '),
        (r'\)', ' ) '),
        (r'1 ', 'numeric '),
        (r' 1', 'numeric'),
        (r"'1 ", "'numeric "),
        (r" 1'", " numeric'"),
        (r'1,', 'numeric,'),
        (r' 2 ', ' numeric '),
        (r' 3 ', ' numeric '),
        (r' 3--', ' numeric--'),
        (r' 4 ', ' numeric '),
        (r' 5 ', ' numeric '),
        (r' 6 ', ' numeric '),
        (r' 7 ', ' numeric '),
        (r' 8 ', ' numeric '),
        (r'1234', ' numeric '),
        (r'22', ' numeric '),
        (r' 8 ', ' numeric '),
        (r' 200 ', ' numeric '),
        (r'23 ', ' numeric '),
        (r'"1', '"numeric'),
        (r'1"', '"numeric'),
        (r'7659', 'numeric'),
        (r' 37 ', ' numeric '),
        (r' 45 ', ' numeric ')
    ]

    for pattern, replacement in patterns:
        user_in = re.sub(pattern, replacement, user_in)

    return user_in

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python predict_sqli_attack.py <message>")
        sys.exit(1)

    input_val = sys.argv[1]
    predict_sqli_attack(input_val)
