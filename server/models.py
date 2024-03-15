from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates
from config import db
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

    friends = db.relationship(
        'User',
        secondary=friend,
        primaryjoin=(friend.c.friend1_id == id),
        secondaryjoin=(friend.c.friend2_id == id),
        backref=db.backref('friendships', lazy='dynamic')
    )
    # user_hobbies = db.relationship('UserHobby', back_populates = "user")
    # user_posts = db.relationship('UserPosts', back_populates = "user")

    serialize_rules = ("-friends.user",)

    @validates('email')
    def validate_email(self, key, email):
        if not re.match(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$', email):
            raise ValueError("Invalid email format")
        return email
    pass

class Hobby(db.Model, SerializerMixin):
    __tablename__ = "hobbies"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    image = db.Column(db.String)
    description = db.Column(db.String)

    # user_hobbies = db.relationship('UserHobby', back_populates = "hobby")
    # post_hobbies = db.relationship('PostHobby', back_populates = "hobby")

    # serialize_rules = ("-user_hobbies.hobby", "-post_hobbies.hobby")

    pass

class Post(db.Model, SerializerMixin):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key = True)
    image = db.Column(db.String)
    description = db.Column(db.String)
    comments = db.Column(db.String)

    # post_hobbies = db.relationship("PostHobby", back_populates = "post")
    # user_posts = db.relationship("UserPost", back_populates = "post")
    
    # serialize_rules = ("-post_hobbies.post", "-user_posts.post")

# class UserHobby(db.Model, SerializerMixin):
#     __tablename__ = "user_hobbies"

#     id = db.Column(db.Integer, primary_key = True)
#     user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
#     hobby_id = db.Column(db.Integer, db.ForeignKey("hobbies.id"))

#     user = db.relationship("User", back_populates = "user_hobbies")
#     hobby = db.relationship("Hobby", back_populates = "user_hobbies")
    
#     serialize_rules = ("-user.user.hobbies", "-hobby.user_hobbies")

# class UserPost(db.Model, SerializerMixin):
#     __tablename__ = "user_posts"

#     id = db.Column(db.Integer, primary_key = True)
#     user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
#     post_id = db.Column(db.Integer, db.ForeignKey("posts.id"))

#     user = db.relationship("User", back_populates = "user_posts")
#     post = db.relationship("Post", back_populates = "user_posts")

#     serialize_rules = ("-user.user_posts", "-post.user_posts")

# class PostHobby(db.Model, SerializerMixin):
#     __tablename__ = "post_hobbies"

#     id = db.Column(db.Integer, primary_key = True)
#     post_id = db.Column(db.Integer, db.ForeignKey("posts.id"))
#     hobby_id = db.Column(db.Integer, db.ForeignKey("hobbies.id"))

#     post = db.relationship("Post", back_populates = "post_hobbies")
#     hobby = db.relationship("Hobby", back_populates = "post_hobbies")
    
#     serialize_rules = ("-post.post_hobbies", "-hobby.post_hobbies")