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


@app.route('/api/posts', methods=['GET', 'POST'])
def get_posts():
    try:
        blog_posts = load_posts()
    except FileNotFoundError:
        blog_posts = []
    except json.JSONDecodeError:
        return jsonify({'error': 'posts.json is an invalid JSON.'}), 500

    if request.method == 'GET':
        return jsonify(blog_posts)

    data = request.get_json()

    missing_data = []

    if not data.get('title'):
        missing_data.append('title')
    if not data.get('content'):
        missing_data.append('content')

    if missing_data:
        return jsonify({
            'error': 'Missing Title or Content',
            'missing_data': missing_data
        }), 400

    new_id = max(post['id'] for post in blog_posts) + 1 if blog_posts else 1

    new_post = {
        'id': new_id,
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
