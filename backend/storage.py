import json
import os

#  JSON storage file for the blog posts
POSTS_FILE = "posts.json"

def load_posts():
    """Load the posts for Json file. Returns empty list if file doesnt exist"""
    if not os.path.exists(POSTS_FILE):
        return []
    with open(POSTS_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_posts(posts):
    """Saves the post into the Json File with formatting"""
    with open(POSTS_FILE, "w") as f:
        json.dump(posts, f, indent=2)
