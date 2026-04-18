const API_BASE = window.location.origin;

const form = document.getElementById("comment-form");
const commentsEl = document.getElementById("comments");
document.cookie = "test=123";
function escapeHtml(value) {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

async function fetchComments() {
  const response = await fetch(`${API_BASE}/api/comments`);
  const comments = await response.json();

  if (!comments.length) {
    commentsEl.innerHTML = '<p class="empty">Ainda não há comentários.</p>';
    return;
  }

  commentsEl.innerHTML = comments
    .map(
      (comment) => `
      <article class="comment">
        <div class="meta">#${escapeHtml(comment.id)} por ${escapeHtml(comment.author)} em ${escapeHtml(comment.created_at)}</div>
        <div class="message">${escapeHtml(comment.message)}</div>
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
