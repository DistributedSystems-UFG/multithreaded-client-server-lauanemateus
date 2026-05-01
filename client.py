from socket import *
from constCS import *
import json
import threading
import random
import time

lock = threading.Lock()
OPERAÇÕES = ["add", "subtract", "multiply", "divide"]

def gerar_requisicao_aleatoria():
    """Gera uma requisição aleatória"""
    operacao = random.choice(OPERAÇÕES)
    valor1 = random.randint(1, 100)
    valor2 = random.randint(1, 100) if operacao != "divide" else random.randint(2, 100)
    return f"{operacao}|{valor1}|{valor2}", operacao, valor1, valor2

def enviar_requisicao(thread_id, host, port):
    """Envia uma requisição em uma thread separada"""
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((host, port))
    
    requisicao, op, v1, v2 = gerar_requisicao_aleatoria()
    
    s.send(str.encode(requisicao))
    data = s.recv(1024)
    resposta = json.loads(bytes.decode(data))
    
    with lock:
        if "erro" not in resposta:
            print(f"[T{thread_id}] {v1} {op} {v2} = {resposta['resultado']}")
        else:
            print(f"[T{thread_id}] Erro: {resposta['erro']}")
    
    s.close()

def main():
    """Cliente que cria threads para enviar requisições para 2 servidores"""
    print(f"\n{'='*60}")
    print(f"Cliente Multithread - 60 Requisições (2 Servidores)")
    print(f"{'='*60}\n")
    
    servidores = [
        (HOST, PORT, "S1"),
        (HOST, PORT2, "S2")
    ]
    
    requisicoes_por_servidor = 30
    threads = []
    tempo_inicio = time.time()
    
    thread_id = 1
    # Criar threads para cada servidor
    for host, port, id_serv in servidores:
        for i in range(requisicoes_por_servidor):
            thread = threading.Thread(
                target=enviar_requisicao,
                args=(thread_id, host, port),
                daemon=False
            )
            threads.append(thread)
            thread.start()
            thread_id += 1
    
    # Aguardar todas as threads
    for t in threads:
        t.join()
    
    tempo_total = time.time() - tempo_inicio
    total_requisicoes = len(servidores) * requisicoes_por_servidor
    
    print(f"\nESTATÍSTICAS")
    print(f"Tempo total: {tempo_total:.4f} segundos")
    print(f"Total de requisições: {total_requisicoes}")
    print(f"Taxa: {total_requisicoes / tempo_total:.2f} requisições/segundo")

if __name__ == "__main__":
    main()
