from flask import Flask, request, render_template, make_response, jsonify
from flask_cors import CORS
from flask_mongoengine import MongoEngine
import os

app = Flask(__name__)

cors = CORS(app, resources={r"/*": {"origins": "*"}})

app.config["MONGODB_HOST"] = os.environ.get('CONNECTION_STRING')

db = MongoEngine()
db.init_app(app)

class Posts(db.Document):
    name = db.StringField()
    location = db.StringField()
    title = db.StringField()
    text = db.StringField()
    image_url = db.StringField()
    
@app.route('/')
def home():
    filter = []
    for post in Posts.objects:
        if post["location"] not in filter:
            filter.append(post["location"])
    filter.sort()
    return render_template("index.html", posts=Posts.objects, locations=filter)

@app.route('/posts/', methods=['GET', 'POST'])
def posts():
    if request.method == "GET":
        posts = []
        for post in Posts.objects:
            posts.append(post)
        return make_response(jsonify(posts), 200)
    elif request.method == "POST":
        content = request.json
        post = Posts(name=content['name'], location=content['location'], title=content['title'], text=content['text'], image_url=content['image_url'])
        post.save()
        return make_response("Post successfully created.", 201)

@app.route('/posts/<name>', methods=['GET', 'PUT', 'DELETE'])
def post(name):
    post = Posts.objects(name=name).first()
    if post:
        if request.method == "GET":
            return make_response(jsonify(post), 200)
        elif request.method == "PUT":
            content = request.json
            post.update(text=content['text'])
            return make_response("Post successfully modified", 200)
        elif request.method == "DELETE":
            post.delete()
            return make_response("Post successfully deleted.", 200)
    return make_response('Post not found.', 400)

@app.route('/<location>', methods=['GET'])
def filter(location):
    posts = Posts.objects(location=location).all()
    if posts:
        return make_response(jsonify(posts), 200)
    return make_response('Location not found.', 400)

if __name__ == '__main__':
    app.run()
    