from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from api_v1 import v1
from backend.storage import load_posts, save_posts  # <--- NEU

app = Flask(__name__)

CORS(app, methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["5 per minute"]
)

app.register_blueprint(v1)

@app.route("/api/posts", methods=["GET"])
def get_posts():
    sort_field = request.args.get("sort")
    direction = request.args.get("direction")

    valid_fields = ["title", "content"]
    valid_directions = ["asc", "desc"]

    posts = load_posts()
    sorted_posts = posts.copy()

    if sort_field:
        if sort_field not in valid_fields:
            return jsonify({
                "error": f"Invalid sort field '{sort_field}'. Must be 'title' or 'content'."}), 400

        reverse = False
        if direction:
            if direction not in valid_directions:
                return jsonify(
                    {"error": f"Invalid direction '{direction}'. Must be 'asc' or 'desc'."}), 400
            reverse = (direction == "desc")

        sorted_posts.sort(key=lambda post: post[sort_field].lower(), reverse=reverse)

    return jsonify(sorted_posts)


@app.route('/api/posts', methods=['POST'])
def add_post():
    data = request.get_json()

    if not data.get('title') or not data.get('content'):
        return jsonify({"error": "Title and content are required"}), 400

    posts = load_posts()
    new_id = len(posts) + 1
    new_post = {
        "id": new_id,
        "title": data["title"],
        "content": data["content"]
    }

    posts.append(new_post)
    save_posts(posts)

    return jsonify(new_post), 201


@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    posts = load_posts()

    post_to_delete = next((post for post in posts if post["id"] == id), None)

    if post_to_delete:
        posts.remove(post_to_delete)
        save_posts(posts)
        return jsonify({"message": f"Post with id {id} has been deleted successfully."}), 200
    else:
        return jsonify({"message": "Post not found."}), 404


@app.route('/api/posts/<int:id>', methods=['PUT'])
def update_post(id):
    posts = load_posts()

    post_to_update = next((post for post in posts if post["id"] == id), None)

    if not post_to_update:
        return jsonify({"message": "Post not found"}), 404

    data = request.get_json()
    post_to_update["title"] = data.get("title", post_to_update["title"])
    post_to_update["content"] = data.get("content", post_to_update["content"])

    save_posts(posts)

    return jsonify(post_to_update), 200


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    title_query = request.args.get('title', '').lower()
    content_query = request.args.get('content', '').lower()

    if not title_query and not content_query:
        return jsonify([])

    posts = load_posts()

    filtered_posts = [
        post for post in posts
        if (title_query and title_query in post['title'].lower()) or
           (content_query and content_query in post['content'].lower())
    ]

    return jsonify(filtered_posts)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
