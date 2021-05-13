from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Programlar/YAZILIM/VS_Code_projeler/Python/todo-app/todo.db'
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    complete = db.Column(db.Boolean)

    
@app.route("/")
def index():
    todos = Todo.query.all()
    result = len(todos)
    return render_template("index.html", todos=todos,result=result)


# todo ekleme
@app.route("/add", methods=["POST"])
def addtodo():
    title = request.form.get("title")
    newtodo = Todo(title=title, complete=False)
    db.session.add(newtodo)
    db.session.commit()
    return redirect(url_for("index"))


# todo tamamlama
@app.route("/complete/<string:id>")
def complete(id):
    sorgu = Todo.query.filter_by(id=id).first()
    sorgu.complete = not sorgu.complete
    db.session.commit()
    return redirect(url_for("index"))

#todo hepsini tamamla
@app.route("/allcomplete")
def allcomplete():
    todos = Todo.query.all()
    for todo in todos:
        todo.complete = True
    db.session.commit()
    return redirect(url_for("index"))


#todo silme
@app.route("/delete/<string:id>")
def delete(id):
    sorgu = Todo.query.filter_by(id=id).first()
    db.session.delete(sorgu)
    db.session.commit()
    return redirect(url_for("index"))

#todo hepsini sil
@app.route("/alldelete", methods = ["GET","POST"] )
def alldelete():
    todos = Todo.query.all()
    for todo in todos:
        db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
