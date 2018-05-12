from flask import Flask, request, redirect, render_template, flash
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
    title = db.Column(db.Text(150))
    body = db.Column(db.Text(700))
    date = db.Column(db.DateTime)
     
    def __init__(self, title, body ):
        self.title = title
        self.body = body
        self.date = datetime.utcnow()

    def is_valid(self):
        if self.title and self.body:
            return True
        else:
            return False

@app.route('/')
def index():
    return redirect("/blog")


@app.route('/blog')
def blog():
    blog_id = request.args.get('id')
    if (blog_id):
        blog = Blog.query.get(blog_id)
        return render_template('post.html', title="Blog Post", post=post)

    sort = request.args.get('sort')
    if (sort=="newest"):
        blog = Blog.query.order_by(Blog.date.desc()).all()
    else:
        blog = Blog.query.all()   
    return render_template('blog.html', title="All Entries", blog=blog) 



@app.route('/new_post', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        
        new_post_title = request.form['title']
        new_post_body = request.form['body']
        new_post = Blog(new_post_title, new_post_body)

        new_post_title_error = ""
        new_post_body_error = ""
        
        if new_post_title == "":
            return "Error - Please add a title to your entry!"
        elif new_post_body == "":
            return "Error - Please add text to the post box!"

        elif new_post.is_valid():
            db.session.add(new_post)
            db.session.commit()
            
            
            url = "/blog?id" + str(new_post.id)
            return redirect(url)

        else:
            return render_template('newpost.html', 
                title="Enter a new Blog Post", 
                new_post_title=new_post_title, 
                new_post_body=new_post_body,
                new_post_title_error=new_post_title_error,
                new_post_body_error=new_post_body_error)

    else:
        return render_template('newpost.html', title="Enter a new Blog Post")


if __name__ == '__main__':
    app.run()       
