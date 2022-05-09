from flask_login import UserMixin
from datetime import datetime
#from .extensions import db, login_manager #comment back in if mail does not work!
from . import config
from .utils import current_time
import base64
from . import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.objects(username=user_id).first()


class User(db.Document, UserMixin):
    username = db.StringField(required=True, unique=True)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True)

    # Returns unique string identifying our object
    def get_id(self):
        return self.username



#from p5: This is used by movie reviews (can remove later)
'''
class Review(db.Document):
    commenter = db.ReferenceField(User, required=True)
    content = db.StringField(required=True, min_length=5, max_length=500)
    date = db.StringField(required=True)
    imdb_id = db.StringField(required=True, min_length=9, max_length=9)
    movie_title = db.StringField(required=True, min_length=1, max_length=100)
'''

#Just added
class DiaryEntry(db.Document):
    commenter = db.ReferenceField(User, required=True) 
    date = db.StringField(required=True)
    food = db.StringField(required=True) #name of food
    restaurant = db.StringField(required=True) #name of restaurant
    cost = db.IntField(required=True) #Hmmm I am not sure how to get this working w a float/double/decimal field (could not find the docs) - try to find in docs later!
    rating = db.IntField(required=True)
    would_get_again = db.StringField(required=True)
    extra_comments = db.StringField(required=False)
    privacy = db.StringField(required=True)

#Just added
'''
Unlike DiaryEntry:
    - PublicPost does NOT have a privacy field (bc all are public)
    - PublicPost has a "likes" field
'''
class PublicPost(db.Document):
    commenter = db.ReferenceField(User, required=True) 
    date = db.StringField(required=True)
    food = db.StringField(required=True) #name of food
    restaurant = db.StringField(required=True) #name of restaurant
    cost = db.IntField(required=True) #Hmmm I am not sure how to get this working w a float/double/decimal field (could not find the docs) - try to find in docs later!
    rating = db.IntField(required=True)
    would_get_again = db.StringField(required=True)
    extra_comments = db.StringField(required=False)
    likes = db.IntField(required=True)

class Restaurant(db.Document):
    name = db.StringField(required = True)