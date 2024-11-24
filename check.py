import time
import requests
import socket
from config import BOT_TOKEN

# URL da API do Telegram
TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
GET_UPDATES_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"

def is_connected():
    """Verifica a conexão com a Internet."""
    try:
        requests.get("https://www.google.com", timeout=5)
        return True
    except requests.ConnectionError:
        return False

def get_local_ip():
    """Obtém o IP local da máquina."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))  # Usando o DNS público do Google
            return s.getsockname()[0]
    except Exception as e:
        print(f"Erro ao obter o IP local: {e}")
        return "IP local desconhecido"

def get_external_ip():
    """Obtém o IP externo da máquina."""
    try:
        response = requests.get("https://api.ipify.org?format=json", timeout=5)
        response.raise_for_status()
        return response.json().get("ip", "IP externo desconhecido")
    except Exception as e:
        print(f"Erro ao obter o IP externo: {e}")
        return "IP externo desconhecido"

def get_chat_id():
    """Obtém o ID da conversa privada mais recente com o bot."""
    try:
        response = requests.get(GET_UPDATES_URL, timeout=5)
        response.raise_for_status()
        updates = response.json()

        if updates.get("ok"):
            results = updates.get("result", [])
            for update in reversed(results):  # Percorre os updates do mais recente para o mais antigo
                if "message" in update and "chat" in update["message"]:
                    chat = update["message"]["chat"]
                    if chat["type"] == "private":  # Certifica-se de que é uma conversa privada
                        return chat["id"]
        print("Nenhuma conversa privada encontrada. Envie uma mensagem ao bot para iniciar.")
    except Exception as e:
        print(f"Erro ao obter o ID da conversa privada: {e}")
    return None

def send_message(chat_id, text):
    """Envia uma mensagem para o Telegram."""
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    try:
        response = requests.post(TELEGRAM_URL, json=payload)
        if response.status_code == 200:
            print("Mensagem enviada com sucesso!")
        else:
            print(f"Falha ao enviar mensagem: {response.text}")
    except Exception as e:
        print(f"Erro ao conectar ao Telegram: {e}")

if __name__ == "__main__":
    print("Aguardando conexão com a internet...")
    wait_time = 5  # Tempo inicial de espera em segundos

    while not is_connected():
        print(f"Sem conexão. Tentando novamente em {wait_time} segundos...")
        time.sleep(wait_time)
        wait_time = min(wait_time * 2, 60)  # Aumenta o intervalo até no máximo 60 segundos

    print("Conexão detectada! Obtendo IPs...")
    local_ip = get_local_ip()
    external_ip = get_external_ip()

    print("Obtendo o ID da conversa privada com o bot...")
    chat_id = get_chat_id()

    if chat_id:
        print("Enviando IPs para a conversa privada com o bot...")
        message = (
            f"Raspberry Pi conectado!\n\n"
            f"IP Local: {local_ip}\n"
            f"IP Externo: {external_ip}"
        )
        send_message(chat_id, message)
    else:
        print("Não foi possível obter o ID da conversa privada. Envie uma mensagem ao bot para iniciar a interação.")
