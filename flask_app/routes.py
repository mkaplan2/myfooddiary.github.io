# 3rd-party packages
from distutils.dep_util import newer_pairwise
import re
from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash,
    jsonify,
    Blueprint,
    session,
    g,
    current_app,
    Flask
)
from flask_mongoengine import MongoEngine
from flask_login import (
    LoginManager,
    current_user,
    login_user,
    logout_user,
    login_required,
)
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename

from flask_mail import Mail, Message
# stdlib
from datetime import datetime
import io
import base64

# local
#from . import bcrypt, movie_client
from . import bcrypt

from .forms import (
    SearchForm,
    MovieReviewForm,
    RegistrationForm,
    LoginForm,
    UpdateDiaryEntryExtraCommentsForm,
    UpdateDiaryEntryRatingForm,
    UpdateUsernameForm,
    DiaryEntryForm
)
from .models import Restaurant, User, DiaryEntry, PublicPost, load_user
from .utils import current_time


main = Blueprint("main", __name__)


#from .extensions import mail, login_manager, db #remove if mail does not work

""" ************ View functions ************ """


@main.route("/", methods=["GET", "POST"])
def index():
    form = SearchForm()

    if form.validate_on_submit():
        return redirect(url_for("main.query_results", query=form.search_query.data))

    public_entries = PublicPost.objects()
    return render_template("index.html", form=form, public_entries=public_entries)

'''
@main.route("/search-results/<query>", methods=["GET"])
def query_results(query):
    try:
        results = movie_client.search(query)
    except ValueError as e:
        flash(str(e))
        return redirect(url_for("main.index"))

    return render_template("query.html", results=results)
'''

'''
@main.route("/movies/<movie_id>", methods=["GET", "POST"])
def movie_detail(movie_id):
    try:
        result = movie_client.retrieve_movie_by_id(movie_id)
    except ValueError as e:
        flash(str(e))
        return redirect(url_for("main.login"))

    form = MovieReviewForm()
    if form.validate_on_submit() and current_user.is_authenticated:
        review = Review(
            commenter=current_user._get_current_object(),
            content=form.text.data,
            date=current_time(),
            imdb_id=movie_id,
            movie_title=result.title,
        )
        review.save()

        return redirect(request.path)

    reviews = Review.objects(imdb_id=movie_id)

    return render_template(
        "movie_detail.html", form=form, movie=result, reviews=reviews
    )
'''

'''
@main.route("/user/<username>")
def user_detail(username):
    user = User.objects(username=username).first()
    #reviews = Review.objects(commenter=user)

    return render_template("user_detail.html", username=username)
'''

#Just added
@main.route("/restaurant/<restaurant>")
@login_required
def restaurant_detail(restaurant):
    restaurant_object = Restaurant.objects(name=restaurant).first()
    user = User.objects(username=current_user.username).first()
    reviews = DiaryEntry.objects(commenter=user, restaurant=restaurant) #check to make sure this works!

    array = []
    for review in reviews:
        array.append(review)

    #return render_template("restaurant_detail.html", restaurant=restaurant_object, reviews=reviews)
    return render_template("restaurant_detail.html", restaurant=restaurant_object, reviews=array)



@main.route("/restaurant/<restaurant>/<sorted_by>")
@login_required
def restaurant_detail_with_sorting(restaurant, sorted_by):
    restaurant_object = Restaurant.objects(name=restaurant).first()
    user = User.objects(username=current_user.username).first()
    reviews = DiaryEntry.objects(commenter=user, restaurant=restaurant) #check to make sure this works!

    array = []
    for review in reviews:
        array.append(review)

    if (sorted_by == "cost"):
        array.sort(key=lambda x: x.cost) #check if this works!
        return render_template("restaurant_detail.html", restaurant=restaurant_object, reviews=array)
    
    if (sorted_by == "rating"):
        array.sort(key=lambda x: x.rating, reverse=True) #check if this works!
        return render_template("restaurant_detail.html", restaurant=restaurant_object, reviews=array)
    
    #return render_template("restaurant_detail.html", restaurant=restaurant_object, reviews=reviews)
    return render_template("restaurant_detail.html", restaurant=restaurant_object, reviews=array)




#returns array of objects
#if number == 1, then sort by cost
'''
def sort_reviews_by_cost(restaurant, review_objects, number):
    array = []
    if request.form['submit_button'] == 'cost':
        for review in review_objects:
            array.append(review)
        if (number == 1):
            array.sort(key=lambda x: x.cost) #check if this works!
        #return array
        return render_template("restaurant_detail.html", restaurant=restaurant, reviews=array)
'''


""" ************ User Management views ************ """

