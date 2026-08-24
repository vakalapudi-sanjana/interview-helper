
from flask import Flask, render_template, request
from openai import OpenAI
import os

app = Flask(__name__)

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY
)


def interview_helper(role, experience, skills, interview_type):

    prompt = f"""
You are an expert interview preparation assistant.

Create a practical interview preparation guide for:

Job Role: {role}
Experience Level: {experience}
Skills: {skills}
Interview Type: {interview_type}

Give the answer in this structure:

1. Interview Overview

2. Top Interview Questions
Include 5 important questions.

3. Sample Answers
Give simple and clear answers.

4. Technical Questions
Include relevant technical questions based on the candidate's skills.

5. HR Questions
Include common HR questions with sample answers.

6. Interview Tips
Give practical tips for the candidate.

7. Common Mistakes to Avoid

Make the answers realistic, simple and easy to understand.
"""

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful interview preparation assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content


@app.route("/", methods=["GET", "POST"])
def home():

    result = ""

    if request.method == "POST":

        role = request.form.get("role", "")
        experience = request.form.get("experience", "")
        skills = request.form.get("skills", "")
        interview_type = request.form.get("interview_type", "")

        result = interview_helper(
            role,
            experience,
            skills,
            interview_type
        )

    return render_template(
        "index.html",
        result=result
    )
