HOSTNAME = "localhost:3306"
DATABASE = "flask"
USERNAME = "web"
PASSWORD = "web"
DRIVER = "pymysql"

DB_URI = f"mysql+{DRIVER}://{USERNAME}:{PASSWORD}@{HOSTNAME}/{DATABASE}"
