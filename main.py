#!/usr/bin/env python3
"""Build an in-memory inverted index over text files and search it."""
import argparse
import os
import re
import tempfile
from collections import defaultdict

TOKEN_RE = re.compile(r"[A-Za-z0-9']+")

def tokenize(text: str):
    return [token.lower() for token in TOKEN_RE.findall(text)]

class InvertedIndex:
    def __init__(self):
        self.index = defaultdict(set)
        self.documents = {}

    def add_document(self, path: str, text: str) -> None:
        self.documents[path] = text
        for token in set(tokenize(text)):
            self.index[token].add(path)

    def add_directory(self, directory: str) -> int:
        count = 0
        for name in sorted(os.listdir(directory)):
            path = os.path.join(directory, name)
            if os.path.isfile(path) and name.lower().endswith((".txt", ".md", ".rst")):
                with open(path, encoding="utf-8", errors="ignore") as fh:
                    self.add_document(path, fh.read())
                count += 1
        return count

    def search(self, query: str, mode: str = "and"):
        """Return matching document paths; mode is 'and' or 'or'."""
        terms = tokenize(query)
        if not terms:
            return []
        sets = [self.index.get(term, set()) for term in terms]
        if mode == "and":
            result = set.intersection(*sets) if sets else set()
        else:
            result = set.union(*sets) if sets else set()
        return sorted(result)

    def stats(self):
        postings = sum(len(paths) for paths in self.index.values())
        return len(self.documents), len(self.index), postings

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dir", help="directory of .txt/.md files to index")
    parser.add_argument("--query", help="search terms (default: AND)")
    parser.add_argument("--or", dest="mode", action="store_const", const="or", default="and")
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()

    if args.demo:
        with tempfile.TemporaryDirectory() as tmp:
            samples = {
                "alpha.txt": "the quick brown fox jumps over the lazy dog",
                "beta.txt": "a quick brown dog outpaces a quick fox",
                "gamma.txt": "lazy afternoons are for sleeping dogs",
            }
            for name, text in samples.items():
                with open(os.path.join(tmp, name), "w", encoding="utf-8") as fh:
                    fh.write(text)
            index = InvertedIndex()
            index.add_directory(tmp)
            docs, terms, postings = index.stats()
            print(f"indexed {docs} documents, {terms} unique terms, {postings} postings")
            for query, mode in (("quick fox", "and"), ("quick dog", "and"),
                                ("sleeping fox", "or"), ("lazy", "and")):
                hits = index.search(query, mode)
                print(f"search '{query}' ({mode.upper()}): {[os.path.basename(h) for h in hits]}")
        return

    if not args.dir:
        raise SystemExit("--dir is required (or use --demo)")
    index = InvertedIndex()
    count = index.add_directory(args.dir)
    print(f"indexed {count} files: {index.stats()[1]} unique terms")
    query = args.query or input("search query: ")
    for path in index.search(query, args.mode):
        print(path)

if __name__ == "__main__":
    main()
