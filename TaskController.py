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


if __name__ == "__main__":
    servidor = HTTPServer(("localhost", 8000), ServidorTarefas)
    print("Servidor rodando em http://localhost:8000")
    servidor.serve_forever()