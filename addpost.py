import psycopg2

def main():
	conn = psycopg2.connect(dbname="blog", user="conzty01")
	#conn = psycopg2.connect(os.environ["DATABASE_URL"])

	

if _name__ == "__main__":
	main()
