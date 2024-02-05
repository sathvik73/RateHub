from flask import Flask, render_template, request, jsonify , session , redirect , url_for, g
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__, template_folder="C:/Users/gsath/OneDrive/Desktop/Code/ratehub")
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1245@localhost:3306/ratehub'
app.secret_key = 'abcd1234'
db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

class Categories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)

class Titles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    title_name = db.Column(db.String(255), nullable=False)
    rating = db.Column(db.Float)
    num_ratings = db.Column(db.Integer, default=0)
    reviews = db.relationship('Reviews', backref='titles', lazy=True)

class Reviews(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title_id = db.Column(db.Integer, db.ForeignKey('titles.id'), nullable=False)
    user_id = db.Column(db.Integer)
    rating = db.Column(db.Integer)
    comment = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = Users.query.filter_by(username=username, password=password).first()

        if user:
            session['logged'] = True
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('home'))

        else:
            return render_template('login.html', error='Invalid credentials')

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if the username already exists
        existing_user = Users.query.filter_by(username=username).first()

        if existing_user:
            return render_template('signup.html', error='Username already exists')
        new_user = Users(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/logout')
def logout():
    session['logged'] = False
    return redirect(url_for('category'))

@app.route('/')
def category():
    all_categories = Categories.query.all()
    logged = session.get('logged', False)
    username = session.get('username')
    return render_template('categories.html', categories=all_categories, logged=logged, username=username)

@app.route('/category/<int:category_id>')
def title(category_id):
    category = Categories.query.get(category_id)
    titles = Titles.query.filter_by(category_id=category.id).all()
    logged = session.get('logged', False)
    username = session.get('username')
    return render_template('titles.html', category=category, titles=titles, logged=logged, username=username)

@app.route('/title/<int:title_id>')
def details(title_id):
    title = Titles.query.get(title_id)
    reviews = Reviews.query.filter_by(title_id=title.id).all()
    logged = session.get('logged', False)
    username = session.get('username')

    user_has_rated = False
    user_rating = 0

    if logged:
        user_id = session['user_id']
        user_review = Reviews.query.filter_by(title_id=title.id, user_id=user_id).first()

        if user_review:
            user_has_rated = True
            user_rating = user_review.rating

    return render_template('title_details.html', title=title, user_has_rated=user_has_rated, user_rating=user_rating, reviews=reviews, logged=logged, username=username)

@app.route('/rate_title/<int:title_id>', methods=['POST'])
def rate_title(title_id):
    if not session.get('logged'):
        return redirect(url_for('login'))

    user_id = session['user_id']

    title = Titles.query.get(title_id)
    if title:
        rating = int(request.form.get('rating'))
        comment = request.form.get('comment')
        print(f"New Rating: {rating}")

        # Update the title rating and no.of ratings
        title.rating = (title.rating * title.num_ratings + rating) / (title.num_ratings + 1)
        title.num_ratings += 1

        # Add the new review to the database
        newreview = Reviews(title_id=title.id, user_id=user_id,comment = comment, rating=rating)
        db.session.add(newreview)
        db.session.commit()
        print("Review added successfully.")
    else:
        print("Title not found.")

    return redirect(url_for('details', title_id = title_id))

@app.route('/remove_rating/<int:title_id>', methods=['POST'])
def remove_rating(title_id):
    if not session.get('logged'):
        return redirect(url_for('login'))

    user_id = session['user_id']
    title = Titles.query.get(title_id)

    # Check if the user has already rated this title
    existing_rating = Reviews.query.filter_by(title_id=title_id, user_id=user_id).first()
    if existing_rating:
        # Remove the existing review
        db.session.delete(existing_rating)
        db.session.commit()
        print("Rating and review removed successfully.")
    else:
        print("User has not rated this title.")

    # Redirect back to the category page
    return redirect(url_for('details', title_id = title_id))

if __name__ == "__main__":
    app.run(debug=True)