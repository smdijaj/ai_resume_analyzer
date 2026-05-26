from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///resume.db'
app.config['SECRET_KEY']='secretkey'
db=SQLAlchemy(app)
@app.route('/')
def home():
    return render_template('home.html')
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
@app.route('/analytics')
def analytics():
    return render_template('analytics.html')
@app.route('/improvements')
def improvements():
    return render_template('improvements.html')
@app.route('/jobs')
def jobs():
    return render_template('jobs.html')
if __name__=='__main__':
    app.run(debug=True)