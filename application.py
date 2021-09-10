from flask import Flask, flash, render_template, request, session, redirect, url_for
import flask_login
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps

#------Configs------#
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True 
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False 
app.config["SESSION_TYPE"] = "filesystem"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

MySession = sessionmaker()
Base = declarative_base()

engine = create_engine('sqlite:///data.db')
Base.metadata.create_all(bind=engine)
MySession.configure(bind=engine)
session = MySession()
Session(app)
#------------------#

#--------Routes---------#
@app.route("/")
def index():
    if flask_login.current_user.is_authenticated:
        return render_template("index.html", 
            username = flask_login.current_user.username, 
            total_books = flask_login.current_user.total_books, 
            total_pages = flask_login.current_user.total_pages)
    else:
        return redirect("/login")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        name = request.form.get("name").strip()
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if len(name) == 0 or len(password) == 0 or len(confirmation) == 0:
            return render_template("apology.html", message="Fill in all the fields")
        
        if password != confirmation:
            return render_template("apology.html", message="Passwords don't match")
        
        if User.findUser("username", name) != None:
            return render_template("apology.html", message="Username taken")
        
        user = User(name, password)
        flask_login.login_user(user)
        return redirect("/")
        

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        name = request.form.get("name").strip()
        password = request.form.get("password")

        if len(name) == 0 or len(password) == 0:
            return render_template("apology.html", message="Fill in all the fields")
        
        user = User.checkUser(name, password)

        if user == False:
            return render_template("apology.html", message="Password or username wrong. Are you already registered?")
        else:
            flask_login.login_user(user)
            return redirect("/")

@app.route("/logout")
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return redirect("/")

@app.route("/add", methods=["GET", "POST"])
@flask_login.login_required
def add():
    if request.method == 'GET':
        return render_template("add.html")
    else:
        user_id = flask_login.current_user.id
        title = request.form.get('title').strip()
        author = request.form.get('author').strip()
        pages = request.form.get('pages').strip()
        rating = request.form.get('rating')
        month = request.form.get('month')
        year = request.form.get('year').strip()

        if len(title) == 0 or len(author) == 0 or len(pages) == 0 or len(rating) == 0 or len(month) == 0 or len(year) == 0:
            return render_template("apology_home.html", message="Fill in all the fields")

        if Book.findBook(title, author) != None:
            return render_template("apology_home.html", message="Book already added")
        else:
            Book(user_id, title, author, pages, rating, month, year)
            return redirect("/")

@app.route("/library", methods=["GET", "POST"])
@flask_login.login_required
def library():
    if request.method == 'GET': 
        current_session = sessionmaker()
        current_session.configure(bind=engine)
        sess = current_session()
        user_id = flask_login.current_user.id
        books = sess.query(Book).filter_by(user_id=user_id).order_by(Book.year.desc()).order_by(Book.month.desc()).all()
        if len(books) == 0:
            return render_template("apology_home.html", message="You haven't added any books yet")
        return render_template("library.html", books=books)
    else:
        rating_f = request.form.get("rating_filter")
        month_f = request.form.get("month_filter")
        year_f = request.form.get("year_filter")

        current_session = sessionmaker()
        current_session.configure(bind=engine)
        sess = current_session()

        # only rating filter entered
        if rating_f != 'None':
            if month_f != 'None':
                if len(year_f) > 0:
                    books = sess.query(Book).filter_by(user_id=flask_login.current_user.id).filter_by(rating=rating_f).filter_by(year=year_f).filter_by(month=month_f).order_by(Book.year.desc()).order_by(Book.month.desc()).all()
                    return render_template("library.html", books=books)
                books = sess.query(Book).filter_by(user_id=flask_login.current_user.id).filter_by(rating=rating_f).filter_by(month=month_f).order_by(Book.year.desc()).order_by(Book.month.desc()).all()
                return render_template("library.html", books=books)
            if len(year_f) > 0:
                books = sess.query(Book).filter_by(user_id=flask_login.current_user.id).filter_by(rating=rating_f).filter_by(year=year_f).order_by(Book.year.desc()).order_by(Book.month.desc()).all()
                return render_template("library.html", books=books)    
            books = sess.query(Book).filter_by(user_id=flask_login.current_user.id).filter_by(rating=rating_f).order_by(Book.year.desc()).order_by(Book.month.desc()).all()      
            return render_template("library.html", books=books)
        
        if month_f != 'None':
            if len(year_f) > 0:
                books = sess.query(Book).filter_by(user_id=flask_login.current_user.id).filter_by(month=month_f).filter_by(year=year_f).order_by(Book.year.desc()).order_by(Book.month.desc()).all()
                return render_template("library.html", books=books)    
            books = sess.query(Book).filter_by(user_id=flask_login.current_user.id).filter_by(month=month_f).order_by(Book.year.desc()).order_by(Book.month.desc()).all()
            return render_template("library.html", books=books)

        if len(year_f) > 0:
            books = sess.query(Book).filter_by(user_id=flask_login.current_user.id).filter_by(year=year_f).order_by(Book.year.desc()).order_by(Book.month.desc()).all()
            return render_template("library.html", books=books)

        
        return redirect("/library")
            
            
        
def rating_f(rating_f):
    current_session = sessionmaker()
    current_session.configure(bind=engine)
    sess = current_session()
    
    books = sess.query(Book).filter_by(user_id=flask_login.current_user.id).filter_by(rating=rating_f).order_by(Book.year.desc()).order_by(Book.month.desc())
    return books

def month_f(month_f):
    current_session = sessionmaker()
    current_session.configure(bind=engine)
    sess = current_session()
    
    books = sess.query(Book).filter_by(user_id=flask_login.current_user.id).filter_by(month=month_f).order_by(Book.year.desc()).order_by(Book.month.desc())
    return books

