from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from .models import Post, Contact
from .database import db
from datetime import datetime

views = Blueprint('views', __name__)


@views.route('/')
def home():
    post_data = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('index.html', user=current_user, posts=post_data)


@views.route('/blog_posted', methods=['POST'])
@login_required
def blog_posted():
    if request.method == 'POST':
        title = request.form.get('title')
        sub_title = request.form.get('sub_title')
        author = request.form.get('author')
        content = request.form.get('blog_content')

        if title and author and content:
            data = Post(title=title, sub_title=sub_title,
                        author=author, date_posted=datetime.now(),
                        content=content, user_id=current_user.id)
        else:
        	data = Post(title=title, sub_title=sub_title,
                        author=current_user.name, date_posted=datetime.now(),
                        content=content, user_id=current_user.id)
        db.session.add(data)
        db.session.commit()
        post_data = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template("index.html", user=current_user, posts=post_data)


@views.route('/add_post')
@login_required
def add_post():
    return render_template('add_post.html', user=current_user)


@views.route('/post/<int:post_id>', methods=['GET'])
@login_required
def post(post_id):
    post = Post.query.get(post_id)
    return render_template('post.html', user=current_user, post=post)


@views.route('/about')
@login_required
def about():
    return render_template('about.html', user=current_user)


@views.route('/contact', methods=['GET', 'POST'])
@login_required
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        ph_no = request.form['phone']
        message = request.form['message']
        msg_details = Contact(name=name, email=email, ph_no=ph_no, message=message)
        db.session.add(msg_details)
        db.session.commit()
        flash(f'Thanks for your valuable message!', category='success')
        return redirect(url_for('views.contact'))
    else:
        return render_template('contact.html', user=current_user)
    return redirect(url_for('views.home'))
