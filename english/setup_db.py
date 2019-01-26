# create a sqlite db file with a cooc table (empty)

# usage python setup_db.py --model="my.sqlite"

import sqlite3
import argparse

param_model = 'arthur_c.sqlite'

def setup():
  global param_model
  parser = argparse.ArgumentParser()
  parser.add_argument('--model', help='the sqlite model for the ngram prominence (input and output)')
  args = parser.parse_args()
  param_model = args.model


def main():
  setup()
  print("Params: ")
  print("model: ", param_model)

  sql_cmd_create1 = """
create table prominence_n1(
word1 text,
cooc integer,
primary key(word1))
"""
  sql_cmd_create2 = """
create table prominence_n2(
word1 text, word2 text,
cooc integer,
primary key(word1, word2))
"""
  sql_cmd_create3 = """
create table prominence_n3(
word1 text, word2 text, word3 text,
cooc integer,
primary key(word1, word2, word3))
"""
  db = sqlite3.connect(param_model)
  cursor = db.cursor()
  cursor.execute(sql_cmd_create1)
  cursor.execute(sql_cmd_create2)
  cursor.execute(sql_cmd_create3)
  db.commit()

  print("Setup done.")

if __name__ == "__main__":
  main() 
