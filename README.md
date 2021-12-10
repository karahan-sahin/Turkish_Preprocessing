# Turkish Preprocessing Toolkit

This repository includes the modules of preprocessing operations for Turkish text data. The modules are implemented for the general domain text data. The modules include

- Sentence Splitting (Sentence Boundary Disambiguation)
- Tokenization
- Normalization
- Stemming
- Stopword Removal
- Also a handwritten Naive Bayes Classifier for any use

## Requirements

First, you need to clone this repository to your project from your terminal and have the necessary Python version which is `__version__ >= 3.6`

```bash
git clone git@github.com:karahan-sahin/Turkish_Preprocessing.git
```

After cloning the repository, you need to initiate your `virtualenv` and load the necessary package

```bash
cd Turkish_Preprocessing/
python -m venv toolkit_venv
source toolkit_venv/bin/activate
pip install -r requirements.txt
```

After that you can go to the initial folder contains the repository folder and use it on your notebook or script 

```bash
cd ..
mv Turkish_Preprocessing/example/demo.ipynb -t .
```



## Usage

Create sample text for the usage which can be also `demo.ipynb`

```python
sample_text = """...politika faizi olan bir hafta vadeli repo ihale faiz oranının yüzde 16’dan yüzde 15’e indirilmesine karar vermiştir. Küresel iktisadi..."""
```

### Tokenization

```python
from Turkish_Preprocessing.modules.tokenizer import Tokenizer
tokenizer = Tokenizer()
```

After you import your module, you need the initiate the instance of the tokenizer. In this processes, the necessary models will be trained. Then you can either use `RuleBasedTokenizer` which is tokenizer that uses handwritten and non-overlapping set of rules.

```python
tokens = tokenizer.RuleBasedTokenizer(sample_text)
```

`RuleBasedTokenizer` also includes normalization rules for Multi-Word Expression and other normalization method

or `LogisticTokenizer` which is trained char-by-char binary Logistic Regression classifier which detects a char to be a end-of-token or not

```python
tokens = tokenizer.LogisticTokenizer(sample_text)
```

---------------

### Sentence Splitting

```python
from Turkish_Preprocessing.modules.splitter import SentenceSplitter
splitter = SentenceSplitter()
```

Sentence Splitter also contains one rule based and one machine learning based (a Naive Bayes classifier) which detects a punctuation to be a sentence boundary punctuation or not

```python
sentences = splitter.RuleBasedTokenizer(sample_text)
```

```python
sentences = tokenizer.NaiveBayesSplitter(sample_text)
```

______

### Normalization

Normalization module for normalization of newlines, multiwords and other special tokens

```python
from Turkish_Preprocessing.modules.normalization import Normalization
normalization = Normalization()
```

```python
normalized_text = normalization.normalize(sample_text)
```

Has multiple attributes as 

```python
normalization.normalize_abbreviation()
normalization.adapt_newline()
normalization.normalize_urls()
normalization.normalize_emails()
normalization.normalize_hashtags()
normalization.remove_punctuation()
normalization.MWE_Normalization()
```

-----------

### Stemmer

Stemmer works with only in token base you need to give token by token to get the stems and the detect list of morphology. Stemmer has created using the regular expression which are obtained from *Universal Dependencies* framework.

```python
from Turkish_Preprocessing.modules.stemmer import Stemmer
stemmer = Stemmer()
```

```python
stems, morphs = stemmer.get_stem(token)
```

#### Sample Output

```json
{
	Token: "etmektedir",
	Stem: "et",
	Morphology:  ['Copula=GenCop', 'Case=Loc', 'PersonNumber=V1pl', 'Polarity=Neg']
}
```

----

### Stopword Removal

Has a both dynamic approach from corpus where top_k words and frozen lexicon from `nltk.stopwords` can be selected.


```python
from Turkish_Preprocessing.modules.stopwords import StopwordRemoval
stopword = StopwordRemoval("custom", top_k=100)
stopword = StopwordRemoval("lexicon")
```

```python
tokens = stopword.remove(tokenized_text)
```

