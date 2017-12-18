import psycopg2
import os

def createPosts(cursor):
    cursor.execute("DROP TABLE IF EXISTS posts CASCADE;")
    cursor.execute("""

    CREATE TABLE posts (
        id              serial,
        title           varchar(200),
        date            date,
        image           varchar(200),
        body            text,
        PRIMARY KEY (id)
    );

    """)
def createTags(cursor):
    cursor.execute("DROP TABLE IF EXISTS tags CASCADE;")
    cursor.execute("""

    CREATE TABLE tags (
        id              serial,
        name            varchar(50),
        PRIMARY KEY (id)
    );

    """)
def createPost_Tag(cursor):
    cursor.execute("DROP TABLE IF EXISTS post_tags")
    cursor.execute("""

    CREATE TABLE post_tags (
        post_id          int,
        tag_id           int,
        PRIMARY KEY (post_id,tag_id),
        FOREIGN KEY (post_id) REFERENCES posts(id),
        FOREIGN KEY (tag_id) REFERENCES tags(id)
    );

    """)

def run():
    conn = psycopg2.connect(os.environ["DATABASE_URL"])
    #conn = psycopg2.connect(dbname="blog", user="conzty01")
    cur = conn.cursor()

    print("creating 'posts' table")
    createPosts(cur)
    print("creating 'tags' table")
    createTags(cur)
    print("creating 'post_tag' table")
    createPost_Tag(cur)
    print("commiting tables")
    conn.commit()
    print("finished creation")

if __name__ == "__main__":
    run()
