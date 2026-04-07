import json
import os

from flask import Flask, jsonify, request
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


@app.route('/api/posts', methods=['GET'])
def get_posts():
    try:
        blog_posts = load_posts()
    except FileNotFoundError:
        blog_posts = []
    except json.JSONDecodeError:
        return "Error: posts.json is an invalid JSON.", 500

    return jsonify(blog_posts)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
