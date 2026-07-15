import urllib.request
import json
import time

BASE_URL = "http://127.0.0.1:5000"

def make_request(path, method="GET", data=None):
    url = f"{BASE_URL}{path}"
    headers = {"Content-Type": "application/json"}
    
    body = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode("utf-8")), response.status
    except urllib.error.HTTPError as e:
        return json.loads(e.read().decode("utf-8")), e.code

def run_tests():
    print("--- Iniciando Testes do Estudo de Caso ---\n")

    # 1. Criar Serviço
    print("1. Criando Servico...")
    service_data = {
        "nome": "Instalacao",
        "descricao": "Instalacao de equipamentos",
        "preco_base": 150.0
    }
    res, code = make_request("/services", "POST", service_data)
    print(f"Status: {code}")
    print(f"Resposta: {json.dumps(res, indent=2)}\n")
    service_id = res.get("data", {}).get("id")

    # 2. Listar Serviços
    print("2. Listando Serviços...")
    res, code = make_request("/services", "GET")
    print(f"Status: {code}")
    print(f"Resposta: {json.dumps(res, indent=2)}\n")

    # 3. Criar Ordem de Serviço
    if service_id:
        print(f"3. Criando Ordem de Serviço para o serviço ID {service_id}...")
        order_data = {
            "descricao": "Instalar roteador",
            "status": "aberta",
            "service_id": service_id
        }
        res, code = make_request("/orders", "POST", order_data)
        print(f"Status: {code}")
        print(f"Resposta: {json.dumps(res, indent=2)}\n")

    # 4. Listar Ordens de Serviço
    print("4. Listando Todas as Ordens de Serviço...")
    res, code = make_request("/orders", "GET")
    print(f"Status: {code}")
    print(f"Resposta: {json.dumps(res, indent=2)}\n")

    # 5. Listar Ordens de um Serviço Específico (Consulta de Domínio)
    if service_id:
        print(f"5. Listando Ordens do Serviço ID {service_id}...")
        res, code = make_request(f"/services/{service_id}/orders", "GET")
        print(f"Status: {code}")
        print(f"Resposta: {json.dumps(res, indent=2)}\n")

    # 6. Testar Erro: Criar Ordem para Serviço Inexistente
    print("6. Testando Erro: Criar Ordem para Serviço ID 999 (Inexistente)...")
    bad_order_data = {
        "descricao": "Teste Inexistente",
        "status": "aberta",
        "service_id": 999
    }
    res, code = make_request("/orders", "POST", bad_order_data)
    print(f"Status: {code}")
    print(f"Resposta: {json.dumps(res, indent=2)}\n")

if __name__ == "__main__":
    # Pequena espera para o servidor carregar completamente se necessário
    time.sleep(1)
    run_tests()
