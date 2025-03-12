from fastapi import FastAPI, File, UploadFile
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC

import torch
import io
import soundfile as sf
from scipy import signal

# Variables
model_name = "facebook/wav2vec2-large-960h"

# Initialise FastAPI Server
app = FastAPI()

# load model and processor
processor = Wav2Vec2Processor.from_pretrained(model_name)
model = Wav2Vec2ForCTC.from_pretrained(model_name)


# Endpoint: GET /ping
# Simple server healthcheck
# Input: nil
# Returns: "pong" if healthcheck passes

@app.get("/ping")
def testPing():
    return {"message": "pong"}


# Endpoint: POST /asr
# Transcribes audio files to text
# Required input: Audio file sampled at 16kHz
# Returns: Transcription text and audio duration

@app.post("/asr")
async def transcribe_audio(file: UploadFile):
    # Read uploaded file and retreive audio and samplerate
    audio_bytes = io.BytesIO(await file.read())
    audio, samplerate = sf.read(audio_bytes)

    # check if samplerate is 16kHz, if not, resample to 16kHz
    if samplerate != 16000:
        audio = signal.resample(audio, int(len(audio) * 16000 / samplerate))
        samplerate = 16000

    input_values = processor(audio, sampling_rate=samplerate,
                             return_tensors="pt", padding="longest").input_values
    with torch.no_grad():
        logits = model(input_values).logits
        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = processor.batch_decode(predicted_ids)[0]

    duration = len(audio) / samplerate

    return {"transcription": transcription, "duration": str(duration)}
