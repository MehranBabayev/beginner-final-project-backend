from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField,  TextAreaField, PasswordField, SubmitField,EmailField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from models import User

class RegisterForm(FlaskForm):
    def validate_email(form,field):
      if User.query.filter_by(Email=field.data).count()>0:
        raise ValidationError('You have registered before')
    
    Full_name = StringField(label='Full name', validators=[DataRequired(), Length(min=3, max=30)])
    Email = StringField(label='Email', validators=[DataRequired(), Email(), Length( max=30)])
    password = PasswordField( label='password', validators=[DataRequired(), Length(min=3, max=30)])
    confirm_password = PasswordField('confirm password', validators=[DataRequired(), EqualTo('password'),Length(min=3, max=30)])
    
    
    
class LoginForm(FlaskForm):
    email = EmailField(label='Email', validators=[DataRequired(), Email(), Length( max=30)])
    password = PasswordField(label='password', validators=[DataRequired(), Length(min=3, max=30)])
    
    
    
    
class ContactForm(FlaskForm):
    Name = StringField(label='Name', validators=[DataRequired(), Length(min=3, max=30)])
    Email = StringField(label='Email', validators=[DataRequired(), Email(), Length( max=30)])
    Subject = StringField(label= 'Subject', validators=[DataRequired()])
    Message = TextAreaField( label='Message', validators=[DataRequired()])


class SearchForm(FlaskForm):
    searchtext = StringField(label='Search for products')
    submit_search = SubmitField(label='search')
    


class NewsletterForm(FlaskForm):
    name = StringField(label = 'Your name')
    email = StringField(label = 'Your email', validators=[DataRequired(), Email(), Length( max=30)])
    submit_news = SubmitField(label='Subscribe now')
    
    
    
class FavoritesForm(FlaskForm):
    submit_favorite = SubmitField('Add to favorites')   
    
    
class ReviewForm(FlaskForm):
    review_text = TextAreaField('review text', validators=[DataRequired()])

    