from fastapi import FastAPI, HTTPException
import instaloader
from decouple import config

app = FastAPI()

async def get_followers(username):
    L = instaloader.Instaloader()
    # Login using your Instagram username and password
    L.login("robsonbot", "Fr00ty")
    profile = instaloader.Profile.from_username(L.context, username)
    followers = []
    for follower in profile.get_followers():
        # Extract the username directly (no await needed)
        followers.append(follower.username)
    return followers

@app.get("/followers/{username}")
async def read_followers(username: str):
    try:
        followers = await get_followers(username)
        return {"followers": followers}
    except instaloader.exceptions.ProfileNotExistsException:
        raise HTTPException(status_code=404, detail="Profile not found")
    except instaloader.exceptions.LoginRequiredException:
        raise HTTPException(status_code=401, detail="Login failed. Please check your credentials.")
