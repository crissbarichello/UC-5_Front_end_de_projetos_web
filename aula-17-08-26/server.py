from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/upload", methods=["POST"])
def upload():
    if "imagem" not in request.files:
        return jsonify({"erro": "Nenhuma imagem enviada"}), 400

    arquivo = request.files["imagem"]

    if arquivo.filename == "":
        return jsonify({"erro": "Arquivo inválido"}), 400

    caminho = os.path.join(UPLOAD_FOLDER, arquivo.filename)
    arquivo.save(caminho)

    return jsonify({
        "mensagem": "Upload realizado com sucesso",
        "arquivo": arquivo.filename
    })

@app.route("/inscricao", methods=["POST"])
def incricao():
    retorno = request.get_json()
    if not retorno:
        return jsonify({"erro": "Nenhum dado enviado"}), 400    
    else:
        for campo in ["nome", "email", "data_nascimento", "assunto", "mensagem", "modalidade", "interesses"]:
            if campo not in retorno:
                return jsonify({"erro": f"Campo '{campo}' ausente"}), 400
            else:
                nomeArquivo = retorno.get("nomeArquivo", None) 
                arquivo = {
                    "nome": retorno["nome"],
                    "email": retorno["email"],
                    "data_nascimento": retorno["data_nascimento"],
                    "assunto": retorno["assunto"],
                    "mensagem": retorno["mensagem"],
                    "modalidade": retorno["modalidade"],
                    "interesses": retorno["interesses"],
                    "nomeArquivo": nomeArquivo
                } 
                os.write(os.open(nomeArquivo.json, os.O_WRONLY | os.O_CREAT | os.O_APPEND), json.dumps(arquivo).encode() + b"\n")  
    return jsonify({"mensagem": "Inscrição realizada com sucesso"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)