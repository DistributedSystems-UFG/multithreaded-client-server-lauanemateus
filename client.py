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

def enviar_para_servidor(thread_id, num_requisicoes, host, port, id_servidor):
    """Envia requisições para um servidor específico em thread separada"""
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((host, port))
    
    with lock:
        print(f"[{id_servidor}-T{thread_id}] Conectado a {host}:{port}")
    
    for i in range(num_requisicoes):
        requisicao, op, v1, v2 = gerar_requisicao_aleatoria()
        
        s.send(str.encode(requisicao))
        data = s.recv(1024)
        resposta = json.loads(bytes.decode(data))
        
        if "erro" not in resposta:
            with lock:
                print(f"[{id_servidor}-T{thread_id}] {v1} {op} {v2} = {resposta['resultado']}")
    
    s.close()
    with lock:
        print(f"[{id_servidor}-T{thread_id}] Desconectado")

def main():
    """Cliente que conecta a dois servidores locais em paralelo"""
    print(f"\n{'='*60}")
    print(f"Cliente Multithread - Dois Servidores")
    print(f"{'='*60}\n")
    
    # Configuração dos dois servidores locais
    servidores = [
        ("127.0.0.1", 5678, "S1"),   # Servidor 1
        ("127.0.0.1", 5679, "S2"),   # Servidor 2
    ]
    
    threads_por_servidor = 3
    requisicoes_por_thread = 10
    
    threads = []
    tempo_inicio = time.time()
    
    # Criar threads para cada servidor
    for host, port, id_serv in servidores:
        for t in range(threads_por_servidor):
            thread = threading.Thread(
                target=enviar_para_servidor,
                args=(t + 1, requisicoes_por_thread, host, port, id_serv),
                daemon=False
            )
            threads.append(thread)
            thread.start()
    
    # Aguardar todas as threads
    for t in threads:
        t.join()
    
    tempo_total = time.time() - tempo_inicio
    total_threads = len(servidores) * threads_por_servidor
    total_requisicoes = total_threads * requisicoes_por_thread
    
    print(f"\nESTATÍSTICAS")
    print(f"Tempo total: {tempo_total:.4f} segundos")
    print(f"Total de requisições: {total_requisicoes}")
    print(f"Taxa: {total_requisicoes / tempo_total:.2f} requisições/segundo")

if __name__ == "__main__":
    main()
