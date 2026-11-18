import requests
from flask import Flask, render_template, request

app = Flask(__name__)
API = "http://127.0.0.1:8000/api"


@app.route("/")
def index():
    padaria = request.args.get("padaria", "")
    produto = request.args.get("produto", "")
    try:
        filtros = requests.get(f"{API}/filtros", timeout=5).json()
        dados = requests.get(
            f"{API}/vendas", params={"padaria": padaria, "produto": produto}, timeout=5
        ).json()
    except requests.RequestException:
        return "Back-end indisponível. Inicie a API FastAPI na porta 8000.", 503
    return render_template(
        "index.html", filtros=filtros, dados=dados, padaria=padaria, produto=produto
    )


if __name__ == "__main__":
    app.run(port=5000, debug=True)
