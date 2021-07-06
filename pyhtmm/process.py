import json, os
from tqdm import tqdm

from .utils import *
from .document import _Document
from .sentence import _Sentence

word_index = {} #string: int
index_word = {} #int: string
index = 0

def process_file(filename):
    file = open(filename)
    docs = []
    for line in file:
        docs.append(process(line))
    return docs

def process(txt):
    global index
    sentences = paragraph2sentence(txt)
    doc = _Document()
    for stn in sentences:
        sentence = _Sentence(stn)
        for w in filter_wordlist(sentence2word_normalized(stn)):
            if w in word_index:
                sentence.add_word(word_index[w])
            else:
                word_index[w] = index
                index_word[index] = w
                index += 1

        doc.add_sentence(sentence)
    return doc

def process_doc(txt, word2index):
    sentences = paragraph2sentence(txt)
    doc = _Document()
    for stn in sentences:
        sentence = _Sentence(stn)
        for w in filter_wordlist(sentence2word_normalized(stn)):
            if w in word2index:
                sentence.add_word(word2index[w])
        doc.add_sentence(sentence)
    return doc


def read_train_documents(data_dir):
    docs = []
    print("Loading all train documents...")

    for filename in tqdm(os.listdir(data_dir)):
        docs += process_file(data_dir+filename)

    return docs, word_index, index_word
