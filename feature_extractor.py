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
        pd.Series(report).to_csv(filename.replace('.pdf', '.csv'))

        vec = CountVectorizer(ngram_range=(1, 2), vocabulary=vocab)
        return vec.fit_transform(report).toarray().sum(axis=0)

def process_folder(folder: str, vocab: List[str]) -> pd.DataFrame:
    freq_matrix = []
    for filename in tqdm(glob(folder + '*.pdf')):
        try:
            freq_matrix.append(
                process_file(filename, vocab)
            )
        except:
            print(filename)
            freq_matrix.append(
                np.full(len(vocab), np.nan)
            )
    
    df = pd.DataFrame(np.vstack(freq_matrix), columns=vocab)
    return df

def main():
    folder = "data/statements_clean/"
    vocab = pd.read_csv("vocab.csv")
    matrix = process_folder(folder, vocab.token)
    # assert len(os.listdir(folder)) == matrix.shape[0]
    return matrix

if __name__ == "__main__":
    main()