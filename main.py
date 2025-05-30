from fastapi import FastAPI, Request  # FastAPI = website backend, Request = get info from URL
import uvicorn  # Runs the app

app = FastAPI()  # Create the app

@app.get("/")  # When someone goes to the homepage
def home():
    return {"message": "Welcome to your Exact Online test app!"}

@app.get("/callback")  # This handles the redirect from Exact
def oauth_callback(request: Request):
    code = request.query_params.get("code")  # Get the ?code=... from the URL
    return {"message": "Got the code from Exact!", "code": code}



