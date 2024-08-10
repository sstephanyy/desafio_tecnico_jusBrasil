from flask import Blueprint, jsonify, request
from Crawlers.tjal_tjce_scraper import get_process_data
from Crawlers.tjal_tjce_level2_scraper import get_process_data_grau2


scraper_bp = Blueprint('process', __name__, url_prefix='/api')

@scraper_bp.route("/processo", methods=["GET"])
def get_processo():
    data = request.json
    if 'process_number' not in data or 'tribunal_name' not in data:
        return jsonify({"error": "Parâmetros 'process_number' e 'tribunal_name' são obrigatórios!"}), 400

    process_number = data['process_number']
    tribunal_name = data['tribunal_name']

    if tribunal_name == "TJAL":
        data_grau1 = get_process_data(process_number, tribunal_name)
        data_grau2 = get_process_data_grau2(process_number, tribunal_name)

        return jsonify({"grau_1": data_grau1, "grau_2": data_grau2})
    
    elif tribunal_name == "TJCE":
        data_grau1 = get_process_data(process_number, tribunal_name)
        data_grau2 = get_process_data_grau2(process_number, tribunal_name)

        return jsonify({"grau_1": data_grau1, "grau_2": data_grau2})
    
    else:
        return jsonify({"error": "Nome do Tribunal não foi encontrado ou não existe!"}), 400
