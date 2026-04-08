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
    """
    Generate a new unique ID for a blog post.
    Args:
        blog_posts (list[dict]): A list of existing blog post dictionaries.
    Returns:
        int: A new unique integer ID. Returns 1 if no posts exist.
    """
    return max(post['id'] for post in blog_posts) + 1 if blog_posts else 1


def check_post_data(post_data: dict[str, str]) -> bool:
    """
    Validate that the blog post data contains the required fields.
    Args:
        post_data (dict[str, str]): The JSON data for a blog post.
    Returns:
        bool: True if both 'title' and 'content' are present, otherwise False.
    """
    if 'title' not in post_data or 'content' not in post_data:
        return False
    return True


def find_post(post_id: int):
    """
    Find a blog post by its ID.
    Args:
        post_id (int): The ID of the blog post to find.
    Returns:
        dict | None: The matching blog post dictionary if found, otherwise None.
    """
    blog_posts = load_posts()
    return next((post for post in blog_posts if post['id'] == post_id), None)


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """
    Delete a blog post by its ID.
    Args:
        post_id (int): The ID of the blog post to delete.
    Returns:
        Response: A JSON response with a success message if the post was deleted,
        or an error message with status code 404 if the post was not found.
    """
    blog_posts = load_posts()
    post_delete = find_post(post_id)

    if post_delete is None:
        return jsonify({
            'error': f'Post id {post_id} not found'
        }), 404

    blog_posts.remove(post_delete)

    save_posts(blog_posts)
    return jsonify({
        "message": f"Post with id {post_id} has been deleted successfully."
    })


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    """
    Update an existing blog post by its ID.
    Args:
        post_id (int): The ID of the blog post to update.
    Expects:
        A JSON request body containing optional fields:
            - title (str): The updated title of the post.
            - content (str): The updated content of the post.
    Returns:
        Response: A JSON response containing the updated blog post.
    Status Codes:
        200: If the post was updated successfully.
        400: If the request body is invalid.
        404: If no post with the given ID exists.
    """
    blog_posts = load_posts()
    post_update = find_post(post_id)

    if post_update is None:
        return jsonify({
            'error': f'Post id {post_id} not found'
        }), 404

    data = request.get_json()

    if not data:
        return jsonify({
            'error': 'Request must be valid JSON'
        }), 400

    if 'title' in data:
        post_update['title'] = data['title']
    if 'content' in data:
        post_update['content'] = data['content']

    save_posts(blog_posts)
    return jsonify(
        post_update
    ), 200


@app.route('/api/posts/search')
def search_post():
    """
    Search blog posts by title and/or content.
    Query Parameters:
        title (str, optional): A keyword to search for in the post titles.
        content (str, optional): A keyword to search for in the post content.
    Returns:
        Response: A JSON list of blog posts that match the search criteria.
    Notes:
        - If both 'title' and 'content' are provided, only posts matching both conditions are returned.
        - If no query parameters are provided, all blog posts are returned.
        - Returns an empty list if no matching posts are found.
    """
    blog_posts = load_posts()
    search_title = request.args.get('title')
    search_content = request.args.get('content')

    results = blog_posts

    if search_title:
        results = [
            post for post in results
            if search_title.lower() in post['title'].lower()
        ]

    if search_content:
        results = [
            post for post in results
            if search_content.lower() in post['content'].lower()
        ]

    return jsonify(results)


@app.route('/api/posts', methods=['GET'])
def get_posts():
    """
    Retrieve all blog posts, optionally sorted by title or content.
    Query Parameters:
        sort (str, optional): Field to sort by. Allowed values: 'title', 'content'.
        direction (str, optional): Sort direction. Allowed values: 'asc', 'desc'.
    Returns:
        Response: A JSON list of blog posts.
    Status Codes:
        200: If posts are returned successfully.
        400: If sort field or direction is invalid.
        500: If posts.json is missing or contains invalid JSON.
    """
    sorted_by = request.args.get('sort')
    sorted_direction = request.args.get('direction')
    try:
        blog_posts = load_posts()
    except FileNotFoundError:
        blog_posts = []
    except json.JSONDecodeError:
        return jsonify({'error': 'posts.json is an invalid JSON.'}), 500

    if sorted_by is None or sorted_direction is None:
        return jsonify(blog_posts)

    if sorted_by not in ['title', 'content']:
        return jsonify({
            'error': 'Invalid sort field. Use "title" or "content".'
        }), 400
    if sorted_direction not in ['asc', 'desc']:
        return jsonify({
            'error': 'Invalid direction. Use "asc" or "desc".'
        }), 400

    reverse_sort = sorted_direction == 'desc'

    sorted_posts = sorted(
        blog_posts,
        key=lambda post: post[sorted_by].lower(),
        reverse=reverse_sort
    )

    return jsonify(sorted_posts)


@app.route('/api/posts', methods=['POST'])
def add_post():
    """
    Create a new blog post.
    Expects:
        A JSON request body containing:
            - title (str): The title of the new post.
            - content (str): The content of the new post.
    Returns:
        Response: A JSON response containing the newly created post with a unique ID.
    Status Codes:
        201: If the post was created successfully.
        400: If the request body is invalid or required fields are missing.
        500: If there is an error reading or writing the JSON file.
    """
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
