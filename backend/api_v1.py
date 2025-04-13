from flask import Blueprint, jsonify, request

v1 = Blueprint('v1', __name__, url_prefix='/api/v1')

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]

@v1.route("/posts", methods=["GET"])
def get_posts():
    sort_field = request.args.get("sort")
    direction = request.args.get("direction")

    valid_fields = ["title", "content"]
    valid_directions = ["asc", "desc"]

    sorted_posts = POSTS.copy()

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


@v1.route('/posts', methods=['POST'])
def add_post():
    data = request.get_json()

    if not data.get('title') or not data.get('content'):
        return jsonify({"error": "Title and content are required"}), 400

    new_id = len(POSTS) + 1
    new_post = {
        "id": new_id,
        "title": data["title"],
        "content": data["content"]
    }

    POSTS.append(new_post)
    return jsonify(new_post), 201


@v1.route('/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    global POSTS
    post_to_delete = next((post for post in POSTS if post["id"] == id), None)

    if post_to_delete:
        POSTS.remove(post_to_delete)
        return jsonify({"message": f"Post with id {id} has been deleted successfully."}), 200
    else:
        return jsonify({"message": "Post not found."}), 404


@v1.route('/posts/<int:id>', methods=['PUT'])
def update_post(id):
    post_to_update = next((post for post in POSTS if post["id"] == id), None)

    if not post_to_update:
        return jsonify({"message": "Post not found"}), 404

    data = request.get_json()

    post_to_update["title"] = data.get("title", post_to_update["title"])
    post_to_update["content"] = data.get("content", post_to_update["content"])

    return jsonify(post_to_update), 200


@v1.route('/posts/search', methods=['GET'])
def search_posts():
    title_query = request.args.get('title', '').lower()
    content_query = request.args.get('content', '').lower()

    if not title_query and not content_query:
        return jsonify([])

    filtered_posts = [
        post for post in POSTS
        if (title_query and title_query in post['title'].lower()) or
           (content_query and content_query in post['content'].lower())
    ]

    return jsonify(filtered_posts)
