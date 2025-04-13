from flask import Blueprint, jsonify, request
from flask_cors import CORS
from backend.storage import load_posts, save_posts  # <--- NEU

# API Version number 1
v1 = Blueprint('v1', __name__, url_prefix='/api/v1')

CORS(v1, methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])

@v1.route("/posts", methods=["GET"])
def get_posts():
    """Gets all posts with the option of sorting."""
    sort_field = request.args.get("sort")
    direction = request.args.get("direction")

    valid_fields = ["title", "content"]
    valid_directions = ["asc", "desc"]

    posts = load_posts()

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

        posts.sort(key=lambda post: post[sort_field].lower(), reverse=reverse)

    return jsonify(posts)


@v1.route('/posts', methods=['POST'])
def add_post():
    """Creates a new post. Title AND Content are required here."""
    data = request.get_json()

    if not data.get('title') or not data.get('content'):
        return jsonify({"error": "Title and content are required"}), 400

    posts = load_posts()
    new_id = max([post["id"] for post in posts], default=0) + 1

    new_post = {
        "id": new_id,
        "title": data["title"],
        "content": data["content"]
    }

    posts.append(new_post)
    save_posts(posts)

    return jsonify(new_post), 201


@v1.route('/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    """Deletes a post you choose by its unique ID"""
    posts = load_posts()
    post_to_delete = next((post for post in posts if post["id"] == id), None)

    if post_to_delete:
        posts.remove(post_to_delete)
        save_posts(posts)
        return jsonify({"message": f"Post with id {id} has been deleted successfully."}), 200
    else:
        return jsonify({"message": "Post not found."}), 404


@v1.route('/posts/<int:id>', methods=['PUT'])
def update_post(id):
    """Updates an existing post partially or completly."""
    posts = load_posts()
    post_to_update = next((post for post in posts if post["id"] == id), None)

    if not post_to_update:
        return jsonify({"message": "Post not found"}), 404

    data = request.get_json()
    post_to_update["title"] = data.get("title", post_to_update["title"])
    post_to_update["content"] = data.get("content", post_to_update["content"])

    save_posts(posts)
    return jsonify(post_to_update), 200


@v1.route('/posts/search', methods=['GET'])
def search_posts():
    """Searches a post via keywords in title and / or content. Not case sensitive."""
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
