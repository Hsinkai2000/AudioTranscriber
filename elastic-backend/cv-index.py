from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk
import pandas as pd
import os
from dotenv import load_dotenv
import numpy as np

load_dotenv()
INDEX_NAME = "cv-transcriptions"


def generate_actions(client):
    df = pd.read_csv("../asr/cv-valid-dev-updated.csv")
    for index, row in df.iterrows():
        doc = row.to_dict()
        # Convert NaN values to strings
        for key, value in doc.items():
            if isinstance(value, float) and np.isnan(value):
                doc[key] = None  # Or another suitable replacement like "null"
        client.index(index=INDEX_NAME, document=doc)


def main():
    client = Elasticsearch("http://127.0.0.1:9200/")
    generate_actions(client)


if __name__ == "__main__":
    main()
