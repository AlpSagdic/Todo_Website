from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = "YOU_CHOOSE_A_SECRET_KEY"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

#We used it to create the database.
#with app.app_context():
#    db.create_all()


@app.route("/")
def home():
    todos = Todo.query.all()
    return render_template("index.html", todos=todos)


@app.route("/complete/<string:id>")
def complete_todo(id):
    todo = Todo.query.filter_by(id=id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/add", methods=["POST"])
def add_todo():
    title = request.form.get("title")
    new_todo = Todo(
        title=title,
        complete=False
    )
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/delete/<string:todo_id>")
def delete_todo(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
