import requests

BASE_URL = "http://127.0.0.1:5000"

score = 0


def print_result(name, success):
    global score
    if success:
        print(f"[✔] {name}")
        score += 3
    else:
        print(f"[✘] {name}")


# 🧩 1. Criar usuário
def test_create_user():
    r = requests.post(f"{BASE_URL}/users", json={
        "nome": "Teste",
        "email": "teste@email.com",
        "senha": "123456"
    })
    ok = r.status_code in [200, 201]
    print_result("Criar usuário", ok)

    if ok:
        return r.json()["data"]["id"]
    return None


# 🧩 2. Listar usuários
def test_list_users():
    r = requests.get(f"{BASE_URL}/users")
    ok = r.status_code == 200 and isinstance(r.json()["data"], list)
    print_result("Listar usuários", ok)


# 🧩 3. Criar mensagem válida
def test_create_message(user_id):
    r = requests.post(f"{BASE_URL}/messages", json={
        "content": "Mensagem teste",
        "user_id": user_id
    })
    ok = r.status_code in [200, 201]
    print_result("Criar mensagem válida", ok)

    if ok:
        return r.json()["data"]["id"]
    return None


# 🧩 4. Criar mensagem com usuário inválido
def test_invalid_user_message():
    r = requests.post(f"{BASE_URL}/messages", json={
        "content": "Erro",
        "user_id": 9999
    })
    ok = r.status_code == 404
    print_result("Erro mensagem com usuário inválido", ok)


# 🧩 5. Listar mensagens
def test_list_messages():
    r = requests.get(f"{BASE_URL}/messages")
    ok = r.status_code == 200 and isinstance(r.json()["data"], list)
    print_result("Listar mensagens", ok)


# 🧩 6. Endpoint domínio
def test_messages_by_user(user_id):
    r = requests.get(f"{BASE_URL}/users/{user_id}/messages")
    ok = r.status_code == 200 and isinstance(r.json()["data"], list)
    print_result("Mensagens por usuário", ok)


# 🧩 7. Atualizar usuário
def test_update_user(user_id):
    r = requests.patch(f"{BASE_URL}/users/{user_id}", json={
        "nome": "Atualizado"
    })
    ok = r.status_code == 200
    print_result("Atualizar usuário", ok)


# 🧩 8. Deletar usuário
def test_delete_user(user_id):
    r = requests.delete(f"{BASE_URL}/users/{user_id}")
    ok = r.status_code == 204
    print_result("Deletar usuário", ok)


# 🧩 9. Validação (senha curta)
def test_validation():
    r = requests.post(f"{BASE_URL}/users", json={
        "nome": "Erro",
        "email": "email@email.com",
        "senha": "123"
    })
    ok = r.status_code == 400
    print_result("Validação senha", ok)


# 🧩 10. Rota inexistente
def test_404():
    r = requests.get(f"{BASE_URL}/rota-invalida")
    ok = r.status_code == 404
    print_result("Rota inexistente", ok)


# 🚀 Execução

print("\n🚀 Iniciando testes (User + Message)...\n")

user_id = test_create_user()

test_list_users()

if user_id:
    test_create_message(user_id)
    test_messages_by_user(user_id)
    test_update_user(user_id)

test_invalid_user_message()
test_list_messages()
test_validation()
test_404()

if user_id:
    test_delete_user(user_id)

print(f"\n🎯 Pontuação final: {score}/30\n")