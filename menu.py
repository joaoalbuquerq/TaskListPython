import requests
import json

BASE_URL = "http://localhost:8000"

# Criar tarefa
def criar_tarefa():
    titulo = input("Digite o título da tarefa: ")
    descricao = input("Digite a descrição da tarefa (opcional): ")
    status = input("Digite o status (pendente/completo): ")

    payload = {"titulo": titulo, "descricao": descricao, "status": status}
    r = requests.post(f"{BASE_URL}/task", json=payload)

    print("Resposta:", r.status_code, r.text)

# Listar tarefas
def listar_tarefas():
    r = requests.get(f"{BASE_URL}/task")
    print("Resposta:", r.status_code)
    try:
        tarefas = r.json()
        for t in tarefas:
            print(f"[{t['id']}] {t['titulo']} | {t.get('descricao', '')} | Status: {t['status']} | Criado em: {t['criado_em']}")
    except:
        print(r.text)

# Detalhar tarefa
def detalhar_tarefa():
    tarefa_id = input("Digite o ID da tarefa: ")
    r = requests.get(f"{BASE_URL}/task/{tarefa_id}")
    print("Resposta:", r.status_code, r.text)

# Atualizar tarefa
def atualizar_tarefa():
    tarefa_id = input("Digite o ID da tarefa a atualizar: ")
    print("Deixe em branco os campos que não deseja alterar.")
    titulo = input("Novo título: ")
    descricao = input("Nova descrição: ")
    status = input("Novo status: ")

    payload = {}
    if titulo: payload["titulo"] = titulo
    if descricao: payload["descricao"] = descricao
    if status: payload["status"] = status

    r = requests.put(f"{BASE_URL}/task/{tarefa_id}", json=payload)
    print("Resposta:", r.status_code, r.text)

# Excluir tarefa
def excluir_tarefa():
    tarefa_id = input("Digite o ID da tarefa a excluir: ")
    r = requests.delete(f"{BASE_URL}/task/{tarefa_id}")
    print("Resposta:", r.status_code, r.text)

# Menu principal
def menu():
    while True:
        print("\n=== MENU PRINCIPAL ===")
        print("1 - Criar tarefa")
        print("2 - Listar todas as tarefas")
        print("3 - Atualizar uma tarefa")
        print("4 - Detalhar uma tarefa")
        print("5 - Excluir uma tarefa")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            criar_tarefa()
        elif opcao == "2":
            listar_tarefas()
        elif opcao == "3":
            atualizar_tarefa()
        elif opcao == "4":
            detalhar_tarefa()
        elif opcao == "5":
            excluir_tarefa()
        elif opcao == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida, tente novamente.")

if __name__ == "__main__":
    menu()
