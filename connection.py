import psycopg2

conn = psycopg2.connect(
    dbname="fin_flow_db",
    user="postgres",
    password="Ps1029384756,.",
    host="localhost",
    port="5432"
)

print()
