from PyPDF2 import PdfReader
from glob import glob
from sklearn.feature_extraction.text import CountVectorizer
from tqdm import tqdm
import numpy as np
import os

files = glob('data/statements/20*/*')

def process_file(filename, vocab):
    reader = PdfReader(filename)
    report = [page.extract_text() for page in reader.pages]

    vec = CountVectorizer(vocabulary=vocab)
    return vec.fit_transform(report).toarray().sum(axis=0)

def process_folder(folder, vocab):
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
    folder = "data/statements/2019/"
    vocab = ["digital", "media"]
    matrix = process_folder(folder, vocab)
    # assert len(os.listdir(folder)) == matrix.shape[0]
    print(matrix)