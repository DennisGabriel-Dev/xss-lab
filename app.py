import os
import sqlite3
from datetime import datetime

from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "comments.db")

app = Flask(__name__)
CORS(app)


def init_db() -> None:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            author TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/comments", methods=["GET"])
def list_comments():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, author, message, created_at FROM comments ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()

    comments = [dict(row) for row in rows]
    return jsonify(comments)


@app.route("/api/comments", methods=["POST"])
def create_comment():
    data = request.get_json(silent=True) or {}
    author = data.get("author", "Anônimo")
    message = data.get("message", "")

    if not message:
        return jsonify({"error": "Campo 'message' é obrigatório."}), 400

    now = datetime.utcnow().isoformat()

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO comments (author, message, created_at) VALUES (?, ?, ?)",
        (author, message, now),
    )
    conn.commit()
    comment_id = cur.lastrowid
    conn.close()

    return jsonify(
        {
            "id": comment_id,
            "author": author,
            "message": message,
            "created_at": now,
        }
    ), 201


@app.route("/search")
def reflected_search():
    q = request.args.get("q", "")

    # VULNERABILIDADE INTENCIONAL:
    # O valor de q é renderizado diretamente no HTML sem qualquer sanitização/escape.
    return f"""
    <!doctype html>
    <html lang=\"pt-BR\">
      <head>
        <meta charset=\"utf-8\">
        <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
        <title>Busca Vulnerável</title>
        <style>
          body {{ font-family: Arial, sans-serif; margin: 2rem; background: #0f172a; color: #e2e8f0; }}
          .card {{ background: #1e293b; padding: 1.2rem; border-radius: 10px; max-width: 860px; }}
          a {{ color: #93c5fd; }}
          code {{ background: #334155; padding: 2px 6px; border-radius: 6px; }}
        </style>
      </head>
      <body>
        <div class=\"card\">
          <h1>Resultado da busca</h1>
          <p>Você buscou por: {q}</p>
          <p><strong>Observação:</strong> Esta página é intencionalmente vulnerável a Reflected XSS.</p>
          <p><a href=\"/\">Voltar para o guestbook</a></p>
        </div>
      </body>
    </html>
    """


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
