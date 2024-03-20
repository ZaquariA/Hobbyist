from flask import Flask, request, make_response, session
from flask_migrate import Migrate
from models import *
import os



BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

app.secret_key = "\xe6\xaf\xfb\xfc.\x01I'\x1bG\xb5\x1e\xa4`!\xf0"


migrate = Migrate(app, db)
db.init_app(app)


# Views go here!

@app.route('/')
def index():
    return '<h1>Project Server</h1>'

@app.route('/check_session', methods=['GET'])
def check_session():
    user = User.query.filter(User.id == session.get('user_id')).first()
    if not user:
        return make_response({'error': "Unauthorized: you must be logged in to make that request"}, 401)
    else:
        return make_response(user.to_dict(), 200)

@app.route('/signup', methods=['POST'])
def signup():
    get_json = request.get_json()
    try:
        user = User(
            username=get_json['username'],
            name=get_json['name'],
            email=get_json['email'],
            password=get_json['password'],
            image=get_json['image'],
            bio=get_json['bio']
        )
        user.password_hash = get_json['password']
        db.session.add(user)
        db.session.commit()
        session['user_id'] = user.id

        return make_response(user.to_dict(rules = ('-user_hobbies', '-user_posts')), 201)

    except Exception as e:
        return make_response({'errors': str(e)}, 422)

@app.route('/login', methods=['POST'])
def login():
    username = request.get_json()['username']

    user = User.query.filter(User.username == username).first()
    password = request.get_json()['password']

    if not user:
        response_body = {'error': 'User not found'}
        status = 404
    else:
        if user.authenticate(password):
            session['user_id'] = user.id
            response_body = user.to_dict()
            status = 200
        else:
            response_body = {'error': 'Invalid username or password'}
            status = 401
    return make_response(response_body, status)

@app.route('/logout', methods=['DELETE'])
def logout():
    session['user_id'] = None
    return '', 204

@app.route("/users", methods=["GET", "POST"])
def users():
    if request.method == "GET":
        user_list = [user.to_dict(rules =("-user_hobbies", "-user_posts")) for user in User.query.all()]
        return make_response(user_list, 200)
    
    elif request.method == "POST":
        get_json = request.get_json()
        try:
            new_user = User(
                name = get_json["name"],
                email = get_json["email"],
                password = get_json["password"],
                image = get_json["image"],
                bio = get_json["bio"]
            )
            db.session.add(new_user)
            db.session.commit()
            return make_response(new_user.to_dict(rules = ("-user_hobbies", "-user_posts")), 201)
        except:
            return make_response({
                "errors": "validation errors"
            },400)

