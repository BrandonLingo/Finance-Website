from flask import Flask, render_template, url_for, redirect, request, flash
from forms import *
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from datetime import datetime, date
from flask_migrate import Migrate

app = Flask(__name__)

# Sercet Key
app.config['SECRET_KEY'] = "Password"


#Create Home Page
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')
#----------------------------------------------------------------------------------
# Sign Up
@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    proceed = False
    form = UserForm()
    if form.validate_on_submit():
        user = UsersModel.query.filter_by(email=form.email.data).first()
        if user is None:

            # Creates a Hashed Password
            hashed_pw = generate_password_hash(form.password_hash.data)

            # Sets all the data entered in form in to the database
            user = UsersModel(name=form.name.data, email=form.email.data, phone_number=form.phone_number.data, password_hash=hashed_pw, balance=0)
            flash("Account Cretaed!")
            db.session.add(user)
            db.session.commit()
        form.email.data = ''
        form.name.data = ''
        form.phone_number.data = ''
        form.password_hash.data = ''
        proceed = True
        return redirect(url_for('index'))
    return render_template('signUp.html', form=form, proceed=proceed)
#----------------------------------------------------------------------------------
#Delete Users
@app.route('/delete/<int:id>')
def delete_user(id):
    user_delete = UsersModel.query.get_or_404(id)

    try:
        db.session.delete(user_delete)
        db.session.commit()
        user = UsersModel.query.order_by(UsersModel.date_added)
        return redirect(url_for('login'))
    except:
        return redirect(url_for('login'))

# Delete for admin
@app.route('/delete/<int:id>/admin')
def delete_user_admin(id):
    user_delete = UsersModel.query.get_or_404(id)

    try:
        db.session.delete(user_delete)
        db.session.commit()
        user = UsersModel.query.order_by(UsersModel.date_added)
        return redirect(url_for('admin'))
    except:
        return render_template('admin.html', user=user)

#----------------------------------------------------------------------------------
# Update Users
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_user(id):
    form = UserForm()
    user_to_update = UsersModel.query.get_or_404(id)

    if request.method == "POST":
        user_to_update.name = request.form['name']
        user_to_update.email = request.form['email']
        user_to_update.phone_number = request.form['phone_number']
        try:
            db.session.commit()
            flash("Updated!")
            return render_template('update.html', form=form, user=user_to_update)
        except:
            return render_template('update.html', form=form, user=user_to_update)
    else: return render_template('update.html', form=form, user=user_to_update, id=id)

#----------------------------------------------------------------------------------
# Profile Page
@app.route('/profile/<int:id>')
def profile(id):
    user = UsersModel.query.get_or_404(id)
    if current_user.id != id:
        flash("Access Denied")
        return redirect(url_for('index'))
    return render_template('profile.html', users=user)
#----------------------------------------------------------------------------------
# DASHBOARD
@app.route('/dashboard/<int:id>', methods=['POST', 'GET'])
def dashboard(id):
    
    if current_user.id != id:
        return redirect(url_for('index'))
    else:
        form = TransactionForm()
        user = UsersModel.query.get_or_404(id)
        return render_template('dashboard.html', user=user, form=form)

@app.route('/deposit/<int:id>', methods=['POST', 'GET'])
def deposit(id):
    if current_user.id != id:
        return redirect(url_for('index'))
    else:
        form = TransactionForm()
        user = UsersModel.query.get_or_404(id)
        
        if request.method == "POST":
            current_money = user.balance + form.deposit.data
            user.balance = current_money
            user.deposit_contnet = form.deposit_content.data
            form.deposit_content.data = ''
    
            try:
                db.session.commit()
                return render_template('dashboard.html', user=user, form=form)
            except:
                return render_template('dashboard.html', user=user, form=form)
        else: return render_template('dashboard.html', user=user, form=form)

@app.route('/withdrawl/<int:id>', methods=['POST', 'GET'])
def withdrawl(id):
    if current_user.id != id:
        return redirect(url_for('index'))
    else:
        form = TransactionForm()
        user = UsersModel.query.get_or_404(id)

        if request.method == 'POST':
            current_money = user.balance - form.withdrawl.data
            user.balance = current_money
            user.withdrawl_content = form.withdrawl_content.data
            form.withdrawl_content.data = ''

            try:
                db.session.commit()
                return render_template('dashboard.html', user=user, form=form)
            except:
                return render_template('dashboard.html', user=user, form=form)
        else: 
            return render_template('dashboard.html', user=user, form=form)

#----------------------------------------------------------------------------------
# Admin
@app.route('/admin/MasterGaming1')
def admin():
    contact = contactModel.query.order_by(contactModel.date_posted)
    users = UsersModel.query.order_by(UsersModel.date_added)

    return render_template('admin.html', user=users, contact=contact)

#----------------------------------------------------------------------------------
#Login/Logout
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return UsersModel.query.get(int(user_id))

# Login Page
 #Create Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = UsersModel.query.filter_by(email=form.email.data).first()
        if user:
            # Check the Hash
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash('Login Successful')
                return redirect(url_for('dashboard', id=user.id))
            else:
                flash('Wrong Password')
        else:
            flash('User dosent exist')
    return render_template('login.html', form=form)

@app.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
#----------------------------------------------------------------------------------
# Contact

@app.route('/contact', methods=['POST', 'GET'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        contact = contactModel(email=form.email.data, phone_number=form.phone_number.data, content=form.content.data, subject=form.subject.data)
        db.session.add(contact)
        db.session.commit()
    form.email.data = ''
    form.phone_number.data = ''
    form.subject.data = ''
    form.content.data = ''
    return render_template('contact.html', form=form)

#----------------------------------------------------------------------------------
# About
@app.route('/about')
def about():
    return render_template('about.html')
#----------------------------------------------------------------------------------

# DATABASES

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///accounts.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.app_context().push()

class UsersModel(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False,)
    email = db.Column(db.String(120), nullable=False, unique=True)
    phone_number = db.Column(db.Integer, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    password_hash = db.Column(db.String(100))
    balance = db.Column(db.Integer)
    deposit_contnet = db.Column(db.Text)
    withdrawl_content = db.Column(db.Text)

    @property
    def password(self):
        raise AttributeError('password is not good')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return '<Name %r>' % self.name
    
class contactModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120))
    phone_number = db.Column(db.Integer)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    content = db.Column(db.Text)
    subject = db.Column(db.String(150))

if __name__ == '__main__':
    app.run(debug=True)