from flask import Blueprint, request, jsonify
from core.database import (
    consultar_alimentos_disponiveis,
    inserir_alimento,
    alterar_status_alimento
)

bp = Blueprint('routes', __name__)

@bp.route("/alimentos", methods=["GET"])
def listar_alimentos():
    alimentos = consultar_alimentos_disponiveis()
    return jsonify(alimentos)

@bp.route("/alimentos", methods=["POST"])
def adicionar_alimento():
    dados = request.json
    campos_obrigatorios = ["nome", "descricao", "categoria", "data_validade", "quantidade"]

    if not all(campo in dados for campo in campos_obrigatorios):
        return jsonify({"erro": "Dados incompletos"}), 400

    try:
        inserir_alimento(
            nome=dados["nome"],
            descricao=dados["descricao"],
            categoria=dados["categoria"],
            data_validade=dados["data_validade"],
            quantidade=dados["quantidade"]
        )
        return jsonify({"mensagem": "Alimento adicionado com sucesso"}), 201
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@bp.route("/alimentos/<int:id>/status", methods=["PUT"])
def atualizar_status(id):
    dados = request.json
    novo_status = dados.get("status")

    if not novo_status:
        return jsonify({"erro": "O novo status é obrigatório"}), 400

    try:
        alterar_status_alimento(id_alimento=id, novo_status=novo_status)
        return jsonify({"mensagem": f"Status do alimento {id} atualizado para '{novo_status}'"}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
