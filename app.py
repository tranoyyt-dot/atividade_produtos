from flask import Flask, redirect, url_for
from database import inicializar_banco, CAMINHO_BANCO
from controllers.produto_controller import produto_bp
 
app = Flask(__name__)
 
app.register_blueprint(produto_bp)
 
inicializar_banco(CAMINHO_BANCO)
 
 
@app.route("/", methods=["GET"])
def inicio():
    return redirect(url_for("produto_bp.listar"))
 
 
if __name__ == '__main__':
    app.run(debug=True)
 