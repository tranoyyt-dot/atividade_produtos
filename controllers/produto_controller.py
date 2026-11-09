from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from database import conectar_banco, CAMINHO_BANCO

produto_bp = Blueprint("produto_bp", __name__)


@produto_bp.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():
    if request.method == "GET":
        return render_template("cadastrar.html")
    nome = request.form.get("nome", "").strip()
    descricao = request.form.get("descricao", "").strip()
    categoria = request.form.get("categoria", "").strip()

    try:
        preco = float(request.form.get("preco", "").replace(",", "."))
        quantidade = int(request.form.get("quantidade", ""))
    except ValueError:
        return render_template(
            "cadastrar.html",
            erro="Preço e quantidade precisam ser números válidos."
        ), 400

    if not nome or preco < 0 or quantidade < 0:
        return render_template(
            "cadastrar.html",
            erro="Informe um nome e valores não negativos para preço e quantidade."
        ), 400

    conexao = conectar_banco(CAMINHO_BANCO)
    cursor = conexao.cursor()
    cursor.execute(
        "INSERT INTO produtos (nome, descricao, preco, quantidade, categoria) "
        "VALUES (?, ?, ?, ?, ?)",
        (nome, descricao, preco, quantidade, categoria)
    )
    conexao.commit()
    conexao.close()

    return redirect(url_for("produto_bp.listar"))


@produto_bp.route("/listar", methods=["GET"])
def listar():
    conexao = conectar_banco(CAMINHO_BANCO)
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM produtos ORDER BY id")
    produtos = cursor.fetchall()
    conexao.close()

    return render_template("listar.html", produtos=produtos)


@produto_bp.route("/apagar/<int:id>", methods=["DELETE"])
def apagar(id):
    conexao = conectar_banco(CAMINHO_BANCO)
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM produtos WHERE id = ?", (id,))
    conexao.commit()
    apagados = cursor.rowcount
    conexao.close()

    if apagados == 0:
        return jsonify({"erro": "Produto não encontrado."}), 404

    return jsonify({"mensagem": "Produto excluído com sucesso."}), 200