import pandas as pd
import requests
import os
from dotenv import load_dotenv

# Variables
load_dotenv()
API_URL = "http://localhost:8001/asr"

df = pd.read_csv(os.getenv("CSV_FILE_PATH"))

# Loop through all rows in file
for index, row in df.iterrows():

    # Obtain audio file path
    curr_audio_file_path = os.path.join(
        os.getenv("AUDIO_FILE_PATH"), row['filename'])

    # Read Audio file and make request to /asr endpoint
    with open(curr_audio_file_path, "rb") as audio_file:
        response = requests.post(API_URL, files={"file": audio_file})

    # Add duration to duration column
    df.loc[index, "duration"] = float(response.json()["duration"])
    # Append new col 'generated_text' at the end
    df.loc[index, "generated_text"] = response.json()["transcription"]
    print(f'reading row no. {index}')
# Save final file to current dir
df.to_csv("cv-valid-dev-updated.csv", index=False)
