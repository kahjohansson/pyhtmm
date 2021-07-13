import json, os, jsonlines
from tqdm import tqdm

from .utils import *
from .document import _Document
from .sentence import _Sentence

word_index = {} #string: int
index_word = {} #int: string
index = 0

def process_plain_text(filename):
    file = open(filename)
    docs = []
    for line in file:
        docs.append(process(line))
    return docs

def process_jsonlines(filename, data_field):
    with jsonlines.open(filename, 'r') as reader:
        docs = []
        for doc in reader:
            docs.append(process(doc[data_field]))
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


def read_train_documents(data_dir, file_type='plain_text', data_field=None):
    docs = []
    print("Loading all train documents...")

    function_name = ''
    if file_type == 'plain_text':
        function_name = 'process_plain_text(data_dir+filename)'
    elif file_type == 'jsonlines':
        function_name = 'process_jsonlines(data_dir+filename, data_field)'

    for filename in tqdm(os.listdir(data_dir)):
        docs += eval(function_name)

    return docs, word_index, index_word
