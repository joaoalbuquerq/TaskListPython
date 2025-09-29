from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import psycopg2
import psycopg2.extras
from psycopg2 import sql

# Configurações do banco
DB_NAME = "tarefas_db"
USER = "postgres"      
PASSWORD = "rfB6J84WJH29"  
HOST = "10.2.1.11"
PORT = "5432"

def criarBanco():
    conn = psycopg2.connect(dbname="postgres", user=USER, password=PASSWORD, host=HOST, port=PORT)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", [DB_NAME])
    exists = cur.fetchone()
    if not exists:
        cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DB_NAME)))
        print(f"Banco '{DB_NAME}' criado com sucesso!")
    else:
        print(f"Banco '{DB_NAME}' já existe.")

    cur.close()
    conn.close()

def criarTabelas():
    conn = psycopg2.connect(dbname=DB_NAME, user=USER, password=PASSWORD, host=HOST, port=PORT)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS tarefas (
            id SERIAL PRIMARY KEY,
            titulo VARCHAR(255) NOT NULL,
            descricao TEXT,
            status VARCHAR(50) DEFAULT 'pendente',
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("Tabela 'tarefas' pronta para uso!")

def inicializarBanco():
    criarBanco()
    criarTabelas()


def get_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT
)

class ServidorTarefas(BaseHTTPRequestHandler):
    def _set_headers(self, status=200, content_type="application/json"):
        self.send_response(status)
        self.send_header("Content-type", content_type)
        self.end_headers()

    def do_GET(self):
        conn = get_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        if self.path == "/tarefas":
            cur.execute("SELECT * FROM tarefas ORDER BY id")
            tarefas = cur.fetchall()
            self._set_headers()
            self.wfile.write(json.dumps(tarefas, default=str).encode())
        
        elif self.path.startswith("/tarefas/"):
            try:
                tarefa_id = int(self.path.split("/")[-1])
                cur.execute("SELECT * FROM tarefas WHERE id = %s", (tarefa_id,))
                tarefa = cur.fetchone()
                if tarefa:
                    self._set_headers()
                    self.wfile.write(json.dumps(tarefa, default=str).encode())
                else:
                    self._set_headers(404)
                    self.wfile.write(b'{"erro": "Tarefa nao encontrada"}')
            except ValueError:
                self._set_headers(400)
                self.wfile.write(b'{"erro": "ID invalido"}')

        cur.close()
        conn.close()
    
    def do_POST(self):
        if self.path == "/tarefas":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode()
            dados = json.loads(body)

            conn = get_connection()
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            cur.execute(
                "INSERT INTO tarefas (titulo, descricao, status) VALUES (%s, %s, %s) RETURNING *",
                (dados.get("titulo"), dados.get("descricao"), dados.get("status", "pendente"))
            )
            nova_tarefa = cur.fetchone()
            conn.commit()

            self._set_headers(201)
            self.wfile.write(json.dumps(nova_tarefa, default=str).encode())

            cur.close()
            conn.close()
    
    def do_DELETE(self):
        if self.path.startswith("/tarefas/"):
            try:
                tarefa_id = int(self.path.split("/")[-1])

                conn = get_connection()
                cur = conn.cursor()

                cur.execute("DELETE FROM tarefas WHERE id = %s RETURNING id", (tarefa_id,))
                deletada = cur.fetchone()
                conn.commit()

                if deletada:
                    self._set_headers(204)
                    self.wfile.write(b"")
                else:
                    self._set_headers(404)
                    self.wfile.write(b'{"erro": "Tarefa nao encontrada"}')

                cur.close()
                conn.close()

            except ValueError:
                self._set_headers(400)
                self.wfile.write(b'{"erro": "ID invalido"}')

    
        def do_PUT(self):

            if self.path.startswith("/tarefas/"):
                try:
                    tarefa_id = int(self.path.split("/")[-1])
                    content_length = int(self.headers.get("Content-Length", 0))
                    body = self.rfile.read(content_length).decode()
                    dados = json.loads(body)

                    conn = get_connection()
                    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

                    cur.execute(
                        "UPDATE tarefas SET titulo = COALESCE(%s, titulo), descricao = COALESCE(%s, descricao), status = COALESCE(%s, status) WHERE id = %s RETURNING *",
                        (dados.get("titulo"), dados.get("descricao"), dados.get("status"), tarefa_id)
                    )
                    tarefa_atualizada = cur.fetchone()
                    conn.commit()

                    if tarefa_atualizada:
                        self._set_headers()
                        self.wfile.write(json.dumps(tarefa_atualizada, default=str).encode())
                    else:
                        self._set_headers(404)
                        self.wfile.write(b'{"erro": "Tarefa nao encontrada"}')

                    cur.close()
                    conn.close()

                except ValueError:
                    self._set_headers(400)
                    self.wfile.write(b'{"erro": "ID invalido"}')


if __name__ == "__main__":

    inicializarBanco()
    servidor = HTTPServer(("localhost", 8000), ServidorTarefas)
    print("Servidor rodando em http://localhost:8000")
    servidor.serve_forever()