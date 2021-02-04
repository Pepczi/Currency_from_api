from flask import Flask
from flask import request, render_template

app = Flask(__name__)

@app.route("/")
def main_page():
    return "Strona główna: Użyj /me, /contact"

@app.route("/me")
def me():
    print("GET /me")
    return render_template("me.html")

@app.route('/contact', methods=['GET', 'POST'])
def message():
   if request.method == 'GET':
       print("We received GET")
       return render_template("contact.html")
   elif request.method == 'POST':
       print("We received POST")
       print(request.form)
       return f'Dzięki za wiadomość {request.form}'