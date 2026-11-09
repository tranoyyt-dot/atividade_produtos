from flask import Blueprint, request,  url_for, jsonify, render_template, redirect
from database import conectar_banco

produto = Blueprint("produto", __name__)

@produto.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():
    if request.method == "GET":
        return render_template("cadastrar.html")

    nome= request.form.get("nome")
    descricao= request.form.get("descricao")
    preco= request.form.get("preco")
    quantidade= request.form.get("quantidade")
    categoria= request.form.get("categoria")

    conexao = conectar_banco()
    cursor =conexao.cursor()
    
    cursor.execute ("INSERT INTO produtos(nome, descricao, preco, quantidade, categoria)" 
                    "VALUES (?, ?, ?, ?, ?)",
                    (nome, descricao, preco, quantidade, categoria)
    )
    conexao.commit()
    cursor.close()
    conexao.close()

    return redirect(url_for("produto.listar"))

@produto.route("/listar", methods=["GET"])
def listar():
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('SELECT * FROM produtos ORDER BY id')
    produtos = cursor.fetchall()
    cursor.close()
    conexao.close()
    return render_template("listar.html", produtos=produtos)

@produto.route("/apagar", methods=["DELETE"])
def apagar(id):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('DELETE FROM produtos WHERE  id = ?', (id))
    conexao.commit()
    apagados = cursor.rowcount
    cursor.close()
    conexao.close()

    if apagados == 0:
        return jsonify({"erro": "Produto não encontrado."}), 404

    return redirect(url_for("produto.listar"))
    