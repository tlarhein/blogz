from flask import Flask, request, redirect, render_template, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['DEBUG'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:tc-lc101@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'cmarch102562tmarch041662'


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    body = db.Column(db.Text(700))
    date = db.Column(db.DateTime)
     
    def __init__(self, title, body, date=None):
        self.title = title
        self.body = body
        if date is None:
            date = datetime.utcnow()
        self.date = date

    def is_valid(self):
        if self.title and self.body:
            return True
        else:
            return False

@app.route('/')
def index():
    return redirect("/blog")


@app.route('/blog')                      #FOR ALL ENTRIES
def blog():
    if request.args:
        blog_id = request.args.get('id')
        blog_post = Blog.query.get(blog_id)
        return render_template('post.html', title="Single Blog Post", post=blog_post)

    blog_posts = Blog.query.order_by(Blog.date.asc()).all()
    return render_template('blog.html', title="Build-A-Blog Posts", posts=blog_posts)
    

@app.route('/new_post', methods=['GET', 'POST'])    #FOR NEW ENTRIES
def new_post():
    if request.method == 'POST':
        
        new_post_title = request.form['title']
        new_post_body = request.form['body']
        new_post = Blog(new_post_title, new_post_body)

        new_post_title_error = ""
        new_post_body_error = ""
        
        if new_post_title == new_post_title_error:
            return "Error - Please add a title AND post to your entry!"
        elif new_post_body == new_post_body_error:
            return "Error - Please add title AND post to your entry!"

        elif new_post.is_valid():
            db.session.add(new_post)
            db.session.commit()
            
            
            return redirect(url_for('new_post'))

        else:
            return render_template('newpost.html', 
                title="Enter a new Blog Post", 
                new_post_title=new_post_title, 
                new_post_body=new_post_body)

    else:
        return render_template('newpost.html', title="Blog Posts")


if __name__ == '__main__':
    app.run()       
