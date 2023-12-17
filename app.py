from flask import Flask,jsonify,request

import secrets

from secrets import randbelow, token_urlsafe
from datetime import datetime


app = Flask(__name__)

posts=[]

# @app.get("/random/<int:sides>")
# def roll(sides):
#     if sides <= 0:
#         return { 'err': 'need a positive number of sides' }, 400
    
#     return { 'num': randbelow(sides) + 1 }

def generate_key():
    return secrets.token_urlsafe(16)

def generate_id():
    return len(posts) + 1

def fulltext_search(query):
    results = []

    for post in posts:
        if query.lower() in post['msg'].lower():
            results.append({
                "id": post['id'],
                "timestamp": post['timestamp'],
                "msg": post['msg']
            })

    return results

@app.post("/post")
def create_post():
    try:
        data = request.get_json()

        if not isinstance(data, dict) or 'msg' not in data or not isinstance(data['msg'], str):
            return jsonify({"error": "Bad Request. 'msg' field missing or not a string."}), 400

        post_id = generate_id()
        key = generate_key()
        timestamp = datetime.utcnow().isoformat().split('.')[0]
        reply_to = data.get('reply_to')

        post = {
            "id": post_id,
            "key": key,
            "timestamp": timestamp,
            "msg": data['msg'],
            "reply_to": reply_to
        }

        posts.append(post)
        response = {
            "id": post_id,
            "key": key,
            "timestamp": timestamp
        }

        return jsonify(response), 200

    except Exception as e:
        print(f"err: {e}")
        return jsonify({"err": "Internal Server Error"}), 500
    

@app.get('/post/<int:post_id>')
def read_post(post_id):
    post = next((p for p in posts if p['id'] == post_id), None)
    
    if post:
        replies = [p['id'] for p in posts if p.get('reply_to') == post_id]
        
        return jsonify({
            "id": post['id'],
            "timestamp": post['timestamp'],
            "msg": post['msg'],
            "replies": replies
        }), 200
    else:
        return jsonify({"err": "Post not found"}), 404
    
@app.delete('/post/<int:post_id>/delete/<string:key>')
def delete_post(post_id, key):
    global posts
    post = next((p for p in posts if p['id'] == post_id), None)

    if post:
        if key == post['key']:
            posts = [p for p in posts if p['id'] != post_id]
            response = {
                "id": post['id'],
                "key": generate_key(),
                "timestamp": post['timestamp']
            }

            return jsonify(response), 200
        else:
            return jsonify({"err": "Forbidden. Key is inavalid"}), 403
    else:
        return jsonify({"err": "Post not found"}), 404


@app.get('/thread/<int:post_id>')
def get_thread(post_id):
    def find_replies(post_id):
        return [p for p in posts if p.get('reply_to') == post_id]

    thread_posts = []
    queue = [post_id]

    while queue:
        current_post_id = queue.pop(0)
        current_post = next((p for p in posts if p['id'] == current_post_id), None)

        if current_post:
            thread_posts.append(current_post)
            replies = find_replies(current_post_id)
            queue.extend([reply['id'] for reply in replies])

    return jsonify([
        {
            "id": post['id'],
            "timestamp": post['timestamp'],
            "msg": post['msg']
        } for post in thread_posts
    ]), 200


@app.get('/fulltext_search')
def manual_fulltext_search():
    try:
        query = request.args.get('query')
        if not query:
            return jsonify({"err": "Bad Request. 'query' parameter missing."}), 400

        results = fulltext_search(query)

        return jsonify(results), 200

    except Exception as e:
        print(f"err: {e}")
        return jsonify({"err": "Internal Server Error"}), 500

@app.get('/date_time_range_search')
def date_time_range_search():
    try:
        start_date_time_str = request.args.get('start_datetime', '')
        end_date_time_str = request.args.get('end_datetime', '')

        if not start_date_time_str and not end_date_time_str:
            return jsonify({"error": "Bad Request. Provide at least one of 'start_datetime' or 'end_datetime' parameters."}), 400

        start_datetime = datetime.strptime(start_date_time_str, "%Y-%m-%dT%H:%M:%S") if start_date_time_str else None
        end_datetime = datetime.strptime(end_date_time_str, "%Y-%m-%dT%H:%M:%S") if end_date_time_str else None
        # print("success1")
        filtered_posts = []

        for post in posts:
            post_timestamp = datetime.strptime(post['timestamp'], "%Y-%m-%dT%H:%M:%S")
            # print("success2")

            if (not start_datetime or post_timestamp >= start_datetime) and (not end_datetime or post_timestamp <= end_datetime):
                filtered_posts.append({
                    "id": post['id'],
                    "timestamp": post['timestamp'],
                    "msg": post['msg']
                })

        return jsonify(filtered_posts), 200

    except Exception as e:
        print(f"err: {e}")
        return jsonify({"err": "Internal Server Error"}), 500