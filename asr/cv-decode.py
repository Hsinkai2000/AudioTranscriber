import pandas as pd
import requests
import os
from dotenv import load_dotenv

# Variables
load_dotenv()
API_URL = "http://localhost:8001/asr"

df = pd.read_csv(os.getenv("CSV_FILE_PATH"))

for index, row in df.iterrows():
    curr_audio_file_path = os.path.join(
        os.getenv("AUDIO_FILE_PATH"), row['filename'])
    with open(curr_audio_file_path, "rb") as audio_file:
        response = requests.post(API_URL, files={"file": audio_file})
    df.loc[index, "generated_text"] = response.json()["transcription"]

df.to_csv("cv-valid-dev-updated.csv", index=False)
