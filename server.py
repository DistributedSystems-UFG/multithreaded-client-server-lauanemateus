from socket import *
from constCS import *
import json
import threading
import os

def processar_operacao(operacao, valor1, valor2):
    """
    Processa uma operação matemática e retorna o resultado.
    Operações suportadas: add, subtract, multiply, divide
    """
    valor1 = float(valor1)
    valor2 = float(valor2)
    
    if operacao == "add":
        resultado = valor1 + valor2
    elif operacao == "subtract":
        resultado = valor1 - valor2
    elif operacao == "multiply":
        resultado = valor1 * valor2
    elif operacao == "divide":
        if valor2 == 0:
            return {"erro": "Divisão por zero não permitida"}
        resultado = valor1 / valor2
    else:
        return {"erro": f"Operação '{operacao}' não reconhecida"}
    
    return {"resultado": resultado, "operacao": operacao, "valor1": valor1, "valor2": valor2}

def processar_requisicao(dados):
    """
    Processa requisição do cliente no formato: operacao|valor1|valor2
    """
    partes = dados.strip().split("|")
    if len(partes) != 3:
        return {"erro": "Formato inválido. Use: operacao|valor1|valor2"}
    
    operacao, valor1, valor2 = partes
    return processar_operacao(operacao, valor1, valor2)

def handle_cliente(conn, addr):
    """
    Função para lidar com cada cliente em uma thread separada
    """
    print(f"Conexão estabelecida com {addr}")
    
    while True:
        data = conn.recv(1024)
        
        if not data:
            break
        
        requisicao = bytes.decode(data).strip()
        print(f"Requisição recebida: {requisicao}")
        
        resposta = processar_requisicao(requisicao)
        resposta_json = json.dumps(resposta, ensure_ascii=False)
        
        print(f"Resposta enviada: {resposta_json}\n")
        conn.send(str.encode(resposta_json))
    
    print("Cliente desconectado")
    conn.close()

# Inicializando servidor
porta_servidor = int(os.getenv('PORT', PORT))

s = socket(AF_INET, SOCK_STREAM)
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
s.bind((HOST, porta_servidor))
s.listen(5)

print(f"Servidor iniciado em {HOST}:{porta_servidor}")
print("Aguardando conexões...\n")

try:
    while True:
        (conn, addr) = s.accept()
        thread_cliente = threading.Thread(target=handle_cliente, args=(conn, addr), daemon=True)
        thread_cliente.start()
except KeyboardInterrupt:
    print("\n\nServidor interrompido pelo usuário")
finally:
    s.close()
    print("Servidor encerrado")
