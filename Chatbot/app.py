from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)
mensagens = []
modo_atendente = False

# Dicionário com pedidos fictícios
pedidos = {
    "1001": "Pedido 1001: Entregue ✅",
    "1002": "Pedido 1002: Em trânsito 🚚",
    "1003": "Pedido 1003: Aguardando pagamento 💳"
}

@app.route('/')
def cliente():
    return render_template('cliente.html')

@app.route('/atendente')
def atendente():
    return render_template('atendente.html')

@app.route('/mensagens')
def listar_mensagens():
    return jsonify(mensagens)

@app.route('/enviar_cliente', methods=['POST'])
def enviar_cliente():
    global modo_atendente
    data = request.get_json()
    mensagem = data['mensagem'].strip()
    mensagens.append({'autor': 'cliente', 'mensagem': mensagem})

    if not modo_atendente:
        resposta = gerar_resposta_chatbot(mensagem)
        mensagens.append({'autor': 'bot', 'mensagem': resposta})

        if "falar com atendente" in mensagem.lower() or mensagem.strip() == "3":
            mensagens.append({'autor': 'bot', 'mensagem': "Caso deseje ser atendido por whatsapp,clique no link: https://wa.me/5511999999999"})
            modo_atendente = True

    return '', 204

@app.route('/enviar_atendente', methods=['POST'])
def enviar_atendente():
    data = request.get_json()
    mensagem = data['mensagem'].strip()
    mensagens.append({'autor': 'atendente', 'mensagem': mensagem})
    return '', 204

def gerar_resposta_chatbot(msg):
    msg = msg.lower()
    hora = datetime.now().hour
    saudacao = "Bom dia" if hora < 12 else "Boa tarde" if hora < 18 else "Boa noite"

    # Verificar se é um número de pedido
    if msg in pedidos:
        return pedidos[msg]

    # Opções do menu
    if msg == "1" or "verificar pedido" in msg:
        return "Por favor, digite o número do seu pedido (ex: 1001, 1002 ou 1003)."
    elif msg == "2" or "ajuda" in msg:
        return "Acesse nossa central de ajuda pelo site ou descreva sua dúvida aqui."
    elif msg == "3" or "falar com atendente" in msg:
        return "Encaminhando para um atendente..."

    return f"""{saudacao}, em que posso ajudar?
1. Verificar pedido
2. Central de ajuda
3. Falar com atendente"""

if __name__ == '__main__':
    app.run(debug=True)
