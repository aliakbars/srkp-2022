from glob import glob
from sklearn.feature_extraction.text import CountVectorizer
from tqdm import tqdm
from typing import List
import numpy as np
import os
import pandas as pd
import pdfplumber

files = glob('data/statements/20*/*')

def process_file(filename: str, vocab: List[str]) -> np.ndarray:
    with pdfplumber.open(filename) as pdf:
        report = [page.extract_text(layout=True) for page in pdf.pages]

        vec = CountVectorizer(ngram_range=(1, 2), vocabulary=vocab)
        return vec.fit_transform(report).toarray().sum(axis=0)

def process_folder(folder: str, vocab: List[str]) -> np.ndarray:
    freq_matrix = []
    for filename in tqdm(os.listdir(folder)):
        try:
            freq_matrix.append(
                process_file(folder + filename, vocab)
            )
        except:
            print(filename)
    
    return np.vstack(freq_matrix)

if __name__ == "__main__":
    folder = "data/statements/2018/"
    vocab = pd.read_csv("vocab.csv")
    matrix = process_folder(folder, vocab.token)
    # assert len(os.listdir(folder)) == matrix.shape[0]
    print(matrix)