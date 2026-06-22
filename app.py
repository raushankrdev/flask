from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


#SQLite configuration
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

db= SQLAlchemy(app)

#Task Model
class Task(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200), nullable=False)
    description=db.Column(db.Text)
    due_date=db.Column(db.String(50))
    status=db.Column(db.String(20))

    def __repr__(self):
        return f'{self.title}'
    
#Home page
@app.route('/')
def home():
    tasks = Task.query.order_by(Task.id.desc()).all()

    print("tasks******", tasks)

    for task in tasks:
        print(task.title)
        print(task.due_date)
    
    return render_template('index.html', tasks=tasks)

#Add Task page
@app.route('/add', methods= ['GET', 'POST'])
def gettask():

    if request.method == 'POST':
    
        title = request.form['title']
        description = request.form['description']
        due_date = request.form['due_date']
        #status= request.form['status']


        print(title,description,due_date)
        # errrrrrr

        task= Task(
            title= title,
            description= description,
            due_date= due_date,
            #status= status
            )
        db.session.add(task)
        db.session.commit()
        return redirect('/')
    
    return render_template("add_task.html")

@app.route('/get-task', methods=['GET'])
def Taskdata():
    profiles=Task.query.all()
    print("profiles***", profiles)
    data= []
    for profile in profiles:
        print(
            profile.id,
            profile.title,
            profile.description,
            profile.due_date,
            profile.status
        )
        data.append(profile.id)
        data.append(profile.title)
        data.append(profile.description)
        data.append(profile.due_date)
        data.append(profile.status)
    return str(data)


# Update Task
@app.route('/update-task/<int:id>', methods=['GET', 'POST'])
def update_task(id):

    task = Task.query.get_or_404(id)
   


    task = Task.query.get_or_404(id)

    if request.method == 'POST':

        task.title = request.form['title']
        task.description = request.form['description']
        task.due_date = request.form['due_date']
        task.status = request.form['status']

        db.session.commit()

        return redirect('/')
    
    return render_template('update_task.html', task=task)



# Delete Task
@app.route('/delete-task/<int:id>', methods=['GET', 'POST'])
def delete_task(id):

    task = Task.query.get_or_404(id)

    db.session.delete(task)
    db.session.commit()

    return redirect('/')


if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    app.run(debug=True)
