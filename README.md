# Serviço Concorrente de Processamento de Imagens

**Disciplina:** Informática Industrial – ENE118  
**Integrantes:**
- Barbara Castro – 202169030B
- Barbara Salgado – [ ficticio ]

**Divisão de tarefas:**
- Barbara Castro: `imagem.py` e `cliente.py` (branch `cliente`)
- Barbara Salgado: `protocolo.py` e `servidor.py` (branch `servidor`)

---

## Instalação

```bash
pip install -r requirements.txt
```

---

## Como executar

Abre um terminal e roda o servidor:
```bash
py servidor.py
```

Abre outro terminal e roda o cliente:
```bash
py cliente.py
```

---

## Testes

### Teste 1 – Imagem com face
O servidor detectou a face e retornou a imagem com retângulo verde desenhado ao redor.  
![com face](tests/com_face.png)

### Teste 2 – Imagem sem face
Nenhuma face detectada, a imagem voltou sem nenhum retângulo.  
![sem face](tests/sem_face.png)

### Teste 3 – Dois clientes ao mesmo tempo
Coloquei um `time.sleep(5)` temporário no início do `atender_cliente`. Rodei dois clientes em terminais separados e o servidor mostrou dois "Iniciou" antes de qualquer "Terminou", confirmando que as threads rodam em paralelo.  
![dois clientes](tests/dois_clientes.png)

---

## Perguntas

**1. Onde o tamanho da imagem é enviado e como o laço sabe que recebeu tudo?**

Em `protocolo.py`, a `enviar_mensagem` empacota o tamanho em 4 bytes big-endian com `struct.pack('>I', tamanho)` e manda junto com os dados da imagem usando `sendall`. Na hora de receber, a `_ler_bytes` fica num loop acumulando o que chega até o total bater, porque o `recv` pode devolver menos do que o esperado de uma vez só.

**2. Onde a thread é criada e por que o servidor atende dois clientes ao mesmo tempo?**

Em `servidor.py`, depois do `s.accept()`, criei uma `threading.Thread` apontando pra `atender_cliente` e chamei `.start()`. O servidor não trava esperando aquele cliente terminar, volta pro `accept` e já pode pegar a próxima conexão.

**3. Um commit de cada integrante e a diferença entre commit, push e PR:**

- Commit de Barbara Castro (`7fc0afb`): "Configura caminho da imagem no cliente" – definiu a constante `CAMINHO_IMAGEM` em `cliente.py`.
- Commit de Barbara Salgado (`c7f0f81`): "Adiciona mensagem de inicio no servidor" – adicionou o print de status na thread do servidor.

`commit` salva as mudanças no repositório local. `push` envia esses commits pro GitHub. O **PR** é a forma de pedir pra integrar uma branch no `main`, mantendo o histórico completo sem squash.

---

## Uso de IA

Foi feito o uso de IA para ajudar a montar o laço de leitura completa em `protocolo.py` (a função `_ler_bytes`) e também pra me orientar nos comandos do terminal — como rodar o servidor e o cliente em janelas separadas, resolver erros de instalação do opencv e executar os testes. Precisei entender e conferir o trecho que acumula os chunks do `recv` até completar o total esperado, testando com imagens reais pra garantir que funcionava corretamente.
