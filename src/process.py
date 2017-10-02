# coding: utf-8
import json
import operator

from tqdm import tqdm
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import *
from collections import defaultdict

NUMBER_OF_FILES = 266546

def build_dataset():

    stemmer = PorterStemmer()
    stopwords_english = stopwords.words('english')
    punctiation_words = ['.', ',', ';', ':', '(', ')', '`', '\'', '\'\'', '-', '–', '—', '…', '[', ']', '...', '{', '}']
    forbidden_words = ['']
    punctiation_chars = ['`']

    out_raw = open('raw.txt', 'w')

    out_tokenized = open('tokenized.txt', 'w')
    vocab_tokenized = defaultdict(int)

    out_lowercased = open('lowercased.txt', 'w')
    vocab_lowercased = defaultdict(int)

    out_without_punctuation = open('without-punctuation.txt', 'w')
    vocab_without_punctuation = defaultdict(int)

    out_without_stop_words = open('without-stop-words.txt', 'w')
    vocab_without_stop_words = defaultdict(int)

    out_stemmed = open('stemmed.txt', 'w')
    vocab_stemmed = defaultdict(int)

    for (title, extract) in raw_iterator():

        out_raw.write('%s ||| %s\n' % (title, extract))

        title = word_tokenize(title)
        extract = word_tokenize(extract)

        add_to_vocab(title, extract, vocab_tokenized)
        out_tokenized.write('%s ||| %s\n' % (' '.join(title), ' '.join(extract)))

        # to lower case
        title = [t.lower() for t in title]
        extract = [t.lower() for t in extract]

        add_to_vocab(title, extract, vocab_lowercased)
        out_lowercased.write('%s ||| %s\n' % (' '.join(title), ' '.join(extract)))

        # remove punctuation
        title = [t for t in title if t not in punctiation_words]
        extract = [t for t in extract if t not in punctiation_words]

        # remove punctuation chars
        title = [''.join(c for c in t if c not in punctiation_chars) for t in title]
        extract = [''.join(c for c in t if c not in punctiation_chars) for t in extract]

        # forbidden words
        title = [t for t in title if t not in forbidden_words]
        extract = [t for t in extract if t not in forbidden_words]

        add_to_vocab(title, extract, vocab_without_punctuation)
        out_without_punctuation.write('%s ||| %s\n' % (' '.join(title), ' '.join(extract)))

        title = [t for t in title if t not in stopwords_english]
        extract = [t for t in extract if t not in stopwords_english]

        add_to_vocab(title, extract, vocab_without_stop_words)
        out_without_stop_words.write('%s ||| %s\n' % (' '.join(title), ' '.join(extract)))

        title = [stemmer.stem(t) for t in title]
        extract = [stemmer.stem(t) for t in extract]

        add_to_vocab(title, extract, vocab_stemmed)
        out_stemmed.write('%s ||| %s\n' % (' '.join(title), ' '.join(extract)))

    write_vocab(vocab_tokenized, 'tokenized.vocab')
    write_vocab(vocab_lowercased, 'lowercased.vocab')
    write_vocab(vocab_without_punctuation, 'without-punctuation.vocab')
    write_vocab(vocab_without_stop_words, 'without-stop-words.vocab')
    write_vocab(vocab_stemmed, 'stemmed.vocab')

def add_to_vocab(title, extract, vocab):
    for t in title:
        vocab[t] += 1
    for t in extract:
        vocab[t] += 1

def write_vocab(vocab, out_path):
    out = open(out_path, 'w')

    sorted_vocab = sorted(vocab.items(), key=operator.itemgetter(1), reverse=True)

    for (word, count) in sorted_vocab:
        out.write('%s %s\n' % (word, count))


def process_text(text):
    return ' '.join([line.strip() for line in text.splitlines()]).replace(' ||| ', ' ')

def raw_iterator():

    for i in tqdm(range(NUMBER_OF_FILES)):
        in_f = open('out/%d.json' % i, 'rb')
        data = json.load(in_f)

        for page_id in data['query']['pages'].keys():

            page = data['query']['pages'][page_id]

            if 'extract' in page and 'title' in page:

                title = process_text(page['title'])
                extract = process_text(page['extract'])

                if len(title) > 0 and len(extract) > 0:
                    yield (title, extract)

if __name__ == '__main__':

    build_dataset()