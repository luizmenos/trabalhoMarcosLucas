# Projeto de Processamento de Imagens com Redis e Docker

Este projeto demonstra um sistema distribuído simples para processamento de imagens utilizando **Redis** como fila de mensagens e **Docker Compose** para orquestrar os containers.  

O funcionamento é o seguinte:

- Uma **Redis queue** armazena as imagens a serem processadas.
- O container **image_producer** pega as imagens da pasta `data/input` e as enfileira na fila do Redis.
- Os **workers** (configurados com 3 réplicas no `docker-compose.yml`) consomem as imagens da fila, aplicam **escala de cinza** e salvam o resultado em `data/output`.

---

## Pré-requisitos

- Python 3.x
- Pip
- Docker e Docker Compose
- Biblioteca **Pillow** para manipulação de imagens:

```bash
pip install pillow
```

---

# Passo a passo pra rodar o projeto

**1. Gerar imagens**

  Na raiz do projeto, execute o arquivo `gerar_imagens.py` para criar 30 imagens aleatórias na pasta `/data/input` 
  ```bash 
  python gerar_imagens.py
  ```

**2. Rodar o sistema no Docker Compose**

  Ainda na raiz, execute:
  ```bash
  docker-compose up --build
  ```

  * O container `image_producer` vai enfileirar todas as imagens do `/data/input` na queue do redis
  * Os workers vão consumir as imagens, aplicar a escala de cinza e salvar em `/data/output/`

# Estrutura do Projeto
```bash
/projeto
├── app/
│   ├── main.py           # Enfileirador de imagens
│   ├── config.py
│   ├── requirements.txt
│   └── Dockerfile
├── worker/
│   ├── worker.py         # Worker que processa imagens
│   ├── config.py
│   ├── requirements.txt
│   └── Dockerfile
├── data/
│   ├── input/            # Imagens de entrada
│   └── output/           # Imagens processadas
├── gerar_imagens.py      # Gera 30 imagens aleatórias
└── docker-compose.yml
```
