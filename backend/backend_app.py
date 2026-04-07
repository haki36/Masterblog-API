import json
import os

from flask import Flask, jsonify, request, redirect, url_for
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes


POSTS_FILE = os.path.abspath(
    os.path.join(app.root_path, '..', 'data', 'posts.json')
)


def load_posts():
    """
        Load all blog posts from the JSON file.
        Returns:
            list: A list of blog post dictionaries.
        Raises:
            FileNotFoundError: If the JSON file does not exist.
            json.JSONDecodeError: If the JSON file contains invalid JSON.
        """
    with open(POSTS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_posts(posts):
    """
    Save all blog posts to the JSON file.
    Args:
        posts (list): A list of blog post dictionaries to save.
    Raises:
        OSError: If the file cannot be written.
    """
    with open(POSTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(posts, f, indent=4)


def create_new_id(blog_posts: list[dict]) -> int:
    return max(post['id'] for post in blog_posts) + 1 if blog_posts else 1


def check_post_data(post_data: dict[str, str]) -> bool:
    if 'title' not in post_data or 'content' not in post_data:
        return False
    return True


@app.route('/api/posts', methods=['GET'])
def get_posts():
    """
    Handle GET and POST requests for blog posts.
    GET:
        Retrieve all blog posts from the JSON file.
    POST:
        Create a new blog post.
        Expects a JSON object in the request body with the following fields:
            - title (str): The title of the blog post.
            - content (str): The content of the blog post.
        Returns:
            JSON: The newly created blog post with a unique ID.
            Status Code:
                201 - If the post was successfully created.
                400 - If required fields are missing or request body is invalid.
                500 - If there is an error reading or writing the JSON file.
    """
    try:
        blog_posts = load_posts()
    except FileNotFoundError:
        blog_posts = []
    except json.JSONDecodeError:
        return jsonify({'error': 'posts.json is an invalid JSON.'}), 500

    return jsonify(blog_posts)


@app.route('/api/posts', methods=['POST'])
def add_post():
    try:
        blog_posts = load_posts()
    except FileNotFoundError:
        blog_posts = []
    except json.JSONDecodeError:
        return jsonify({'error': 'posts.json is an invalid JSON.'}), 500

    data = request.get_json()

    if not data:
        return jsonify({'error': 'request must be valid JSON'}), 400

    missing_data = []

    if not data.get('title'):
        missing_data.append('title')
    if not data.get('content'):
        missing_data.append('content')

    if not check_post_data(data) or missing_data:
        return jsonify({
            'error': 'Missing Title or Content',
            'missing_data': missing_data
        }), 400

    new_post = {
        'id': create_new_id(blog_posts),
        'title': data.get('title'),
        'content': data.get('content')
    }

    blog_posts.append(new_post)

    try:
        save_posts(blog_posts)
    except OSError:
        return jsonify({'error': 'could not write to posts.json.'}), 500

    return jsonify(new_post), 201


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
