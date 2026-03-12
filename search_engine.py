import json
import re
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def load_index():
    with open("inverted_index.json", "r") as f:
        inverted_index = json.load(f)

    with open("idf.json", "r") as f:
        idf = json.load(f)

    return inverted_index, idf



def tokenize_query(query):

    query = query.lower()

    query = re.sub(r"[^\w\s]", "", query)

    tokens = query.split()

    return tokens



def search_documents(tokens, inverted_index, idf):

    scores = {}

    for token in tokens:

        if token in inverted_index:

            postings = inverted_index[token]

            word_idf = idf.get(token, 0)

            for doc, tf in postings:

                score = tf * word_idf

                if doc not in scores:
                    scores[doc] = 0

                scores[doc] += score

    return scores



def rank_results(scores, top_n=10):

    ranked = sorted(
        scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return ranked[:top_n]



inverted_index, idf = load_index()




app = FastAPI()

# ENABLE CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  #allow all origins (you can specify specific domains if needed)
    allow_credentials=True,  #allow credentials (cookies, authorization headers, etc.)
    allow_methods=["*"],  #allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  #allow all headers (Content-Type, Authorization, etc.)
)



@app.get("/search")
def search(q: str):

    tokens = tokenize_query(q)

    scores = search_documents(tokens, inverted_index, idf)

    ranked = rank_results(scores)

    results = []

    for doc, score in ranked:

        results.append({
            "document": doc,
            "score": score
        })

    return results