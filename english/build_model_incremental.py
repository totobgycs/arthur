# Take a text corpus and a model in sqlite and update the model with the text corpus

# TODO:
# Don't depend on line ends being sentence ends
# Clenup: sentence preprocessing: skip the risky ones
# Add a meta-word to mark the beginning of a sentence
# Process trigrams too

import argparse
import sqlite3
import nltk


param_dryrun = True
param_verbose = False

param_corpus = 'text_corpus.txt'
param_model = 'arthur_c.sqlite'

param_alpha = 0.01


def setup():
  global param_model
  global param_corpus
  parser = argparse.ArgumentParser()
  parser.add_argument('--model', help='the sqlite model for the coocurrence (input and output)')
  parser.add_argument('--corpus', help='the text corpus (input)')
  args = parser.parse_args()
  # TODO: validation
  param_model = args.model
  param_corpus = args.corpus

def process_ngram1(pos, sentence):
  n = 1
  word1 = sentence[pos]
  word1 = word1.upper()

  # read the unigram
  sql_cmd = 'select word1, cooc from prominence_n1 where word1 = ?'
  sql_cmd_bindings = (word1,)
  cursor.execute(sql_cmd, sql_cmd_bindings)
  rec = cursor.fetchall()
  # compute new weights
  if not rec:
    c = 1 * param_alpha
    sql_cmd = 'INSERT INTO prominence_n1(word1, cooc) VALUES(?, ?)'
    sql_cmd_bindings=(word1, c)
  else:
    oldc = rec[0][n]
    c = oldc * (1 - param_alpha) + 1 * param_alpha
    sql_cmd = 'UPDATE prominence_n1 set cooc = ? WHERE word1 = ?'
    sql_cmd_bindings=(c, word1)
  # update the unigram
  cursor.execute(sql_cmd, sql_cmd_bindings)
  if param_verbose:
    print("Updated unigram: {w1}".format(w1=word1))
  db.commit()
   

def process_ngram2(pos, sentence):
  n = 2
  # if this is the last word, there is nothing to do
  if pos == len(sentence) - 1:
    return
  word1 = sentence[pos]
  word2 = sentence[pos + 1]
  word1 = word1.upper()
  word2 = word2.upper()

  # read the bigram
  sql_cmd = 'select word1, word2, cooc from prominence_n2 where word1 = ? and word2 = ?'
  sql_cmd_bindings = (word1, word2)
  cursor.execute(sql_cmd, sql_cmd_bindings)
  rec = cursor.fetchall()
  # compute new weights
  if not rec:
    c = 1 * param_alpha
    sql_cmd = 'INSERT INTO prominence_n2(word1, word2, cooc) VALUES(?, ?, ?)'
    sql_cmd_bindings=(word1, word2, c)
  else:
    oldc = rec[0][n]
    c = oldc * (1 - param_alpha) + 1 * param_alpha
    sql_cmd = 'UPDATE prominence_n2 set cooc = ? WHERE word1 = ? and word2 = ?'
    sql_cmd_bindings=(c, word1, word2)
  # update the bigram
  cursor.execute(sql_cmd, sql_cmd_bindings)
  if param_verbose:
    print("Updated bigram: {w1}, {w2}".format(w1=word1,w2=word2))
  db.commit()
   

def process_corpus():
  with open(param_corpus) as infile:
    for line in infile:
      for sentence in nltk.sent_tokenize(line):
        tokenized_sentence = nltk.word_tokenize(sentence)
        for pos, word in enumerate(tokenized_sentence):
          process_ngram1(pos, tokenized_sentence)
          process_ngram2(pos, tokenized_sentence)
  print("Done processing corpus")


def print_unigram_stats():
  n = 1
  print("Top prominances:")
  sql_cmd = 'select word1, cooc from prominence_n1 order by cooc desc limit 20'
  records = cursor.execute(sql_cmd)
  for record in records:
    print("{w1}\t : {c}".format(w1=record[0], c=record[n]))


def print_bigram_stats():
  n = 2
  print("Top co-occurrances:")
  sql_cmd = 'select word1, word2, cooc from prominence_n2 order by cooc desc limit 20'
  records = cursor.execute(sql_cmd)
  for record in records:
    print("{w1}\t-\t{w2}\t : {c}".format(w1=record[0], w2=record[1], c=record[n]))


def main():
  setup()
  print("Params: ")
  print("alpha: ", param_alpha)
  print("text_corpus: ", param_corpus)
  print("model: ", param_model)

  global db
  db = sqlite3.connect(param_model)
  global cursor
  cursor = db.cursor()
  
  process_corpus()

  print_unigram_stats()
  print_bigram_stats()

  print("Done")

if __name__ == "__main__":
  main()


