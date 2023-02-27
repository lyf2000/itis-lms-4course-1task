import string

import nltk

nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
from nltk.corpus import stopwords
from stop_words import get_stop_words

stop_words = list(get_stop_words('en'))         #Have around 900 stopwords
nltk_words = list(stopwords.words('english'))   #Have around 150 stopwords
stop_words.extend(nltk_words)

from nltk.tokenize import WordPunctTokenizer

tokens = list()
 
import os
import re
from pathlib import Path


def clean_text(text):
    # remove numbers
    text_nonum = re.sub(r'\d+', '', text)
    # remove punctuations and convert characters to lower case
    text_nopunct = "".join([char for char in text_nonum if char not in string.punctuation]) 
    # substitute multiple whitespace with single whitespace
    # Also, removes leading and trailing whitespaces
    # text_no_doublespace = re.sub('\s+', ' ', text_nopunct).strip()
    return text_nopunct.strip()


def get_bios(word):
    if '[' in word and ']' in word:
        return word
    for ch in r'\/(),-.{}@=':
        if ch in word and (word[0] != ch and word[-1] != ch):
            return word
    if '[' in word and ']' in word:
        return word
    if '(' in word and ')' in word:
        return word
    return ''


tok = WordPunctTokenizer()
for i in range(0, 100):
    with open(os.path.join(Path(__file__).resolve().parent, f'{i}.txt'), 'r') as f:
        if i == 20:
            i = 20
        for line in f.readlines():
            bio = []
            for word in line.split(' '):
                b = get_bios(word) 
                if b:
                    bio.append(b)
                    line = line.replace(b, '')
                bi = []

            for sent in nltk.sent_tokenize(line):
                sent = clean_text(sent)
                tokens +=  bio
                tokens += tok.tokenize(sent)
                # if 'hcsccccncoochncocnocccscnnco' in [i.lower() for i in tokens]:
                #     bio = []

import re


def isNumber(value):
    val = value.replace('.','',1)
    val = val.replace('-','')
    return val.isdigit()

tokens = set([t.lower() for t in tokens])
tokens = set([t for t in tokens if (t not in stop_words) and (not isNumber(t))])

with open('tokens.txt', 'w') as f:
    for t in tokens:
        f.write(f'{t}\n')


from collections import defaultdict

from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()


from nltk import pos_tag

lemmas = defaultdict(list)
for t, tag in pos_tag(tokens):
    wntag = tag[0].lower()
    wntag = wntag if wntag in ['a', 'r', 'n', 'v'] else None
    if not wntag:
        lemma = t
    else:
        lemma = lemmatizer.lemmatize(t, wntag)
    lemmas[lemma].append(t)
    
with open('lemmas.txt', 'w') as f:
    for key, words in lemmas.items():
        words = ', '.join(words)
        f.write(f'{key}: {words}\n')
