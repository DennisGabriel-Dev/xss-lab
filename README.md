# XSS Demo App (Intencionalmente Vulnerável)

> ⚠️ **Aviso importante**: Esta aplicação foi criada **apenas para fins educacionais** em laboratório controlado.
> Não use em ambientes de produção ou sistemas expostos à internet sem proteção.

Aplicação web simples (guestbook) com backend Flask + SQLite e frontend HTML/CSS/JS, contendo:

- **Stored XSS** (comentários armazenados no banco e renderizados sem sanitização)
- **Reflected XSS** (parâmetro de URL refletido diretamente em HTML)

---

## Tecnologias

- Python 3.11
- Flask
- Flask-CORS
- SQLite
- HTML/CSS/JavaScript
- Docker

---

## Estrutura do projeto

```bash
.
├── app.py
├── Dockerfile
├── requirements.txt
├── README.md
├── xss_payloads.md
├── static/
│   ├── app.js
│   └── style.css
└── templates/
    └── index.html
```

---

## Como executar com Docker

### 1) Build da imagem

```bash
docker build -t xss-demo-app .
```

### 2) Rodar o container

Mapeando porta **5003** externa para a porta **5000** interna do Flask:

```bash
docker run --rm -p 5003:5000 --name xss-demo xss-demo-app
```

### 3) Acessar no navegador

```text
http://localhost:5003
```

---

## Rotas principais

- `GET /` → interface do guestbook
- `GET /api/comments` → lista comentários
- `POST /api/comments` → salva comentário
- `GET /search?q=...` → página vulnerável a Reflected XSS

---

## Demonstração de Stored XSS

1. Abra `http://localhost:5003`
2. No campo de mensagem, envie um payload (ver `xss_payloads.md`)
3. Ao carregar os comentários, o script será executado no navegador

Exemplo rápido:

```html
<script>alert('Stored XSS')</script>
```

---

## Demonstração de Reflected XSS

Acesse diretamente uma URL com payload no parâmetro `q`:

```text
http://localhost:5003/search?q=<script>alert('Reflected XSS')</script>
```

A página reflete o parâmetro sem escape, executando o script.

---

## Observações didáticas

- A aplicação **não sanitiza** entrada de usuário por design.
- O frontend usa `innerHTML` para renderização dos comentários.
- O endpoint `/search` insere diretamente o valor de `q` no HTML retornado.
- CORS está habilitado para facilitar integração frontend/backend em cenário de laboratório.

---

## Sugestões para aula

1. Mostrar o funcionamento normal da aplicação
2. Inserir payload Stored XSS e recarregar comentários
3. Abrir URL de Reflected XSS
4. Discutir mitigação (escape de saída, CSP, sanitização, HttpOnly, validações)

---

## Limpeza

Para parar o container: `Ctrl + C` no terminal onde está rodando.

Se quiser remover imagem:

```bash
docker rmi xss-demo-app
```
