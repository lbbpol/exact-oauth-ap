from fastapi import FastAPI, Request
import os  # To access environment variables
import uvicorn

# Load the app
app = FastAPI()

# ✅ Load secrets from environment variables (Render will provide these)
CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]
REDIRECT_URI = os.environ["REDIRECT_URI"]

# ✅ Base URL for Exact's OAuth flow
EXACT_AUTH_URL = "https://start.exactonline.nl/api/oauth2/auth"

@app.get("/")
def home():
    # Link to start OAuth login — Exact Online will redirect back to our /callback
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
    # When Exact redirects here, it'll include something like ?code=abc123
    code = request.query_params.get("code")
    return {
        "message": "Got the code from Exact!",
        "code": code
    }




