import uploadProjects
def main():
    print("main")
    f = open("post.txt","r")
    if f.read() != "NONE":
        ("new post")
        f.close()
        uploadProjects.run()
    else:
        print("no new post")
        f.close()
main()
