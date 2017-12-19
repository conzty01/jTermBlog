from flask import Flask, render_template, request
import psycopg2
import psycopg2.extras
import os

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

conn = psycopg2.connect(dbname="blog", user="conzty01")
#conn = psycopg2.connect(os.environ["DATABASE_URL"])

@app.route("/")
def index():
    c = conn.cursor()
    c.execute("SELECT image, image_alt, title, date, abstract, id FROM posts ORDER BY id DESC;")
    return render_template("index.html",posts=c.fetchall())

@app.route("/post/<id>")
def post(id):
    c = conn.cursor()
    c.execute("SELECT image, image_alt, title, date, body FROM posts WHERE id=%s;",(id))
    a = conn.cursor()
    a.execute("SELECT id, image, image_alt, title, date FROM posts ORDER BY id DESC;")
    return render_template("post.html",post=c.fetchone(),archive=a.fetchall())

if __name__ == "__main__":
    app.run(debug=True)
