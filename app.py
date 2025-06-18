from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 📍 Show where the database file is saved
print("📍 Database Location:", os.path.abspath("todo.db"))

# Todo model
class Todo(db.Model):
    Sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.Sno} - {self.title}"

# ✅ Home route: show all todos and handle add
@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
        print("✅ Added todo:", todo)
        return redirect(url_for('home'))

    all_todos = Todo.query.all()
    return render_template('index.html', todos=all_todos)

# ✅ Delete route
@app.route("/delete/<int:Sno>")
def delete(Sno):
    todo = Todo.query.get_or_404(Sno)
    db.session.delete(todo)
    db.session.commit()
    print("❌ Deleted todo:", todo)
    return redirect(url_for('home'))

# ✅ Update route
@app.route("/update/<int:Sno>", methods=['GET', 'POST'])
def update(Sno):
    todo = Todo.query.get_or_404(Sno)
    if request.method == 'POST':
        todo.title = request.form['title']
        todo.desc = request.form['desc']
        db.session.commit()
        print("✏️ Updated todo:", todo)
        return redirect(url_for('home'))
    return render_template('update.html', todo=todo)

# ✅ Run the app
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