def year_f(year_f):
    current_session = sessionmaker()
    current_session.configure(bind=engine)
    sess = current_session()
    
    books = sess.query(Book).filter_by(user_id=flask_login.current_user.id).filter_by(year=year_f).order_by(Book.year.desc()).order_by(Book.month.desc())
    return books



           



@app.route("/search", methods=["GET", "POST"])
@flask_login.login_required
def search():
    if request.method == "GET":
        return render_template("search.html")
    else:
        current_session = sessionmaker()
        current_session.configure(bind=engine)
        sess = current_session()
        
        user_id = flask_login.current_user.id
        books = sess.query(Book).filter_by(user_id=user_id).all()

        title = request.form.get("title").strip()
        author = request.form.get("author").strip()

        # only title entered
        if len(author) == 0 and len(title) > 0:
            books = sess.query(Book).filter_by(user_id=user_id).filter_by(title=title).all()
            if len(books) == 0:
                return render_template("apology_home.html", message="No match found")
            else:
                return render_template("library.html", books=books)
        
        # only author entered
        if len(title) == 0 and len(author) > 0:
            books = sess.query(Book).filter_by(user_id=user_id).filter_by(author=author).all()
            if len(books) == 0:
                return render_template("apology_home.html", message="No match found")
            else:
                return render_template("library.html", books=books)
        
        # both entered
        if len(title) > 0 and len(author) > 0:
            books = sess.query(Book).filter_by(user_id=user_id).filter_by(author=author).filter_by(title=title).all()
            if len(books) == 0:
                return render_template("apology_home.html", message="No match found")
            else:
                return render_template("library.html", books=books)
        
        #both empty
        if len(title) == 0 and len(author) == 0:
                return render_template("apology_home.html", message="You have to enter something")

@app.route("/remove/<id>")
@flask_login.login_required
def remove(id):
    book = Book.find_by_id(id)
    book.removeBook()
    return redirect("/library")


#-----------------#

#------Login Manager------#
@login_manager.user_loader
def load_user(user_id):
    return User.findUser("id", int(user_id))

def unauthorized():
    return redirect("/")
login_manager.unauthorized_handler(unauthorized)
#-------------------------#

#-------User class------#
class User(flask_login.UserMixin, Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    passwordhash = Column(String, nullable=False)
    total_books = Column(Integer, nullable=False, default=0)
    total_pages = Column(Integer, nullable=False, default=0)

    def __init__(self, username, password, addToDatabase=True):        
        self.username = username
        self.passwordhash = generate_password_hash(password)
        if addToDatabase:
            User.addUser(self)
    
    def addUser(self):
        session.add(self)
        session.commit()
        
    
    def removeUser(self):
        session.delete(self)
        session.commit()
    
    def findUser(Type, Value):
        Type = str.lower(Type)
        if (Type == "username"):
            with MySession() as sess:
                user = sess.query(User).filter_by(username = Value).first()
        if (Type == "id"):
            with MySession() as sess:
                user = sess.query(User).filter_by(id = Value).first()
        return user
    
    def checkUser(username, password):
        user = User.findUser("username", username)
        if user == None:
            return False
        if check_password_hash(user.passwordhash, password):
            return user
        else:
            return False
    
    def updateBookCount(self, add=True):
        username = flask_login.current_user.username
        if not add:
            session.query(User).filter(User.username == username).update({
                User.total_books: User.total_books - 1
            }, synchronize_session=False) 
        else:
            session.query(User).filter(User.username == username).update({
                User.total_books: User.total_books + 1
            }, synchronize_session=False) 
        session.commit()
    
    def updatePageCount(self, pages, add=True):
        username = flask_login.current_user.username
        if not add:
            session.query(User).filter(User.username == username).update({
                User.total_pages: User.total_pages - pages
            }, synchronize_session=False)
        else:
            session.query(User).filter(User.username == username).update({
                User.total_pages: User.total_pages + pages
            }, synchronize_session=False)
        session.commit()
    
    def currentUser(self):
        return [self.username, self.total_books, self.total_pages]
#----------------------------#

#--------Book Class----------#
class Book(flask_login.UserMixin, Base):
    __tablename__ = 'Books'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('User.id'))
    title = Column(String, nullable= False)
    author = Column(String, nullable=False)
    pages = Column(Integer, nullable=False)
    rating = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)

    def __init__(self, user_id, title, author, pages, rating, month, year, addToDatabase=True):
        self.user_id = user_id
        self.title = title 
        self.author = author
        self.pages = int(pages)
        self.rating = int(rating)
        self.month = int(month)
        self.year = int(year)
        if addToDatabase:
            Book.addBook(self)
    
    def addBook(self):
        flask_login.current_user.updateBookCount()
        flask_login.current_user.updatePageCount(self.pages)
        session.add(self)
        session.commit()
    
    def removeBook(self):
        flask_login.current_user.updateBookCount(add=False)
        flask_login.current_user.updatePageCount(self.pages, add=False)
        session.delete(self)
        session.commit()
    
    def findBook(title, author):
        for i in session.query(Book).filter_by(title=title).all():
            for x in session.query(Book).filter_by(author=author).all():
                if x == i:
                    return x 
        return None

    def find_by_id(id):
        return session.query(Book).filter_by(id=id).first()
    
    def currentBook(self):
        dic = {
            'id' : self.id,
            'user_id' : self.user_id,
            'title' : self.title,
            'author' : self.author,
            'pages' : self.pages,
            'rating' : self.rating,
            'month' : self.month,
            'year' : self.year
        }
        return dic
    
    def allBooks(user_id):
        book_list = []
        for book in session.query(Book).filter_by(user_id=user_id).all():
            book_list.append(book.currentBook())
        return book_list
