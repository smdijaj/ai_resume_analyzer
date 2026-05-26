from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from PyPDF2 import PdfReader
import re
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
app = Flask(__name__)
app.config['UPLOAD_FOLDER']='uploads'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///resume.db'
app.config['SECRET_KEY']='secretkey'
db=SQLAlchemy(app)
resume_data={}
skills_db=[ 'python','sql','flask','pandas','numpy','matplotlib','machine learning','html','css','javascript','git','github','bootstrap']
recommended_skills = ['python','sql','flask','pandas','numpy','matplotlib','machine learning','git','github','api','data analysis']
@app.route('/', methods=['GET', 'POST'])
def home():

    global resume_data

    if request.method == 'POST':

        resume = request.files['resume']

        if resume:

            file_path = f"{app.config['UPLOAD_FOLDER']}/{resume.filename}"

            resume.save(file_path)

            content = ""

            if resume.filename.endswith('.pdf'):

                reader = PdfReader(file_path)

                for page in reader.pages:

                    text = page.extract_text()

                    if text:

                        content += text

            else:

                with open(file_path, 'r', encoding='utf-8') as file:

                    content = file.read()

            lines = content.split('\n')

            name = "unknown"

            for line in lines:

                cleaned = line.strip()

                if len(cleaned) > 3:

                    name = cleaned

                    break

            emails = re.findall(r'[\w\.-]+@[\w\.-]+', content)

            email = emails[0] if emails else "not found"

            phones = re.findall(r'\+?\d[\d\s-]{8,15}', content)

            phone = phones[0] if phones else "not found"

            found_skills = []

            lower_content = content.lower()

            for skill in skills_db:

                if skill in lower_content:

                    found_skills.append(skill)
                    missing_skills = []

                    for skill in recommended_skills:

                        if skill not in found_skills:

                            missing_skills.append(skill)
            education_keywords = ['btech','bachelor','master','university','college','degree']

            education_found = []

            for word in education_keywords:

                if word in lower_content:

                    education_found.append(word)

            experience_keywords = ['intern','experience','developer','engineer','project']

            experience_found = []

            for word in experience_keywords:

                if word in lower_content:

                    experience_found.append(word)
            skills_score = min(len(found_skills) * 8, 40)
            email_score = 10 if email != "not found" else 0
            phone_score = 10 if phone != "not found" else 0
            education_score = 15 if education_found else 0
            experience_score = 15 if experience_found else 0
            word_count = len(content.split())
            content_score = 10 if word_count > 200 else 0
            score = (skills_score +email_score +phone_score + education_score +experience_score +content_score)
            score = min(score, 100)
            improvements = []
            if email == "not found":
                improvements.append("Add professional email address")
            if phone == "not found":

                improvements.append(
                "Add phone number"
            )
            if not education_found:

                improvements.append(
                "Add education details"
            )
            if not experience_found:

                improvements.append(
                "Add work experience or projects"
            )
            if len(found_skills) < 5:

                improvements.append(
                "Add more technical skills"
            )
            if len(found_skills) < 5:

                improvements.append(
                "Add more technical skills"
            )
            if word_count < 200:

                improvements.append(
                "Increase resume content and project details"
            )
            if 'github' not in lower_content:

                improvements.append(
                "Add GitHub profile link"
            )
            if found_skills:
                skill_values=np.ones(len(found_skills))
                plt.figure(figsize=(8,5))
                plt.bar(found_skills,skill_values)
                plt.title('Detected Skills')
                plt.xlabel('Skills')
                plt.ylabel('Presence')
                plt.xticks(rotation=30)
                plt.tight_layout()
                plt.savefig('static/skills_chart.png')
                plt.close()
            score_labels = ['Skills','Email','Phone','Education','Experience','Content']
            score_values = [skills_score,email_score,phone_score,education_score,experience_score,content_score]
            plt.figure(figsize=(8,5))
            plt.bar(score_labels,score_values)
            plt.title('ATS Score Breakdown')
            plt.xlabel('categories')
            plt.ylabel('score')
            plt.tight_layout()
            plt.savefig('static/score_chart.png')
            plt.close()
            resume_df=pd.DataFrame({'Category':score_labels,'Score':score_values})
            table_data=resume_df.to_dict(orient='records')
            resume_data = {
                'score':score,
                'skills_score': skills_score,
                'email_score': email_score,
                'phone_score': phone_score,
                'education_score': education_score,
                'experience_score': experience_score,
                'content_score': content_score,
                'content': content,
                'name': name,
                'email': email,
                'phone': phone,
                'skills': found_skills,
                'education': education_found,
                'experience': experience_found,
                'table_data':table_data
            }

            return redirect('/dashboard')

    return render_template('home.html')
@app.route('/dashboard')
def dashboard():
    return render_template(
        'dashboard.html',
        data=resume_data
    )
@app.route('/analytics')
def analytics():

    return render_template('analytics.html',data=resume_data)
@app.route('/improvements')
def improvements():
    return render_template('improvements.html',data=resume_data)
@app.route('/jobs')
def jobs():
    return render_template('jobs.html')
if __name__=='__main__':
    app.run(debug=True)