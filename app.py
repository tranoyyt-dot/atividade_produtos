from flask import Flask, redirect, url_for
from database import inicializar_banco
from controllers.produto_controller import produto

app = Flask(__name__)

app.register_blueprint(produto)

@app.route("/", methods=["GET"])
def inicio():
    return redirect(url_for("produto.listar"))

if __name__ == '__main__':
    inicializar_banco("meu_banco.db")
    app.run(debug=True)