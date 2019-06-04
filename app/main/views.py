from flask import render_template, request, redirect,url_for,abort, flash
from . import main
from ..models import Post, User, Comment
from .forms import PostForm, CommentsForm, UpdateProfile, UpdatePost
from flask_login import login_required, current_user
from .. import db, photos
import markdown2
import requests
import json 

# Views
@main.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''
    random = requests.get('http://quotes.stormconsultancy.co.uk/random.json').json()
    post_list = Post.query.order_by(Post.posted.desc()).all()

    title = "Lets have fun "
    return render_template('index.html', title = title, post_data = post_list, random = random)

@main.route('/latest_post')
def latestpost():

    '''
    view function that returns the latest single blog post
    '''

    post_latest = Post.query.order_by(Post.id.desc()).first()


    return render_template('latest.html',post_latest = post_latest)


@main.route('/post/<int:id>', methods = ['GET'])
def post(id):
    id=id
    my_post = Post.query.get(id)

    if id is None:
        abort(404)

    full_post = Post.query.filter_by(id=id).all()

    return render_template('post.html', post_data = my_post, id=id, full_post = full_post)

@main.route('/post/new', methods = ['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    new_post = None

    if form.validate_on_submit():
        post_title = form.post_title.data
        post = form.post.data

        new_post = Post(title = post_title, post = post, user = current_user)

        new_post.save_post()

        return redirect(url_for('.index'))

    title = 'New Post'
    return render_template('new_post.html', title = title, post_form = form, new_post = new_post)

@main.route('/delete_post/<id>', methods=['GET', 'POST'])
@login_required
def delete_post(id):
    post = Post.get_post(id)

    db.session.delete(post)
    db.session.commit()

    
    flash('deleted post!')

    return redirect(url_for('main.index'))
    

@main.route('/delete_comment/<id>', methods=['GET', 'POST'])
@login_required
def delete_comment(id):
    comment = Comment.query.filter_by(id=id).first()
    post_id = comment.post

    Comment.delete_comment(id)

    flash('comment deleted!') 

    return redirect(url_for('main.index', id =post_id ))

@main.route('/post/<int:id>')
def single_post(id):
    post = Post.query.get(id)
    if post is None:
        abort(404)
    format_post = markdown2.markdown(post.post,extras=["code-friendly", "fenced-code-blocks"])
    return render_template('post.html',post = post,format_post=format_post)

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    myposts = Post.query.order_by(Post.posted.desc()).all()

    return render_template("profile/profile.html", user = user, myposts = myposts )


@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)

@main.route('/post/<int:id>/update_post',methods = ['GET','POST'])
@login_required
def update_post(id):

    post = Post.query.filter_by(id=id).first()

    form = PostForm()

    if form.validate_on_submit():
        post.title = form.post_title.data
        post.post = form.post.data

        db.session.commit()

        return redirect(url_for('.index', id=id))

    elif request.method == 'GET':
        form.post_title.data == post.title
        form.post.data == post.post

    return render_template('new_post.html',post_form = form, id = id)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))

@main.route("/post/new/comment/<int:id>",methods=["GET","POST"])
def comment(id):
    
    post = Post.query.get(id)
    comment_form = CommentsForm()

    if id is None:
        abort(404)

    if comment_form.validate_on_submit():
        comments = comment_form.comment.data
        username = comment_form.author.data
        new_comment = Comment(comments = comments,post_id = id, username= username)

        #save
        new_comment.save_comment()
        return redirect(url_for('.comment',id=id))

    
    post_comments = Comment.query.filter_by(post_id=id).order_by(Comment.posted.desc()).all()


    title = f'{post.title} comment'
    return render_template("new_comment.html",post = post, id=id,title = title,comment_form = comment_form, post_comments = post_comments)

@main.route('/comment/<int:id>')
def single_comment(id):
    comment = Comment.query.get(id)
    if comment is None:
        abort(404)
    format_comment = markdown2.markdown(comment.comment,extras=["code-friendly", "fenced-code-blocks"])
    return render_template('comment.html',comment = comment,format_comment=format_comment)
