from flask import Flask,render_template,jsonify,request
from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.orm import DeclarativeBase
from datetime import datetime
import os
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)


class Todo(db.Model):

    id = db.Column(db.Integer, primary_key=True)
   
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id
    
# delete if previously created
# try:
#     # run only once to create the database
#     db.create_all()
# except:
#     try:
#         db.drop_all()
#         db.create_all()
#     except Exception as e:
#         print(e)
#         None
#     # db.drop_all()
    

@app.route('/')
def hello():
    # count of todos
    todo = Todo(content="Hello World", completed=0)
    db.session.add(todo)
    db.session.commit()
        
    return {
            "message": "Hello, World!"
        }
       
@app.route("/all")
def all():
    todos = Todo.query.all()
    output = []
    for todo in todos:
        todo_data = {
            'id': todo.id,
            'content': todo.content,
            'completed': todo.completed,
            'createdAt': todo.createdAt
        }
        output.append(todo_data)
    return jsonify({'todos': output}) 


@app.route("/all/page")
def all_page():
    todos = Todo.query.all()
    output = []
    for todo in todos:
        todo_data = {
            'id': todo.id,
            'content': todo.content,
            'completed': todo.completed,
            'createdAt': todo.createdAt
        }
        output.append(todo_data)
    return render_template('todo.html', todos=sorted(output,key=lambda x: x['createdAt'], reverse=True))


@app.route('/home')
def home():
    return render_template('home.html')

    
    
@app.route("/upload",methods=['POST'])
def fileUpload():
    if "file" not in request.files:
        return "No file part in the request"
    file = request.files["file"]
    num_files = len(request.files)
    print(f"Number of files sent: {num_files}")
    print(request.files.values())
    
 
    if file.filename == "":
        return "No file selected"
    
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)  # Save the file to the configured upload folder
        return f"File successfully uploaded to {file_path}"


    
app.app_context().push()


if (__name__ == "__main__"):
    app.run(debug=True)
