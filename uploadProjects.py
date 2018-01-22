import psycopg2
import os
from PIL import Image

PROJECT_ROOT = os.getcwd()

def parsePostFile(filename):
    pList = []
    with open(filename,"r") as postFile:
        pDict = {}
        for line in postFile:
            if "~~~" in line:
                pList.append(pDict)
                pDict = {}
            else:
                p = line.split("::")
                #print("======",p)
                pDict[p[0]] = p[-1][:-1]
                if p[0] == "images":
                    pDict[p[0]] = p[-1][:-1].split(", ")
                if p[0] == "tags":
                    #print("In Tags")
                    pDict[p[0]] = p[-1][:-1].split(", ")
                if pDict[p[0]] == '':
                    pDict[p[0]] = None

    #print(pList)
    return pList

def enterPost(cur, projectDict):
    try:
        executeStr = "INSERT INTO posts (title, date, images, image_alt, abstract, body) VALUES (%s,TO_DATE(%s, 'Month DD, YYYY'),%s,%s,%s,%s);"
        cur.execute(executeStr,(projectDict['title'],projectDict['date'],projectDict['images'],projectDict['image_alt'],projectDict['abstract'],projectDict['body']))
    except psycopg2.IntegrityError:
        print("DUPLICATE POST: '{}' on {}".format(projectDict["title"],projectDict["date"]))

def enterTags(cur, projectDict):
    if "tags" in projectDict.keys():
        cur.execute("SELECT * FROM tags;")
        tagList = [tup[-1] for tup in cur.fetchall()]
        #print(tagList)

        print(projectDict["tags"])

        for t in projectDict["tags"]:
            if t not in tagList:
                #print(t)
                cur.execute("INSERT INTO tags (name) VALUES ('{}')".format(t))

def enterPost_Tags(cur, projectDict):
    for t in projectDict["tags"]:
        #print(t)
        try:
            cur.execute("""
            INSERT INTO post_tags (post_id, tag_id) VALUES (
                (SELECT id FROM posts
                WHERE title = %s AND date = TO_DATE(%s, 'Month DD, YYYY') LIMIT(1)),
                (SELECT id FROM tags
                WHERE name = %s)
            );
            """, (projectDict["title"],projectDict["date"],t))
        except psycopg2.IntegrityError:
            print("DUPLICATE TAG: postTitle: '{}' tagName: '{}'".format(projectDict["title"],t))

def createImages():
        optWidth = 1000                                                                 # Optimized width (width of image to$
        thumbWidth = 50                                                                 # Thumbnail width (width of image to$

        IMAGE_DIR = os.path.join(PROJECT_ROOT,"static/images")
        UPLOADS_DIR = os.path.join(IMAGE_DIR,"uploads")
	l = os.listdir(os.path.join(PROJECT_ROOT,"static/images/uploads/"))
	l.remove(".gitkeep")

        for pic in l:
                img = Image.open(os.path.join(UPLOADS_DIR,pic))
                optWpercent = (optWidth/float(img.size[0]))                             # Optimized width percent
                thumbWpercent = (thumbWidth/float(img.size[0]))                         # Thumbnail width percent

                # Optimized
                hsize = int((float(img.size[1])*float(optWpercent)))
                optImg = img.resize((optWidth,hsize), Image.ANTIALIAS)
                optImg.save(os.path.join(os.path.join(IMAGE_DIR,"opt"),pic))

                # Thumbnail
                hsize = int((float(img.size[1])*float(optWpercent)))
                thumbImg = img.resize((optWidth,hsize), Image.ANTIALIAS)
                thumbImg.save(os.path.join(os.path.join(IMAGE_DIR,"thumb"),pic))

                img.close()
                os.rename(os.path.join(UPLOADS_DIR,pic),os.path.join(IMAGE_DIR,os.path.join("orig",pic)))
                #os.remove(os.path.join(UPLOADS_DIR,pic))
def run():
    conn = psycopg2.connect(os.environ["DATABASE_URL"])
    #conn = psycopg2.connect(dbname="blog", user="conzty01")
    cur = conn.cursor()
    print("running")

    projectList = parsePostFile("post.txt")
    for item in projectList:
        print("tags", item["title"])
        enterTags(cur, item)
        print("post", item["title"])
        enterPost(cur, item)
        print("post_tags", item['title'])
        enterPost_Tags(cur, item)

    conn.commit()
    createImages()
    print("finished")

if __name__ == "__main__":
    run()
