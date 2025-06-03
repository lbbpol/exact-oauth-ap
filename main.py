from fastapi import FastAPI, Request
import os
import requests

app = FastAPI()

# 🔐 Load secrets from environment (from Render)
CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]
REDIRECT_URI = os.environ["REDIRECT_URI"]

# 🔗 Exact Online OAuth URLs
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

    # Exchange code for access token
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
    access_token = token_data.get("access_token")

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json"
    }

    # Get division ID
    me_response = requests.get("https://start.exactonline.nl/api/v1/current/Me", headers=headers)
    if me_response.status_code != 200:
        return {
            "error": "Could not fetch /Me",
            "response": me_response.text
        }
    me_data = me_response.json()
    division = me_data["d"]["results"][0]["CurrentDivision"]

    return {
        "message": "Login successful",
        "access_token": access_token,
        "division": division
    }

@app.get("/fetch/{endpoint_path:path}")
def fetch_any_endpoint(request: Request, endpoint_path: str):
    access_token = request.query_params.get("token")
    division = request.query_params.get("division")
    
    if not access_token or not division:
        return {"error": "Missing token or division"}

    url = f"https://start.exactonline.nl/api/v1/{division}/{endpoint_path}"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return {
            "error": "Exact API call failed",
            "url": url,
            "status_code": response.status_code,
            "response": response.text
        }

    return {
        "resource": endpoint_path,
        "data": response.json()
    }
