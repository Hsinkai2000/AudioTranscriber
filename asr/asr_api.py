from fastapi import FastAPI

app = FastAPI()

# Simple health check endpoint
# GET /ping returns a "pong" message to verify the API is running


@app.get("/ping")
def testPing():
    return {"message": "pong"}
