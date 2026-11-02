# Inverted index

**Category:** Data Structures

## Problem

An Inverted Index is a data structure used to create full text search. Given a set of text files, implement a program to create an inverted index. Also create a user interface to do a search using that inverted index which returns a list of files that contain the query term / terms. The search index can be in memory.

## Solution

Tokenizes documents with a case-insensitive word regex, maps each unique term to the set of files containing it, and answers multi-term queries by set intersection (AND) or union (OR). Posting lists are deduplicated per document, so repeated words do not bloat the index.

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py --dir ./docs --query "quick fox"
python3 main.py --dir ./docs --query "sleeping fox" --or
python3 main.py --demo
```

## Example

```text
indexed 3 documents, 15 unique terms, 20 postings
search 'quick fox' (AND): ['alpha.txt', 'beta.txt']
search 'quick dog' (AND): ['alpha.txt', 'beta.txt']
search 'sleeping fox' (OR): ['alpha.txt', 'beta.txt', 'gamma.txt']
search 'lazy' (AND): ['alpha.txt', 'gamma.txt']
```

## Attribution

The problem statement is from [karan/Projects](https://github.com/karan/Projects), a list of practical projects that anyone can solve in any programming language (MIT License, Copyright (c) 2013 Karan Goel). The Python solution in this repository was implemented by [bspreston-esq](https://github.com/bspreston-esq).

This repository is part of the [Projects-Python-All](https://github.com/bspreston-esq/Projects-Python-All) collection.
