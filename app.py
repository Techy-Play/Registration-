from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
db = SQLAlchemy(app)

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    mobile = db.Column(db.String(15), nullable=False)
    address = db.Column(db.Text, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    profile_photo = db.Column(db.String(200))
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

def init_admin():
    with app.app_context():
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                password=generate_password_hash('admin'),
                name='Administrator',
                mobile='0000000000',
                address='Admin Address',
                gender='Other',
                dob=datetime.strptime('2000-01-01', '%Y-%m-%d'),
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            name = request.form['name']
            mobile = request.form['mobile']
            address = request.form['address']
            gender = request.form['gender']
            dob = datetime.strptime(request.form['dob'], '%Y-%m-%d')

            if User.query.filter_by(username=username).first():
                flash('Username already exists!', 'error')
                return redirect(url_for('index'))

            new_user = User(
                username=username,
                password=generate_password_hash(password),
                name=name,
                mobile=mobile,
                address=address,
                gender=gender,
                dob=dob
            )
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash('An error occurred. Please try again.', 'error')
            return redirect(url_for('index'))

    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['is_admin'] = user.is_admin
            flash('Logged in successfully!', 'success')
            return redirect(url_for('profile'))
        else:
            flash('Invalid username or password!', 'error')
    
    return render_template('login.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    
    if request.method == 'POST':
        try:
            user.name = request.form['name']
            user.mobile = request.form['mobile']
            user.address = request.form['address']
            
            if 'profile_photo' in request.files:
                file = request.files['profile_photo']
                if file.filename:
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    user.profile_photo = filename
            
            db.session.commit()
            flash('Profile updated successfully!', 'success')
        except Exception as e:
            flash('An error occurred while updating profile.', 'error')
    
    return render_template('profile.html', user=user)

@app.route('/admin')
def admin():
    if not session.get('is_admin', False):
        return redirect(url_for('login'))
    
    users = User.query.filter_by(is_admin=False).all()
    return render_template('admin.html', users=users)

@app.route('/admin/edit/<int:user_id>', methods=['GET', 'POST'])
def admin_edit_user(user_id):
    if not session.get('is_admin', False):
        return redirect(url_for('login'))
    
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        try:
            user.name = request.form['name']
            user.mobile = request.form['mobile']
            user.address = request.form['address']
            db.session.commit()
            flash('User updated successfully!', 'success')
            return redirect(url_for('admin'))
        except Exception as e:
            flash('An error occurred while updating user.', 'error')
    
    return render_template('admin_edit.html', user=user)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        init_admin()
    app.run()