from flask import Flask, render_template, request, session, redirect, url_for
import random

app=Flask(__name__)
app.secret_key='your_secret_key_here'  # Required for session

def load_words(filename):
    with open(filename,'r') as f:
        return [line.strip().lower() for line in f]

guesses=load_words("guesses.txt")
answers=load_words("answers.txt")

def evaluate_guess(guess, answer):
    result = ""
    for i in range(5):
        if guess[i] == answer[i]:
            result += f'<span style="color: #4CAF50; font-weight: bold; font-family: Monaco, monospace;">{guess[i]}</span>'
        elif guess[i] in answer:
            result += f'<span style="color: #FFB300; font-weight: bold; font-family: Monaco, monospace;">{guess[i]}</span>'
        else:
            result += f'<span style="color: #888888; font-family: Monaco, monospace;">{guess[i]}</span>'
    return result


@app.route("/", methods=["GET", "POST"])
def index():
    if "secret_word" not in session:
        session["secret_word"]=random.choice(answers)
        session["attempts"]=0
        session["history"]=[]

    if request.method=="POST":
        guess=request.form.get("guess", "").lower()

        if guess not in guesses:
            error="Invalid word!"
            with open("invalidguesses.txt",'a+') as obj:
                obj.write(guess)
            return render_template("index.html", error=error, history=session["history"])

        session["attempts"]+=1
        feedback=evaluate_guess(guess, session["secret_word"])
        session["history"].append(feedback)

        if guess==session["secret_word"]:
            message="🎉 You won!"
            history=session["history"]
            session.clear()
            return render_template("index.html", message=message, history=history)

        elif session["attempts"]>=6:
            message=f"😢 Game over! The word was {session['secret_word']}."
            history=session["history"]
            session.clear()
            return render_template("index.html", message=message, history=history)


    return render_template("index.html", history=session.get("history", []))

if __name__=="__main__":
    app.run(debug=True)


