from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255))

    users = db.relationship('User', backref = 'role', lazy = "dynamic")
    

    def __repr__(self):
        return f'User {self.name}'


class User(UserMixin,db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index = True)
    email = db.Column(db.String(255),unique = True,index = True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    pass_secure = db.Column(db.String(255))

    posts = db.relationship('Post', backref = 'user', lazy = "dynamic")
    comments = db.relationship('Comment',backref = 'user',lazy = "dynamic")

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls,id):
        comments = Comment.query.filter_by(post_id=id).all()
        
        return comments

    @property
    def password(self):
        raise AttributeError('password attribute not readable')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)

    def __repr__(self):
        return f'User {self.username}'


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(255))
    post = db.Column(db.String())
    author=db.Column(db.String(250))
    posted = db.Column(db.DateTime,default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))

    comments = db.relationship("Comment", backref ="post_name", lazy = "dynamic")


    def save_post(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def clear_posts(cls):
        Post.all_posts.clear()

    @classmethod
    def get_posts(cls,title):
        posts = Post.query.filter_by(title = title).all()
        return posts

    @classmethod
    def get_post(cls,id):
        post = Post.query.filter_by(id=id).first()

        return post

class Comment(db.Model):
    
    __tablename__ = 'comments'

    id = db.Column(db.Integer,primary_key = True)
    comments= db.Column(db.String)
    post_id = db.Column(db.Integer)
    username = db.Column(db.String)
    posted = db.Column(db.DateTime,default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    post = db.Column(db.Integer, db.ForeignKey("posts.id"))
    

    def save_comment(self):
        '''
        Function that saves each post's comments
        '''
        db.session.add(self)
        db.session.commit()

    @classmethod
    def clear_comments(cls):
        Comment.all_comments.clear()

    @classmethod
    def get_comments(cls,post):
        comments = Comment.query.filter_by(post_name=post).all()

        return comments

    @classmethod
    def delete_comment(cls,id):
       comment = Comment.query.filter_by(id=id).first()
       db.session.delete(comment)
       db.session.commit()

class Email(db.Model):
    __tablename__='emails'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    email_data = db.Column(db.String(255))

    def save_email(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def send_single_email(cls,id):
        email = Email.query.filter_by(id=id).first()
        return email