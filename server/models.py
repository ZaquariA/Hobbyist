from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates
from config import db, bcrypt
from sqlalchemy.ext.hybrid import hybrid_property
import re

# Models go here!
friend = db.Table(
    'friend',
    db.Column('friend1_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('friend2_id', db.Integer, db.ForeignKey('users.id'))
)

class User(db.Model, SerializerMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), unique=True)
    email = db.Column(db.String)
    password = db.Column(db.String)
    image = db.Column(db.String)
    bio = db.Column(db.String)
    _password_hash = db.Column(db.String)


    friends = db.relationship(
        'User',
        secondary=friend,
        primaryjoin=(friend.c.friend1_id == id),
        secondaryjoin=(friend.c.friend2_id == id),
        backref=db.backref('friendships', lazy='dynamic')
    )
    user_hobbies = db.relationship('UserHobby', back_populates = "user")
    user_posts = db.relationship('UserPost', back_populates = "user")

    @validates('email')
    def validate_email(self, key, email):
        if not re.match(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$', email):
            raise ValueError("Invalid email format")
        return email
    
    @hybrid_property
    def password_hash(self):
        raise Exception('Password hashes may not be viewed.')
    
    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(
            password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')
    
    def authenticate(self, password):
        return bcrypt.check_password_hash(
            self._password_hash, password.encode('utf-8'))

    serialize_rules = ("-friends.user", "-user.hobbies.user", "-_password_hash")

class Hobby(db.Model, SerializerMixin):
    __tablename__ = "hobbies"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, unique = True)
    image = db.Column(db.String)
    description = db.Column(db.String)

    user_hobbies = db.relationship('UserHobby', back_populates = "hobby")
    post_hobbies = db.relationship('PostHobby', back_populates = "hobby")

    serialize_rules = ("-user_hobbies.hobby", "-post_hobbies.hobby")



class Post(db.Model, SerializerMixin):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key = True)
    image = db.Column(db.String)
    description = db.Column(db.String)
    comments = db.Column(db.String)

    post_hobbies = db.relationship("PostHobby", back_populates = "post")
    user_posts = db.relationship("UserPost", back_populates = "post")
    
    serialize_rules = ( "-user_posts.post","-post_hobbies.post")



class UserHobby(db.Model, SerializerMixin):
    __tablename__ = "user_hobbies"

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    hobby_id = db.Column(db.Integer, db.ForeignKey("hobbies.id"))

    user = db.relationship("User", back_populates = "user_hobbies")
    hobby = db.relationship("Hobby", back_populates = "user_hobbies")
    
    serialize_rules = ("-user.user.hobbies", "-hobby.user_hobbies")

class UserPost(db.Model, SerializerMixin):
    __tablename__ = "user_posts"

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"))

    user = db.relationship("User", back_populates = "user_posts")
    post = db.relationship("Post", back_populates = "user_posts")

    serialize_rules = ("-user.user_posts", "-post.user_posts")

class PostHobby(db.Model, SerializerMixin):
    __tablename__ = "post_hobbies"

    id = db.Column(db.Integer, primary_key = True)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"))
    hobby_id = db.Column(db.Integer, db.ForeignKey("hobbies.id"))

    post = db.relationship("Post", back_populates = "post_hobbies")
    hobby = db.relationship("Hobby", back_populates = "post_hobbies")
    
    serialize_rules = ("-post.post_hobbies", "-hobby.post_hobbies")