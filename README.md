# HTX xData Technical Test (Audio Transcriber)

## Table of Contents
- [Overview](#overview)
- [Repository Structure](#repository-structure)
- [Deployment](#deployment)
- [Setup Instructions](#setup-instructions)
- [Future Improvements](#future-improvements)
---

## Overview <a name="overview"></a>
This repository contains the solution for the HTX xData Technical Test. The goal is to build and deploy an Automatic Speech Recognition (ASR) service using the `wav2vec2-large-960h` model and integrate it with an Elasticsearch-backed search UI for querying transcribed audio data.

---

## Repository Structure 
```
 ├── asr 
 │ ├── asr_api.py # ASR microservice API 
 │ ├── cv-decode.py # Script to transcribe Common Voice dataset 
 │ ├── requirements.txt # Python dependencies 
 │ ├── Dockerfile # Containerization of ASR API
 │ ├── docker-compose.yml # ASR API container setup and run
 ├── deployment-design 
 │ ├── design.pdf # Proposed deployment architecture design 
 ├── elastic-backend 
 │ ├── cv-index.py # Script to index transcriptions into Elasticsearch 
 │ ├── docker-compose.yml # Elasticsearch cluster setup and run
 ├── search-ui 
 │ ├── Search UI React App # Search UI react application
 │ ├── Dockerfile # Containerization of Search UI Application
 │ ├── docker-compose.yml # Search UI configuration 
 ├── essay.pdf # Model monitoring pipeline and model drift tracking 
 ├── .gitignore 
 ├── docker-compose.yml # script to deploy all 3 services: ASR, Elastic Backend, Search UI
 ├── README.md # Documentation
 ├── requirements.txt # requirements of python files
```

---

## Deployment
This Solution is deployed on Azure(Free Tier) @ [Deployment Url](http://20.6.34.185/) following the architecture indicated in ```/deployment-design/design.pdf```.

---

## Setup Instructions
### Prerequisites
Ensure you have the following installed:
- Python 3.8+
- Docker & Docker Compose
- Git

### Clone the Repository
```sh
git clone https://github.com/Hsinkai2000/AudioTranscriber.git
cd AudioTranscriber
```

### Installing dependencies
```sh
pip install -r requirements.txt
```

### Environment Variable
Create a .env file in the root directory with the following two environment variables.
```
CSV_FILE_PATH="PATH_TO_COMMON_VOICE_DIR/cv-valid-dev.csv"
AUDIO_FILE_PATH="PATH_TO_COMMON_VOICE_DIR/cv-valid-dev"
```

### Run services
Run all 3 services with a single command.
```sh
  docker-compose up -d
  docker ps
```
You should see 4 docker containers running. audiotranscriber-asr-api-1, audiotranscriber-search-ui-1, audiotranscriber-es01-1 and audiotranscriber-es02-1.

### Test ASR-API
```sh
curl -X GET "http://localhost:8001/ping"
```
You should get a pong message as response.

### Test ElasticSearch
```sh
curl -X GET "http://localhost:9200/_nodes"
```
You should get the following response.
```response
    "_nodes": {
        "total": 2,
        "successful": 2,
        "failed": 0
    },
```
If any failure happen, you may have to change the amount of memory you allocate to this resource by changing ```ES_JAVA_OPTS``` in ```./docker-compose.yml```.
```docker-compose.yml
 - ES_JAVA_OPTS=-Xms[memory allocated]m -Xmx[memory allocated]m
```

### Transcribe Audio Files from CSV
You should have a ```cv-valid-dev-updated.csv``` file inside asr containing the generated text and duration of the audio file.
```sh
cd asr
python cv-decode.py
```

### Index updated 
This will index all 4075 rows in ```cv-valid-dev-updated.csv``` in the cv-transcriptions cluster.
```sh
cd ../elastic-backend
python cv-index.py
```

### Test Search UI
You may now test the Search UI by heading over to ```http://localhost:3000``` on your browser.

---

## Future Improvements 
1. Future improvements include moving away from scalable VM architecture and moving to serverless containers using kubernetes such as Azure Kubernetes Service (AKS). 
2. Improvements to the model using fine tuning and creating a pipeline to retrain continuously, looking out for common reliability issues like drift and anomalies.




