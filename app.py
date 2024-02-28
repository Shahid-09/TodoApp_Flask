from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy # Sqlalchemy is a sql toolkit and ORM(Object Relational Mapping) that provide efficient and high performance relational database
from datetime import datetime          # Sqlaclchemy python ke through database me changes karne ki facility provide karta hai.

app = Flask(__name__) # This is flask instance name "app"

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db" # It is path of database and create database "todo"	
# The database URI that should be used for the connection
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app) # This is sqlalchemy instance name "db" and associate with "app"

    
class Todo(db.Model): # We create model to store data todo.db through db.Model.. (db.Model is base class of sqlalchemy for all model)
    # We define Schema through our class "Todo"
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
with app.app_context(): 
    db.create_all() 
# Use the app context to create all database tables based on the defined models, when db.Module run
    
@app.route('/', methods=['GET', 'POST']) #This is route for root url ('/')
def add_todo():
    if request.method=='POST': # Request use to access the data sent with http request.
        title = request.form['title']
        desc = request.form['desc']
    # If the request method is POST, retrieve data from the form, 
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
    # create a new Todo object, add it to the database session, and commit the changes.

    allTodo = Todo.query.all()
    return render_template('index.html', allTodo=allTodo) # allTodo is variable store in "allTodo" and we can display this in index.html file
    # Then, retrieve all the Todo objects from the database and render the index.html template with the data.

@app.route('/update/<int:sno>', methods=['GET', 'POST'])  # Define a route for the '/update/int:sno' URL (/update/ This is endpoint)
def update(sno):
    if request.method=='POST':
        # If the request method is POST, update the Todo object with the provided sno (serial number).
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
        # Redirect the user to the root URL(home)
    
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)
    # If the method is GET, retrieve the Todo object with the given sno and render the 'update.html' template with the data.

@app.route('/delete/<int:sno>') # Define a route for the '/delete/int:sno' URL
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    # Retrieve the Todo object with the specified sno, delete it from the database session, and commit the changes
    return redirect("/")
    # Redirect the user to the root URL(home)


if __name__ == "__main__":
    app.run(debug=True)
# We use debug true for find error and which type of we get it shows in browser
    
# what is jinja2 ?
# jinja2 is a template engine it is helpful creating flask app 

# what is the template base app ?
# An application template is a standard framework for users to employ when they create applications.
# In the application template, you can specify the application properties,
# environment properties, and environment gates for an application.

# In short, template-based apps focus on fixed templates for UI,
# while API-based apps use interfaces for flexible communication between different parts of the application.
# API-based apps are generally more adaptable and scalable.






