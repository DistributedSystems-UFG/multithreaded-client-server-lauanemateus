# Calculadora Remota com Sockets

Um sistema cliente-servidor que implementa uma **calculadora remota** utilizando sockets TCP em Python com **arquitetura multithreading**.

## Descrição

Este projeto demonstra a comunicação entre cliente e servidor usando sockets com processamento paralelo via threads. O servidor recebe conexões em uma thread principal e dispara uma nova thread para atender cada cliente. O cliente cria uma thread para cada requisição, permitindo envios paralelos para múltiplos servidores.

## Arquitetura de Multithreading

### Servidor
- **Thread Principal**: Aguarda e aceita conexões de clientes
- **Thread por Cliente**: Cada conexão aceita gera uma nova thread que processa requisições

### Cliente
- **60 Threads Paralelas**: Uma para cada requisição (30 por servidor)
- **2 Servidores**: 30 requisições para o servidor 1, 30 para o servidor 2
- **Processamento Paralelo**: Todas as threads executam simultaneamente

## Funcionalidades

O servidor suporta as seguintes operações matemáticas:

- **add**: Adição de dois números
- **subtract**: Subtração de dois números
- **multiply**: Multiplicação de dois números
- **divide**: Divisão de dois números (com validação para divisão por zero)

## Estrutura do Projeto

- **server.py** - Servidor multithreaded que recebe requisições e executa operações
- **client.py** - Cliente que cria 60 threads para enviar requisições para 2 servidores em paralelo
- **constCS.py** - Constantes de configuração (HOST, PORT e PORT2)
- **README.md** - Este arquivo

## Execução

### Com dois servidores (recomendado):

```bash
# Terminal 1 - Servidor 1
python3 server.py

# Terminal 2 - Servidor 2
PORT=5679 python3 server.py

# Terminal 3 - Cliente
python3 client.py
```

O cliente criará 60 threads: 30 enviando requisições para o servidor 1 (port 5678) e 30 para o servidor 2 (port 5679).

### Com um único servidor:

```bash
# Terminal 1 - Servidor
python3 server.py

# Terminal 2 - Cliente
python3 client.py
```

## Resultado Esperado

Ao executar o cliente, você verá algo semelhante a:
```
============================================================
Cliente Multithread - 60 Requisições (2 Servidores)
============================================================

[T1] 45 add 23 = 68.0
[T2] 12 divide 3 = 4.0
[T3] 78 multiply 5 = 390.0
[T4] 30 subtract 10 = 20.0
...

ESTATÍSTICAS
Tempo total: 0.0088 segundos
Total de requisições: 60
Taxa: 6842.44 requisições/segundo
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

O servidor responde com um JSON contendo o resultado ou mensagem de erro:
```json
{"resultado": 15, "operacao": "add", "valor1": 10, "valor2": 5}
```

## Configuração

Edite o arquivo `constCS.py` para mudar o IP do HOST e as PORTs:
```python
HOST = '192.168.1.10'  # IP do servidor
PORT = 5678             # Porta do servidor 1
PORT2 = 5679            # Porta do servidor 2
```
