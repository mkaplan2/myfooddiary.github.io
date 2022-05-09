from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from wtforms import StringField, IntegerField, SubmitField, TextAreaField, PasswordField, RadioField, FloatField, DecimalField
from wtforms.validators import (
    InputRequired,
    DataRequired,
    NumberRange,
    Length,
    Email,
    EqualTo,
    ValidationError,
)

from .models import User

class SearchForm(FlaskForm):
    search_query = StringField(
        "Query", validators=[InputRequired(), Length(min=1, max=100)]
    )
    submit = SubmitField("Search")


class MovieReviewForm(FlaskForm):
    text = TextAreaField(
        "Comment", validators=[InputRequired(), Length(min=5, max=500)]
    )
    submit = SubmitField("Enter Comment")




#Just added
class DiaryEntryForm(FlaskForm):
    food = StringField( "Food", validators=[InputRequired(), Length(min=1, max=40)])
    restaurant = StringField("Restaurant", validators=[InputRequired(), Length(min=1, max=40)])
    cost = DecimalField("Cost", validators=[InputRequired()] )
    rating = RadioField("Rating", choices=['1','2','3','4','5'], validators=[InputRequired()] )

    #radiofield : circles for choices
    
    would_get_again = RadioField(
        "Would Get Again?", choices=['Yes', 'No', 'Maybe'],validators=[InputRequired()]
    )

    #would_get_again = StringField("Would Get Again?")
    extra_comments = TextAreaField("Extra Comments?") #not required

    privacy = RadioField("Privacy", choices=['public','private'], validators=[InputRequired()] )

    submit = SubmitField("Submit Diary Entry")


'''
- This form will only be available in the diary entry place.
- This way the user is only able to update the diary entries that they themselves made
'''
class UpdateDiaryEntryExtraCommentsForm(FlaskForm):
    extra_comments = TextAreaField("Update Your Extra Comments Below:")
    submit = SubmitField("Update Extra Comments")



#Just added
class UpdateDiaryEntryRatingForm(FlaskForm):
    rating = RadioField("Update Your Rating Below:", choices=['1','2','3','4','5'], validators=[InputRequired()] )
    submit = SubmitField("Update Rating")



class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[InputRequired(), Length(min=1, max=40)]
    )
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password (Must contain a special character, number and uppercase letter)", validators=[InputRequired(), Length(min=1, max=40)])
    confirm_password = PasswordField(
        "Confirm Password", validators=[InputRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")

    def validate_password(self, password):
        special_symbol = ['!','@','#','$','%','&','_','=']
        if not any(char.isdigit() for char in password.data):
            raise ValidationError("Password must have at least one numeral")
        if not any(char in special_symbol for char in password.data):
            raise ValidationError("Password must contain a special character from: !@#$%&_=")
        if not any(char.isupper() for char in password.data):
            raise ValidationError("Password must have at least one upper case letter")
    
    def validate_username(self, username):
        user = User.objects(username=username.data).first()
        if user is not None:
            raise ValidationError("Username is taken")

    def validate_email(self, email):
        user = User.objects(email=email.data).first()
        if user is not None:
            raise ValidationError("Email is taken")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Login")


class UpdateUsernameForm(FlaskForm):
    username = StringField(
        "In other news... Would You Like To Update Your Username?", validators=[InputRequired(), Length(min=1, max=40)]
    )
    submit = SubmitField("Update Username")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.objects(username=username.data).first()
            if user is not None:
                raise ValidationError("That username is already taken")