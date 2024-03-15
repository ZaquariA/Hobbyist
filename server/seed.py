#!/usr/bin/env python3

# Standard library imports
from random import randint, choice as rc

# Remote library imports
from faker import Faker

# Local imports
from app import app
from models import db, User, Hobby



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
        db.create_all()
        db.session.add_all(hobbies)
        db.session.add_all(users)
        db.session.commit()

    
