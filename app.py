from flask import Flask, render_template, request, redirect, session
import json
import os

app = Flask(__name__)
app.secret_key = 'mysecretkey'

QUESTIONS = [
    "The quick brown fox jumps over the lazy dog.",
    "Photosynthesis converts sunlight into energy.",
    "Python is a high-level programming language."
]

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        session['username'] = username
        return redirect('/question/1')  # تغییر: هدایت به سوال ۱
    return render_template('login.html')

@app.route('/question/<int:qnum>', methods=['GET', 'POST'])
def single_question(qnum):
    if 'username' not in session:
        return redirect('/')

    username = session['username']
    question = QUESTIONS[qnum - 1]

    if request.method == 'POST':
        answer = request.form.get('answer')
        time_taken = int(request.form.get('time_taken'))

        # خواندن یا ساختن فایل جواب‌ها
        if os.path.exists("answers.json"):
            with open("answers.json", "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = {}

        if username not in data:
            data[username] = []

        data[username].append({
            "qnumber": qnum,
            "description": answer,
            "time_taken": time_taken
        })

        with open("answers.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        # سوال بعدی یا پایان
        if qnum < len(QUESTIONS):
            return redirect(f"/question/{qnum + 1}")
        else:
            return "✅ همه سوالات با موفقیت ثبت شدند!"

    return render_template("single_question.html", qnum=qnum, question=question)

if __name__ == '__main__':
    app.run(debug=True)