@main.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=hashed)
        user.save()

        #Flask email server was not working. And I think will be even worse if try to work w heroku - so GIVE UP LOL!
        #After make the user, want to send them an email
        '''
        msg = Message("Hello! Thank you for registering for Food Diaries!",
                  sender="mkmoonlight14@gmail.com",
                  recipients=[form.email.data])
        msg.body = "This is the body"
        mail.send(msg)
        '''

        return redirect(url_for("main.login"))

    return render_template("register.html", title="Register", form=form)


@main.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(username=form.username.data).first()

        if user is not None and bcrypt.check_password_hash(
            user.password, form.password.data
        ):
            login_user(user)
            return redirect(url_for("main.account"))
        else:
            flash("Login failed. Check your username and/or password")
            return redirect(url_for("main.login"))

    return render_template("login.html", title="Login", form=form)


@main.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))


@main.route("/account", methods=["GET", "POST"])
@login_required
def account():
    username_form = UpdateUsernameForm()

    if username_form.validate_on_submit():
        # current_user.username = username_form.username.data
        current_user.modify(username=username_form.username.data)
        current_user.save()
        return redirect(url_for("main.account"))

    return render_template(
        "account.html",
        title="Account",
        username_form=username_form,
    )

@main.route("/diary/<food>/<restaurant>/update_extra_comments", methods=["GET", "POST"])
@login_required
def update_extra_comments(food, restaurant):
    update_extra_comments_form = UpdateDiaryEntryExtraCommentsForm()

    user = User.objects(username=current_user.username).first()
    diary_entry_parameter = DiaryEntry.objects(commenter=user, food=food, restaurant=restaurant).first()
    
    if update_extra_comments_form.validate_on_submit() and current_user.is_authenticated:
        diary_entry = DiaryEntry.objects(commenter=user, food=food, restaurant=restaurant).first()
        diary_entry.modify(extra_comments= update_extra_comments_form.extra_comments.data)
        diary_entry.save()
        return redirect(url_for("main.update_extra_comments", food = food, restaurant = restaurant))
    
    return render_template("update_extra_comments.html", update_extra_comments_form = update_extra_comments_form, diary_entry_parameter=diary_entry_parameter)


@main.route("/diary/<food>/<restaurant>/update_rating", methods=["GET", "POST"])
@login_required
def update_rating(food, restaurant):
    update_rating_form = UpdateDiaryEntryRatingForm()

    user = User.objects(username=current_user.username).first()
    diary_entry_parameter = DiaryEntry.objects(commenter=user, food=food, restaurant=restaurant).first()
    
    if update_rating_form .validate_on_submit() and current_user.is_authenticated:
        diary_entry = DiaryEntry.objects(commenter=user, food=food, restaurant=restaurant).first()
        diary_entry.modify(rating = update_rating_form.rating.data)
        diary_entry.save()
        return redirect(url_for("main.update_rating", food = food, restaurant = restaurant))
    
    return render_template("update_rating.html", update_rating_form = update_rating_form, diary_entry_parameter=diary_entry_parameter)




#Just added this
#Displayed when click on "my diary" tab
@main.route("/diary", methods=["GET", "POST"])
@login_required
def diary():
    form = DiaryEntryForm()
    if form.validate_on_submit() and current_user.is_authenticated:
        diary_entry = DiaryEntry(
            commenter=current_user._get_current_object(),
            date = current_time(),
            restaurant = form.restaurant.data,
            food = form.food.data,
            cost = form.cost.data, #do i need to convert this to a float?
            rating = int(form.rating.data),
            would_get_again = form.would_get_again.data,
            extra_comments = form.extra_comments.data,
            privacy = form.privacy.data
        )
        diary_entry.save()

        #If the restaurant the user added did not already exist, then need to add it
        restaurant = Restaurant.objects(name=form.restaurant.data).first()
        if (restaurant == None):
            new_restaurant = Restaurant(name = form.restaurant.data) #make the restaurant
            #If the restaurant does not exist, need to add to database of restaurant
            new_restaurant.save()

        #If the entry is "public", also make it an object in the PublicPost class
        if (form.privacy.data == "public" or form.privacy.data == "Public"):
            public_post = PublicPost(
                commenter = current_user._get_current_object(),
                date = current_time(),
                restaurant = form.restaurant.data,
                food = form.food.data,
                cost = form.cost.data, #do i need to convert this to a float?
                rating = int(form.rating.data),
                would_get_again = form.would_get_again.data,
                extra_comments = form.extra_comments.data,
                likes = 0 #initialized to zero
            )
            public_post.save()
        
        return redirect(request.path) #I think this line just empties the form after it is submitted

    user = User.objects(username=current_user.username).first()
    #user = current_user.username #check to make sure this works! (saw this done in account.html)
    diary_entries = DiaryEntry.objects(commenter = user)
    
    return render_template(
        "my_diary.html", form=form, diary_entries=diary_entries, username = user.username
    )

    #return 'my diary'
