import smtplib


from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from helpers import apology
from secrets import token_urlsafe
from db import User, db_session


app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOADED"] = True


app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


domain = "http://127.0.0.1:5000/"
HOST = "smtp.gmail.com"
SUBJECT = "Your magic link"
FROM = "max.test.python3.8@gmail.com"
server = smtplib.SMTP('smtp.gmail.com: 587')
server.starttls()
server.login("max.test.python.3.8@gmail.com", "SeMe4Ka229")


@app.route("/")
def index():
    if session.get("user_id") is None:
        return redirect("/register")
    user = db_session.query(User).filter_by(token=session.get("user_id")).first()
    return render_template("index.html", id=session.get("user_id"), email=user.email, counter=user.counter)


@app.route("/register")
def register():
    return render_template("register.html", register="register")


@app.route("/registered", methods=["GET", "POST"])
def registered():
    if request.method == "GET":
        return redirect("/register")
    email = request.form.get("email")
    token = token_urlsafe(8)
    emails = db_session.query(User.email).all()
    if (email, ) in emails:
        return apology("This email has been registered")
    new_user = User(email=email, token=token, counter=0)
    db_session.add(new_user)
    db_session.commit()
    body = "\r\n".join(("From: %s" % FROM,
                        "To: %s" % email,
                        "Subject: %s" % SUBJECT,
                        "",
                        f"Your magic link is {domain}login/{token}"
                        ))
    try:
        server.sendmail(FROM, [email], body)
        server.quit()
    except:
        return apology("Something went wrong")
    return redirect(f"/login/{token}")


@app.route("/login/<string:token>")
def login(token):
    if (token, ) not in db_session.query(User.token).all():
        return apology("Your magic link is incorrect")
    user = db_session.query(User).filter_by(token=token).first()
    user.counter += 1
    db_session.commit()
    session["user_id"] = token
    return redirect("/")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == '__main__':
    app.run()

