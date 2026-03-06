import os
import math
import json
import string
from collections import defaultdict, Counter
from bs4 import BeautifulSoup


PAGES_DIR = "pages"


def load_documents(directory):
    files = [f for f in os.listdir(directory) if f.endswith(".html")]
    print(f"Total documents found: {len(files)}")
    return files #files is a list of all html pages saved 


def extract_visible_text(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        soup = BeautifulSoup(f, "html.parser")

        
        for tag in soup(["script", "style"]):
            tag.decompose()

        text = soup.get_text(separator=" ")
        return text #clean text is returned from all html tags


def tokenize(text):
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    tokens = text.split()
    return tokens # list of individual words

#term frequency
def compute_term_frequency(tokens):
    return Counter(tokens)


def build_inverted_index(documents_tf):
    inverted_index = defaultdict(list)

    for doc_id, term_freq in documents_tf.items():
        for word, freq in term_freq.items():
            inverted_index[word].append((doc_id, freq))

    return inverted_index


def save_inverted_index(index, filename="inverted_index.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)


#inverse document frequency #how rare is the word
def compute_idf(inverted_index, total_documents):
    idf = {}

    for word, doc_list in inverted_index.items():
        document_frequency = len(doc_list)
        idf[word] = math.log(total_documents / document_frequency)

    return idf
#high idf more important the world rare world

def save_idf(idf_dict, filename="idf.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(idf_dict, f, indent=2)


def validate_index(inverted_index, idf_dict, total_documents):
    print("\nIndexing Complete!")
    print("Total documents indexed:", total_documents)
    print("Total unique terms:", len(inverted_index))

    sample_words = list(inverted_index.keys())[:5] #first 5 words

    print("\nSample Inverted Index Entries:")
    for word in sample_words:
        print(word, "->", inverted_index[word])

    print("\nSample IDF Values:")
    for word in sample_words:
        print(word, "->", idf_dict[word])


def main():
    files = load_documents(PAGES_DIR)
    total_documents = len(files)

    documents_tf = {}

    for filename in files:
        file_path = os.path.join(PAGES_DIR, filename)

        text = extract_visible_text(file_path)
        tokens = tokenize(text)
        term_freq = compute_term_frequency(tokens)

        documents_tf[filename] = term_freq

    inverted_index = build_inverted_index(documents_tf)
    save_inverted_index(inverted_index)

    idf = compute_idf(inverted_index, total_documents)
    save_idf(idf)

    validate_index(inverted_index, idf, total_documents)


if __name__ == "__main__":
    main()