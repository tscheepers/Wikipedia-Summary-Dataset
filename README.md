Wikipedia Summary Dataset
======

This is a dataset that can be used for research into machine learning and natural language processing. It contains all titles and summaries (or introductions) of English Wikipedia articles, extracted in *september of 2017*.

The dataset is different from the [wikipedia dump](https://dumps.wikimedia.org/backup-index.html) datasets and different from the datasets that can be created by [gensim](http://textminingonline.com/training-word2vec-model-on-english-wikipedia-by-gensim) because ours contains the extracted summaries and not the entire unprocessed page body. This could be useful if one wants to use the smaller, more concise, and more definitional summaries in their research. Or if one just wants to use a smaller but still diverse dataset for efficient training with resource constraints.

A summary or introduction of an article is everything starting from the page title up to the content outline.

![Wikipedia Summary Example](https://user-images.githubusercontent.com/44893/31073372-f02d4384-a76b-11e7-909f-1e3769b3b9d0.png)

The raw dataset leaves the original text structure intact. Additionally, we provide pre-processed versions.

File | Tokenized | Lowercased | No Punctuation | No stop words | Stemmed
--- | --- | --- | --- | --- | ---
[*raw.tar.gz*](https://blob.thijs.ai/wiki-summary-dataset/raw.tar.gz) |  |  |  |  |  |
[*tokenized.tar.gz*](https://blob.thijs.ai/wiki-summary-dataset/tokenized.tar.gz) | ✓ |  |  |  |  |
[*lowercased.tar.gz*](https://blob.thijs.ai/wiki-summary-dataset/lowercased.tar.gz) | ✓ | ✓ |  |  |  |
[*without-punctuation.tar.gz*](https://blob.thijs.ai/wiki-summary-dataset/without-punctuation.tar.gz) | ✓ | ✓ | ✓ |  |  |
[*without-stop-words.tar.gz*](https://blob.thijs.ai/wiki-summary-dataset/without-stop-words.tar.gz) | ✓ | ✓ | ✓ | ✓ |  |
[*stemmed.tar.gz*](https://blob.thijs.ai/wiki-summary-dataset/stemmed.tar.gz) | ✓ | ✓ | ✓ | ✓ | ✓ |

Download
-----

- [*raw.tar.gz*](https://blob.thijs.ai/wiki-summary-dataset/raw.tar.gz) (± 1GB)
- [*tokenized.tar.gz*](https://blob.thijs.ai/wiki-summary-dataset/tokenized.tar.gz) (± 1GB)
- [*lowercased.tar.gz*](https://blob.thijs.ai/wiki-summary-dataset/lowercased.tar.gz) (± 1GB)
- [*without-punctuation.tar.gz*](https://blob.thijs.ai/wiki-summary-dataset/without-punctuation.tar.gz) (± 1GB)
- [*without-stop-words.tar.gz*](https://blob.thijs.ai/wiki-summary-dataset/without-stop-words.tar.gz) (± 1GB)
- [*stemmed.tar.gz*](https://blob.thijs.ai/wiki-summary-dataset/stemmed.tar.gz) (± 1GB)

Dataset construction
-----

The dataset was constructed using a script that calls Wikipedia API for every page with their `page_id`. This API call used the [TextExtracts](https://www.mediawiki.org/wiki/Extension:TextExtracts) extension to create the summaries or introductions.

```
https://en.wikipedia.org/w/api.php?format=json&maxlag=5&action=query&prop=extracts&exintro=&explaintext=&pageids=123|456|789
```

The results from all these calls are then combined into two big files. A `.txt` file containing all the article titles and their respective summaries separated by `|||`. Every line in the document represents a wikipedia article. Example from `tokenized.txt`:

```
Anarchism ||| Anarchism is a political philosophy that advocates self-governed societies based on voluntary…
Autism ||| Autism is a neurodevelopmental disorder characterized by impaired social interaction , impaired verbal…
Albedo ||| Albedo ( ) is a measure for reflectance or optical brightness ( Latin albedo , `` whiteness '' ) of…
…
```

As well as a `.vocab` file which contains the vocabulary and the count of each token. Example from `tokenized.vocab`:

```
, 27222735
the 25505452
. 21555700
of 16267241
in 13313133
and 12630336
a 10202887
is 7770405
) 7460943
( 7459977
…
```

Scripts to create the dataset are provided in this repository. They require a local Wikipedia installation and access to its MySQL database to get the page identifiers (`page_id`). Additionally we would ask you not to build the dataset yourself if this is not needed, since building the dataset would require calling the Wikipedia API for every page and this puts strain on their API. **Please respect the `maxlag=5` parameter.**

