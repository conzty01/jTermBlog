import uploadProjects
def main():
    f = open("post.txt","r")
    if f.read() != "NONE":
        f.close()
        uploadProjects.run()
    else:
        f.close()            
main()
