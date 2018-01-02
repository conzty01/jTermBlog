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
    a = conn.cursor()
    t = conn.cursor()
    c.execute("""
    SELECT posts.images, posts.image_alt, posts.title, posts.date, posts.abstract, posts.id, tg
    FROM posts JOIN
        (SELECT post_tags.post_id, array_agg(tags.name) AS tg
        FROM post_tags JOIN tags ON (post_tags.tag_id = tags.id)
        GROUP BY post_tags.post_id) AS t ON posts.id = t.post_id
    ORDER BY posts.date DESC
    LIMIT (7);
    """)

    temp = c.fetchall()
    if len(temp) != 7:
        nextButton = True
    else:
        nextButton = False

    a.execute("SELECT id, images, image_alt, title, date FROM posts ORDER BY date DESC;")
    t.execute("SELECT id, name FROM tags ORDER BY name ASC;")
    return render_template("index.html",posts=temp,archive=a.fetchall(),passiveTags=t.fetchall(),
                                        activeTags=(),disNextB=nextButton,disPrevB=True)

@app.route("/page/<num>")
def gotoPage(num):
    c = conn.cursor()
    a = conn.cursor()
    t = conn.cursor()
    c.execute("""
    SELECT posts.images, posts.image_alt, posts.title, posts.date, posts.abstract, posts.id, tg
    FROM posts JOIN
        (SELECT post_tags.post_id, array_agg(tags.name) AS tg
        FROM post_tags JOIN tags ON (post_tags.tag_id = tags.id)
        GROUP BY post_tags.post_id) AS t ON posts.id = t.post_id
    ORDER BY posts.date DESC;
    """)

    num = int(num)
    items = c.fetchall()
    if (num-1)*6 > len(items):
        temp = items[(num-2)*7:num*7]
        nextButton = True
        prevButton = False
    elif num - 1 < 0:
        temp = items[num*7:(num+1)*7]
        nextButton = False
        prevButton = True
    elif num - 1 == 0:
        temp = items[(num-1)*7:num*7]
        nextButton = False
        prevButton = True
    else:
        temp = items[(num-1)*7:num*7]
        nextButton = False
        prevButton = False

    if num*7 > len(items):
        nextButton = True

    a.execute("SELECT id, images, image_alt, title, date FROM posts ORDER BY date DESC;")
    t.execute("SELECT id, name FROM tags ORDER BY name ASC;")
    return render_template("index.html",posts=temp,archive=a.fetchall(),passiveTags=t.fetchall(),
                                        activeTags=(),disNextB=nextButton,disPrevB=prevButton)

@app.route("/post/<pid>")
def post(pid):
    c = conn.cursor()
    a = conn.cursor()
    t = conn.cursor()
    s = conn.cursor()
    c.execute("""
    SELECT posts.images, posts.image_alt, posts.title, posts.date, posts.body, posts.id, tg, posts.abstract
    FROM posts JOIN
        (SELECT post_tags.post_id, array_agg(tags.name) AS tg
        FROM post_tags JOIN tags ON (post_tags.tag_id = tags.id)
        GROUP BY post_tags.post_id) AS t ON posts.id = t.post_id
    WHERE id = %s;
    """, (pid,))

    a.execute("SELECT id, images, image_alt, title, date FROM posts ORDER BY date DESC;")
    t.execute("""SELECT id, name FROM tags
                 WHERE name NOT IN (SELECT tags.name
                                    FROM tags JOIN post_tags ON (tags.id = post_tags.tag_id)
                                    WHERE post_tags.post_id = %s
                                    ORDER BY name ASC)
                 ORDER BY name ASC;""",(pid,))
    s.execute("""SELECT tags.id, tags.name
                 FROM tags JOIN post_tags ON (tags.id = post_tags.tag_id)
                 WHERE post_tags.post_id = %s
                 ORDER BY name ASC;""", (pid,))
    return render_template("post.html",posts=(c.fetchone(),),archive=a.fetchall(),passiveTags=t.fetchall(),
                                       activeTags=s.fetchall(),disNextB=True,disPrevB=True)

@app.route("/tag/<tname>")
def tags(tname):
    c = conn.cursor()
    a = conn.cursor()
    t = conn.cursor()
    s = conn.cursor()
    c.execute("""
    SELECT posts.images, posts.image_alt, posts.title, posts.date, posts.abstract, posts.id, tg
    FROM posts JOIN
        (SELECT post_tags.post_id, array_agg(tags.name) AS tg
        FROM post_tags JOIN tags ON (post_tags.tag_id = tags.id)
        GROUP BY post_tags.post_id) AS t ON posts.id = t.post_id
    WHERE %s = ANY (tg)
    ORDER BY posts.date DESC;
    """, (tname,))

    a.execute("SELECT id, images, image_alt, title, date FROM posts ORDER BY date DESC;")
    t.execute("SELECT * FROM tags WHERE name != %s ORDER BY name ASC;", (tname,))
    s.execute("SELECT * FROM tags WHERE name = %s ORDER BY name ASC;", (tname,))
    return render_template("post.html",posts=c.fetchall(),archive=a.fetchall(),passiveTags=t.fetchall(),
                                       activeTags=s.fetchall(),disNextB=True,disPrevB=True)

# Error Handling

@app.errorhandler(404)
def error404(e):
    print(e)
    t = "What you were looking for cannot be found."
    return render_template("error.html",e=e,text=t), 404
@app.errorhandler(500)
def error500(e):
    print(e)
    t = "Something went wrong on our end. We'll get to work on it right away!"
    return render_template("error.html",e="Internal Server Error",text=t), 500
@app.errorhandler(410)
def error410(e):
    print(e)
    t = "The item you were looking for has been deleted."
    return render_template("error.html",e=e,text=t), 410
@app.errorhandler(403)
def error403(e):
    print(e)
    t = "This is not the page you're looking for"
    return render_template("error.html",e=e,text=t), 403

if __name__ == "__main__":
    app.run(debug=True)
