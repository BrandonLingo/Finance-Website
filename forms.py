from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError, IntegerField
from wtforms.validators import DataRequired, EqualTo, Length, NumberRange
from wtforms.widgets import TextArea

class UserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    phone_number = IntegerField('Phone Number', validators=[DataRequired()])
    password_hash = PasswordField('Password', validators=[DataRequired(), EqualTo('password_hash2', message='Password\'s Dont Match')])
    password_hash2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Submit')

class TransactionForm(FlaskForm):
    deposit = IntegerField('Add Deposit', validators=[DataRequired()])
    deposit_content = StringField('Reason for Deposit', widget=TextArea())
    withdrawl = IntegerField('Withdrawl')
    withdrawl_content = StringField('Reason for Withdrawl', widget=TextArea())
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')

class ContactForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    phone_number = IntegerField('Phone Number', validators=[DataRequired()])
    content = StringField('Information', validators=[DataRequired()], widget=TextArea())
    subject = StringField('Subject', validators=[DataRequired()])
    submit = SubmitField('Submit')