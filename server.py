from flask import Flask, render_template, request
import psycopg2
import psycopg2.extras
import os

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

#conn = psycopg2.connect(dbname="blog", user="conzty01")
conn = psycopg2.connect(os.environ["DATABASE_URL"])

@app.route("/")
def index():
    c = conn.cursor()
    a = conn.cursor()
    t = conn.cursor()
    c.execute("""
    SELECT posts.image, posts.image_alt, posts.title, posts.date, posts.abstract, posts.id, tg
    FROM posts JOIN
        (SELECT post_tags.post_id, array_agg(tags.name) AS tg
        FROM post_tags JOIN tags ON (post_tags.tag_id = tags.id)
        GROUP BY post_tags.post_id) AS t ON posts.id = t.post_id
    ORDER BY posts.date DESC;
    """)

    a.execute("SELECT id, image, image_alt, title, date FROM posts ORDER BY date DESC;")
    t.execute("SELECT id, name FROM tags ORDER BY name ASC;")
    return render_template("index.html",posts=c.fetchall(),archive=a.fetchall(),passiveTags=t.fetchall(),activeTags=())

@app.route("/post/<pid>")
def post(pid):
    c = conn.cursor()
    a = conn.cursor()
    t = conn.cursor()
    s = conn.cursor()
    c.execute("""
    SELECT posts.image, posts.image_alt, posts.title, posts.date, posts.body, posts.id, tg
    FROM posts JOIN
        (SELECT post_tags.post_id, array_agg(tags.name) AS tg
        FROM post_tags JOIN tags ON (post_tags.tag_id = tags.id)
        GROUP BY post_tags.post_id) AS t ON posts.id = t.post_id
    WHERE id = %s;
    """, (pid))

    a.execute("SELECT id, image, image_alt, title, date FROM posts ORDER BY date DESC;")
    t.execute("""SELECT tags.id, tags.name
                 FROM tags JOIN post_tags ON (tags.id = post_tags.tag_id)
                 WHERE post_tags.post_id != %s
                 ORDER BY name ASC;""", (pid))
    s.execute("""SELECT tags.id, tags.name
                 FROM tags JOIN post_tags ON (tags.id = post_tags.tag_id)
                 WHERE post_tags.post_id = %s
                 ORDER BY name ASC;""", (pid))
    return render_template("post.html",post=(c.fetchone(),),archive=a.fetchall(),passiveTags=t.fetchall(), activeTags=s.fetchall())

@app.route("/tag/<tname>")
def tags(tname):
    c = conn.cursor()
    a = conn.cursor()
    t = conn.cursor()
    s = conn.cursor()
    c.execute("""
    SELECT posts.image, posts.image_alt, posts.title, posts.date, posts.abstract, posts.id, tg
    FROM posts JOIN
        (SELECT post_tags.post_id, array_agg(tags.name) AS tg
        FROM post_tags JOIN tags ON (post_tags.tag_id = tags.id)
        GROUP BY post_tags.post_id) AS t ON posts.id = t.post_id
    WHERE %s = ANY (tg);
    """, (tname,))

    a.execute("SELECT id, image, image_alt, title, date FROM posts ORDER BY date DESC;")
    t.execute("SELECT * FROM tags WHERE name != %s ORDER BY name ASC;", (tname,))
    s.execute("SELECT * FROM tags WHERE name = %s ORDER BY name ASC;", (tname,))
    return render_template("post.html",post=c.fetchall(),archive=a.fetchall(),passiveTags=t.fetchall(), activeTags=s.fetchall())

if __name__ == "__main__":
    app.run(debug=True)
