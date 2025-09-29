from http.server import BaseHTTPRequestHandler, HTTPServer
import json

# "Banco de dados" em memória
tarefas = []
contador_id = 1


class ServidorTarefas(BaseHTTPRequestHandler):
    def _set_headers(self, status=200, content_type="application/json"):
        self.send_response(status)
        self.send_header("Content-type", content_type)
        self.end_headers()

    def do_GET(self):

        # ROTA PARA LISTAR TODAS AS TAREFAS
        if self.path == "/tarefas":
            self._set_headers()
            self.wfile.write(json.dumps(tarefas).encode())

        # ROTA PARA BUSCAR UMA TAREFA POR ID
        elif self.path.startswith("/tarefas/"):
            
            try:
                tarefa_id = int(self.path.split("/")[-1])
                tarefa = next((t for t in tarefas if t["id"] == tarefa_id), None)

                if tarefa:
                    self._set_headers()
                    self.wfile.write(json.dumps(tarefa).encode())
                else:
                    self._set_headers(404)
                    self.wfile.write(b'{"erro": "Tarefa nao encontrada"}')
                    
            except ValueError:
                self._set_headers(400)
                self.wfile.write(b'{"erro": "ID invalido"}')
    
    def do_POST(self):
        if self.path == "/tarefas":
            # Criar uma nova tarefa
            global contador_id
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode()
            dados = json.loads(body)

            nova_tarefa = {
                "id": contador_id,
                "titulo": dados.get("titulo", "Sem titulo"),
                "descricao": dados.get("descricao", "")
            }
            tarefas.append(nova_tarefa)
            contador_id += 1

            self._set_headers(201)
            self.wfile.write(json.dumps(nova_tarefa).encode())
    
    def do_DELETE(self):
        if self.path.startswith("/tarefas/"):
            try:
                tarefa_id = int(self.path.split("/")[-1])
                global tarefas
                tarefas = [t for t in tarefas if t["id"] != tarefa_id]

                self._set_headers(204)  # Sem conteúdo
                self.wfile.write(b"")

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

                for tarefa in tarefas:
                    if tarefa["id"] == tarefa_id:
                        tarefa["titulo"] = dados.get("titulo", tarefa["titulo"])
                        tarefa["descricao"] = dados.get("descricao", tarefa["descricao"])
                        self._set_headers()
                        self.wfile.write(json.dumps(tarefa).encode())
                        return

                self._set_headers(404)
                self.wfile.write(b'{"erro": "Tarefa nao encontrada"}')

            except ValueError:
                self._set_headers(400)
                self.wfile.write(b'{"erro": "ID invalido"}')


if __name__ == "__main__":
    servidor = HTTPServer(("localhost", 8000), ServidorTarefas)
    print("Servidor rodando em http://localhost:8000")
    servidor.serve_forever()