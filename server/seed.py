#!/usr/bin/env python3

# Standard library imports
from random import randint, choice as rc

# Remote library imports
from faker import Faker

# Local imports
from app import app
from models import db, User, Hobby, Post, UserHobby, UserPost, PostHobby



if __name__ == '__main__':
    fake = Faker()
    with app.app_context():
        print("Seeding User...")
        users = [
            User(
                name= "Bob",
                email= "Zaq@gmail.com",
                password= "123zaq",
                image= "png.png",
                bio= "this is my bio"
            )
        ]

        print("Seeding Hobby...")
        hobbies = [
            Hobby(
                name = "RockClimbing",
                image = "Rock.png",
                description = "We climb rocks"
            )
        ]

        print("Seeding Post...")
        posts = [
            Post(
                image = "string.png",
                description = "stringy string",
                comments = "comments about the stringy string string.png"
            )
        ]

        print("Seeding UserHobby...")
        user_hobbies = [
            UserHobby(
                user_id = 1,
                hobby_id = 1
            )
        ]

        print("Seeding UserPost...")
        user_posts = [
            UserPost(
                user_id = 1,
                post_id = 1
            )
        ]

        print("Seeding PostHobby...")
        post_hobbies = [
            PostHobby(
                post_id = 1,
                hobby_id =1
            )
        ]


        db.create_all()
        db.session.add_all(users)
        db.session.add_all(hobbies)
        db.session.add_all(posts)
        db.session.add_all(user_hobbies)
        db.session.add_all(user_posts)
        db.session.add_all(post_hobbies)
        db.session.commit()

    
