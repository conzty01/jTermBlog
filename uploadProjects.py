import psycopg2

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
                pDict[p[0]] = p[-1][:-1]
                if pDict[p[0]] == '':
                    pDict[p[0]] = None

    #print(pList)
    return pList

def enterPost(cur, projectDict):
    executeStr = "INSERT INTO posts (title, date, image, body) VALUES (%s,TO_DATE(%s, 'Month DD, YYYY'),%s,%s);"
    cur.execute(executeStr,(projectDict['title'],projectDict['date'],projectDict['image'],projectDict['body']))

def run():
    #conn = psycopg2.connect(os.environ["DATABASE_URL"])
    conn = psycopg2.connect(dbname="blog", user="conzty01")
    cur = conn.cursor()

    projectList = parsePostFile("post.txt")
    for item in projectList:
        enterPost(cur, item)

    conn.commit()

if __name__ == "__main__":
    run()
