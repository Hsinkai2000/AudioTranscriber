from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk
import pandas as pd
import os
from dotenv import load_dotenv
import numpy as np

load_dotenv()
INDEX_NAME = "cv-transcriptions"


def create_index(client):
    mappings = {
        "properties": {
            "filename": {"type": "text"},
            "text": {"type": "text"},
            "up_votes": {"type": "integer"},
            "down_votes": {"type": "integer"},
            "gender": {"type": "keyword",
                       "fields": {
                           "keyword": {
                               "type": "keyword"
                           }
                       }},
            "age": {"type": "keyword",
                    "fields": {
                        "keyword": {
                            "type": "keyword"
                        }
                    }},
            "accent": {"type": "keyword",
                       "fields": {
                           "keyword": {
                               "type": "keyword"
                           }
                       }},
            "duration": {"type": "float",
                         "fields": {
                             "keyword": {
                                 "type": "keyword"
                             }
                         }},
            "generated_text": {
                "type": "text",
                "fields": {
                    "suggest": {
                        "type": "search_as_you_type"
                    }
                }
            },
        }
    }

    client.indices.create(
        index=INDEX_NAME,
        mappings=mappings,
        ignore=400  # ignore 400 already exists code
    )


def generate_actions(client):
    df = pd.read_csv("../asr/cv-valid-dev-updated.csv")
    for index, row in df.iterrows():
        doc = row.to_dict()
        # Convert NaN values to strings
        for key, value in doc.items():
            if isinstance(value, float) and np.isnan(value):
                doc[key] = None
        client.index(index=INDEX_NAME, document=doc)


def main():
    client = Elasticsearch("http://127.0.0.1:9200/")
    create_index(client)
    generate_actions(client)


if __name__ == "__main__":
    main()
