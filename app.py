from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from PyPDF2 import PdfReader
app = Flask(__name__)
app.config['UPLOAD_FOLDER']='uploads'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///resume.db'
app.config['SECRET_KEY']='secretkey'
db=SQLAlchemy(app)
resume_data={}
@app.route('/',methods=['GET','POST'])
def home():
    if request.method=='POST':
        resume=request.files['resume']
        if resume:
            file_path=f"{app.config['UPLOAD_FOLDER']}/{resume.filename}"
            resume.save(file_path)
            content=""
            if resume.filename.endswith('.pdf'):
                reader=PdfReader(file_path)
                for page in reader.pages:
                    text=page.extract_text()
                    if text:
                        content+=text
                        resume_data['content']=content
        else:
            with open(file_path,'r',encoding='utf-8') as file:
                content=file.read()

            return redirect('/dashboard')    
    return render_template('home.html')
@app.route('/dashboard')
def dashboard():
    content=resume_data.get('content','')
    return render_template('dashboard.html',content=content)
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