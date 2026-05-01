# Calculadora Remota com Sockets

Um sistema cliente-servidor que implementa uma **calculadora remota** utilizando sockets TCP em Python. O servidor usa threads para atender múltiplos clientes simultaneamente. As requisições também são feitas usando multithreading.

## Descrição

Este projeto demonstra a comunicação entre cliente e servidor usando sockets. O servidor executa operações matemáticas simples e envia os resultados para o cliente.

## Funcionalidades

O servidor suporta as seguintes operações matemáticas:

- **add**: Adição de dois números
- **subtract**: Subtração de dois números
- **multiply**: Multiplicação de dois números
- **divide**: Divisão de dois números (com validação para divisão por zero)

## Estrutura do Projeto

- **server.py** - Servidor que recebe requisições e executa operações matemáticas
- **client.py** - Cliente que envia requisições e exibe os resultados
- **constCS.py** - Constantes de configuração (HOST e PORT)
- **README.md** - Este arquivo

## Execução

Testar com dois servidores simultâneos:

```bash
# Terminal 1 - Servidor 1
PORT=5678 python3 server.py

# Terminal 2 - Servidor 2
PORT=5679 python3 server.py

# Terminal 3 - Cliente
python3 client.py
```

## Protocolo de Comunicação

O cliente envia requisições no formato:
```
operacao|valor1|valor2
```

Exemplos:
- `add|10|5`
- `subtract|20|8`
- `multiply|7|6`
- `divide|100|4`
- `power|2|10`
- `modulo|17|5`

O servidor responde com um JSON contendo o resultado ou mensagem de erro:
```json
{"resultado": 15, "operacao": "add", "valor1": 10, "valor2": 5}
```

## Configuração

Edite o arquivo `constCS.py` para mudar o IP do seu HOST e PORT escolhida:
```python
HOST = '127.0.0.1'  # ou '192.168.1.10' para rede local
PORT = 5678
PORT2 = 5679
```
