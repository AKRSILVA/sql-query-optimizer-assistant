from database.connection import get_connection

def testar_conexao():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT current_database();")
    print(cur.fetchone()[0])

    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public';")
    print(cur.fetchall())

    cur.close()
    conn.close()

if __name__ == "__main__":
    testar_conexao()