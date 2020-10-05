import sqlite3
import nltk
from rake_nltk import Rake, Metric
import nltk
from nltk.stem import WordNetLemmatizer
import re
nltk.download('punkt')
conn = sqlite3.connect('test.sqlite3')

from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))

pool =  []

for i in conn.execute('select distinct id, full_text from gp_search_new'):
    str(i[1]).replace("[^a-zA-Z]", " ") # remove non-letters
    str(i[1]).replace("\d+", " ") # remove numbers
    str(i[1]).replace(r'"', '') # remove quotation

    # Lemmatize list of words and join
    lemma = WordNetLemmatizer()
    text1_lemma= [lemma.lemmatize(x) for x in str(i[1])]

    try:
        if len(text1_lemma) > 10:
            # Keywords expraction by RAKE
            r = Rake(stopwords=None,
                     punctuations=None,
                     language="english",
                     ranking_metric=Metric.DEGREE_TO_FREQUENCY_RATIO,
                     max_length=50,
                     min_length=10)
            r.extract_keywords_from_text(text1_lemma)
            # Append patent's id column
            pool.append((i[0], r.get_ranked_phrases_with_scores()) )
    except:
        pass

for i in pool:
    print(i)
        
import json

with open('piority.json', 'w') as json_file:
    json.dump(priority, json_file)





