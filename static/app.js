const API_BASE = window.location.origin;

const form = document.getElementById("comment-form");
const commentsEl = document.getElementById("comments");

async function fetchComments() {
  const response = await fetch(`${API_BASE}/api/comments`);
  const comments = await response.json();

  if (!comments.length) {
    commentsEl.innerHTML = '<p class="empty">Ainda não há comentários.</p>';
    return;
  }

  // VULNERABILIDADE INTENCIONAL (Stored XSS):
  // message e author são inseridos diretamente com innerHTML.
  commentsEl.innerHTML = comments
    .map(
      (comment) => `
      <article class="comment">
        <div class="meta">#${comment.id} por ${comment.author} em ${comment.created_at}</div>
        <div class="message">${comment.message}</div>
      </article>
    `
    )
    .join("");
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const author = document.getElementById("author").value || "Anônimo";
  const message = document.getElementById("message").value;

  if (!message.trim()) {
    alert("Digite uma mensagem para enviar.");
    return;
  }

  await fetch(`${API_BASE}/api/comments`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ author, message }),
  });

  form.reset();
  await fetchComments();
});

fetchComments();
