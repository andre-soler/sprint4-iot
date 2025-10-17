from flask import Flask, request, jsonify
import logging
import time

app = Flask(__name__)
# Configuração básica de log
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Dados SIMULADOS do Módulo de Cadastro / Perfil Financeiro (IoB Data)
USUARIOS_CADASTRO = {
    42: {"nome": "Joao ReVeste", "score_risco": "ALTO", "progresso_gamificacao": 75},
    10: {"nome": "Maria Outra", "score_risco": "BAIXO", "progresso_gamificacao": 15},
}

def consultar_ia_preventiva(user_id):
    """
    Executa a lógica da IA Preventiva baseada no perfil do usuário.
    """
    perfil = USUARIOS_CADASTRO.get(user_id)
    if not perfil:
        return "Usuário não encontrado.", "INDEFINIDO"

    score = perfil["score_risco"]
    
    if score == "ALTO":
        mensagem = "ALERTA CRÍTICO: Seu Score de Risco está alto. Lembre-se do seu compromisso financeiro e evite sites de apostas."
    elif score == "MODERADO":
        mensagem = "Mantenha o foco. O ReVeste compara suas apostas com o potencial de investimento. Não desvie!"
    else: # BAIXO
        mensagem = "Parabéns! Seu Score está baixo. Continue focado nos investimentos."
    
    return mensagem, score

@app.route('/api/reviste/autenticacao/biometrica', methods=['POST'])
def handle_autenticacao_biometrica():
    """Recebe o sinal do módulo facial, registra e dispara a IA Preventiva."""
    data = request.get_json()
    user_id = data.get('user_id')
    timestamp = data.get('timestamp')
    tipo = data.get('tipo_autenticacao')

    if not user_id or user_id not in USUARIOS_CADASTRO:
        logging.warning(f"Tentativa de autenticação com ID desconhecido: {user_id}")
        return jsonify({"status": "falha", "mensagem": "Usuário não cadastrado ou ID inválido."}), 404

    user_info = USUARIOS_CADASTRO[user_id]
    
    # --- AÇÃO REGISTRADA (LOG de Acesso e IoB) ---
    logging.info(f"*** LOGIN REGISTRADO *** Usuário {user_info['nome']} (ID: {user_id}) autenticado via {tipo} em {timestamp}")

    mensagem_ia, score_risco = consultar_ia_preventiva(user_id)
    
    response = {
        "status": "sucesso",
        "user_id": user_id,
        "score_risco_atual": score_risco,
        "mensagem_intervencao": mensagem_ia, 
    }
    
    return jsonify(response), 200

if __name__ == '__main__':
    print("--- ReVeste Backend API Iniciada (Porta 5000) ---")
    print("Mantenha este terminal aberto.")
    app.run(port=5000)