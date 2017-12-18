from flask import Flask, render_template, request
import psycopg2
import psycopg2.extras

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

conn = psycopg2.connect(dbname="blog", user="conzty01")
#conn = psycopg2.connect(os.environ["DATABASE_URL"])

@app.route("/")
def index():
    c = conn.cursor()
    v = conn.cursor()
    c.execute("SELECT * FROM posts ORDER BY (date) DESC;")
    v.execute("SELECT name FROM tags;")
    return render_template("index.html",posts=c.fetchall(),tags=v.fetchall())

@app.route("/<id>")
def post(id):
    c = conn.cursor()
    v = conn.cursor()
    c.execute("SELECT * FROM posts WHERE id=%d;",(int(id)))
    v.execute("SELECT name FROM tags;")
    return render_template("post.html",post=c.fetchall(),tags=v.fetchall())

if __name__ == "__main__":
    app.run(debug=True)
