# create a sqlite db

import sqlite3

sql_cmd_create = "create table cooc(word1 text primary key, word2 text primary key, cooc integer)"

db = sqlite3.connect('arthur_c.sqlite')
cursor = db.cursor()
cursor.execute(sql_cmd_create)
db.commit()


# word processing

import nltk
nltk.download('punkt')
a1 = '''I used to believe in forever, but forever's too good to be true.'''
nltk.word_tokenize(a1)

a2 = "Sun rises in the east? Sun sets in the west."
nltk.sent_tokenize(a2)


# download the corpus
wget http://www.gutenberg.org/cache/epub/1597/pg1597.txt


# build the model
python setup_db.py --model="arthur_c.sqlite"
python build_model_incremental.py --model=arthur_c.sqlite --corpus="corpus/andersen.txt"

# start a jupyter notebook
jupyter notebook --ip 0.0.0.0 --port 8000 --no-browser

# connect:
http://ec2-18-202-174-17.eu-west-1.compute.amazonaws.com:8000