@app.route('/users/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def user_by_id(id):
    if request.method == 'GET':
        user = User.query.filter(User.id == id).first()
        if user:
            return make_response(user.to_dict(rules=("-user_hobbies", "-user_posts")), 200)
        else:
            return make_response({'error': 'user not found'}, 404)

    elif request.method == 'PATCH':
        user = User.query.filter(User.id == id).first()
        try:
            get_json = request.get_json()
            if user:
                for attr in get_json:
                    setattr(user, attr, get_json.get(attr))
                db.session.add(user)
                db.session.commit()
                return make_response(user.to_dict(rules=("-user_hobbies", "-user_posts")), 202)
            else:
                return make_response({'error': 'user not found'}, 404)
        except:
            return make_response({'errors': 'validation errors'}, 400)

    elif request.method == 'DELETE':
        user = User.query.filter(User.id == id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return make_response({}, 204)
        else:
            return make_response({'error': 'user not found'}, 404)

@app.route('/hobbies', methods = ["GET", "POST"])
def hobbies():
    if request.method == "GET":
        hobby_list = [hobby.to_dict(rules = ("-user_hobbies", "-post_hobbies")) for hobby in Hobby.query.all()]
        return make_response(hobby_list, 200)
    
    elif request.method == "POST":
        get_json = request.get_json()
        try:
            new_hobby = Hobby(
                name = get_json["name"],
                image = get_json["image"],
                description = get_json["description"]
            )
            db.session.add(new_hobby)
            db.session.commit()
            return make_response(new_hobby.to_dict(rules = ("-user_hobbies", "-post_hobbies")), 201)
        except:
            return make_response({
                "errors": "validation errors"
            }, 400)
        
@app.route('/hobbies/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def hobby_by_id(id):
    if request.method == 'GET':
        hobby = Hobby.query.filter(Hobby.id == id).first()
        if hobby:
            return make_response(hobby.to_dict(rules=("-user_hobbies", "-post_hobbies")), 200)
        else:
            return make_response({'error': 'hobby not found'}, 404)

    elif request.method == 'PATCH':
        hobby = Hobby.query.filter(Hobby.id == id).first()
        try:
            get_json = request.get_json()
            if hobby:
                for attr in get_json:
                    setattr(hobby, attr, get_json.get(attr))
                db.session.add(hobby)
                db.session.commit()
                return make_response(hobby.to_dict(rules=("-user_hobbies", "-post_hobbies")), 202)
            else:
                return make_response({'error': 'hobby not found'}, 404)
        except:
            return make_response({'errors': 'validation errors'}, 400)

    elif request.method == 'DELETE':
        hobby = Hobby.query.filter(Hobby.id == id).first()
        if hobby:
            db.session.delete(hobby)
            db.session.commit()
            return make_response({}, 204)
        else:
            return make_response({'error': 'hobby not found'}, 404)
        
@app.route('/posts', methods=["GET", "POST"])
def posts():
    if request.method == "GET":
        post_list = [post.to_dict(rules=("-user_posts", "-post_hobbies")) for post in Post.query.all()]
        return make_response(post_list, 200)

    elif request.method == "POST":
        get_json = request.get_json()
        try:
            new_post = Post(
                image=get_json["image"],
                description=get_json["description"],
                comments=get_json["comments"]
            )
            db.session.add(new_post)
            db.session.commit()
            return make_response(new_post.to_dict(rules=("-user_posts", "-post_hobbies")), 201)
        except:
            return make_response({
                "errors": "validation errors"
            }, 400)


@app.route('/posts/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def post_by_id(id):
    if request.method == 'GET':
        post = Post.query.filter(Post.id == id).first()
        if post:
            return make_response(post.to_dict(rules=("-user_posts", "-post_hobbies")), 200)
        else:
            return make_response({'error': 'post not found'}, 404)

    elif request.method == 'PATCH':
        post = Post.query.filter(Post.id == id).first()
        try:
            get_json = request.get_json()
            if post:
                for attr in get_json:
                    setattr(post, attr, get_json.get(attr))
                db.session.add(post)
                db.session.commit()
                return make_response(post.to_dict(rules=("-user_posts", "-post_hobbies")), 202)
            else:
                return make_response({'error': 'post not found'}, 404)
        except:
            return make_response({'errors': 'validation errors'}, 400)

    elif request.method == 'DELETE':
        post = Post.query.filter(Post.id == id).first()
        if post:
            db.session.delete(post)
            db.session.commit()
            return make_response({}, 204)
        else:
            return make_response({'error': 'post not found'}, 404)
        
@app.route('/userhobbies', methods=["GET", "POST"])
def userhobbies():
    if request.method == "GET":
        userhobby_list = [userhobby.to_dict(rules=("-user.user_hobbies", "-hobby.user_hobbies")) for userhobby in UserHobby.query.all()]
        return make_response(userhobby_list, 200)

    elif request.method == "POST":
        get_json = request.get_json()
        try:
            new_userhobby = UserHobby(
                user_id=get_json["user_id"],
                hobby_id=get_json["hobby_id"]
            )
            db.session.add(new_userhobby)
            db.session.commit()
            return make_response(new_userhobby.to_dict(rules=("-user.user_hobbies", "-hobby.user_hobbies")), 201)
        except:
            return make_response({
                "errors": "validation errors"
            }, 400)


@app.route('/userhobbies/<int:id>', methods=['GET', 'DELETE'])
def userhobby_by_id(id):
    if request.method == 'GET':
        userhobby = UserHobby.query.filter(UserHobby.id == id).first()
        if userhobby:
            return make_response(userhobby.to_dict(rules=("-user.user_hobbies", "-hobby.user_hobbies")), 200)
        else:
            return make_response({'error': 'userhobby not found'}, 404)

    elif request.method == 'DELETE':
        userhobby = UserHobby.query.filter(UserHobby.id == id).first()
        if userhobby:
            db.session.delete(userhobby)
            db.session.commit()
            return make_response({}, 204)
        else:
            return make_response({'error': 'userhobby not found'}, 404)
        
@app.route('/userposts', methods=["GET", "POST"])
def userposts():
    if request.method == "GET":
        userpost_list = [userpost.to_dict(rules=("-user.user_posts", "-post.user_posts")) for userpost in UserPost.query.all()]
        return make_response(userpost_list, 200)

    elif request.method == "POST":
        get_json = request.get_json()
        try:
            new_userpost = UserPost(
                user_id=get_json["user_id"],
                post_id=get_json["post_id"]
            )
            db.session.add(new_userpost)
            db.session.commit()
            return make_response(new_userpost.to_dict(rules=("-user.user_posts", "-post.user_posts")), 201)
        except:
            return make_response({
                "errors": "validation errors"
            }, 400)


@app.route('/userposts/<int:id>', methods=['GET', 'DELETE'])
def userpost_by_id(id):
    if request.method == 'GET':
        userpost = UserPost.query.filter(UserPost.id == id).first()
        if userpost:
            return make_response(userpost.to_dict(rules=("-user.user_posts", "-post.user_posts")), 200)
        else:
            return make_response({'error': 'userpost not found'}, 404)

    elif request.method == 'DELETE':
        userpost = UserPost.query.filter(UserPost.id == id).first()
        if userpost:
            db.session.delete(userpost)
            db.session.commit()
            return make_response({}, 204)
        else:
            return make_response({'error': 'userpost not found'}, 404)
        

@app.route('/posthobbies', methods=["GET", "POST"])
def posthobbies():
    if request.method == "GET":
        posthobby_list = [posthobby.to_dict(rules=("-post.post_hobbies", "-hobby.post_hobbies")) for posthobby in PostHobby.query.all()]
        return make_response(posthobby_list, 200)

    elif request.method == "POST":
        get_json = request.get_json()
        try:
            new_posthobby = PostHobby(
                post_id=get_json["post_id"],
                hobby_id=get_json["hobby_id"]
            )
            db.session.add(new_posthobby)
            db.session.commit()
            return make_response(new_posthobby.to_dict(rules=("-post.post_hobbies", "-hobby.post_hobbies")), 201)
        except:
            return make_response({
                "errors": "validation errors"
            }, 400)


@app.route('/posthobbies/<int:id>', methods=['GET', 'DELETE'])
def posthobby_by_id(id):
    if request.method == 'GET':
        posthobby = PostHobby.query.filter(PostHobby.id == id).first()
        if posthobby:
            return make_response(posthobby.to_dict(rules=("-post.post_hobbies", "-hobby.post_hobbies")), 200)
        else:
            return make_response({'error': 'posthobby not found'}, 404)

    elif request.method == 'DELETE':
        posthobby = PostHobby.query.filter(PostHobby.id == id).first()
        if posthobby:
            db.session.delete(posthobby)
            db.session.commit()
            return make_response({}, 204)
        else:
            return make_response({'error': 'posthobby not found'}, 404)
        

if __name__ == '__main__':
    app.run(port=5555, debug=True)

