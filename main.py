from fastapi import FastAPI, Request
import os
import requests

app = FastAPI()

CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]
REDIRECT_URI = os.environ["REDIRECT_URI"]

EXACT_AUTH_URL = "https://start.exactonline.nl/api/oauth2/auth"
EXACT_TOKEN_URL = "https://start.exactonline.nl/api/oauth2/token"

@app.get("/")
def home():
    login_url = (
        f"{EXACT_AUTH_URL}"
        f"?client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&response_type=code"
    )
    return {
        "message": "Welcome to your Exact Online test app!",
        "login_url": login_url
    }

@app.get("/callback")
def oauth_callback(request: Request):
    code = request.query_params.get("code")
    if not code:
        return {"error": "No code in request"}

    # 🔄 Exchange code for token
    token_response = requests.post(EXACT_TOKEN_URL, data={
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    })

    if token_response.status_code != 200:
        return {
            "error": "Token request failed",
            "status_code": token_response.status_code,
            "response": token_response.text
        }

    token_data = token_response.json()

    return {
        "message": "Successfully got access token!",
        "access_token": token_data.get("access_token"),
        "refresh_token": token_data.get("refresh_token"),
        "expires_in": token_data.get("expires_in")
    }




