import time
import requests
import socket

# Configurações do Telegram
BOT_TOKEN = "7094865944:AAGCyOjgikJqKpCQXXuycmtD77yIE0Q2eLc"  # Token do bot
CHAT_ID = "-4573411635"  # Chat ID do destinatário

# URL da API do Telegram
TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

def is_connected():
    """
    Verifica se há conexão com a internet tentando acessar um site conhecido.
    """
    try:
        requests.get("https://www.google.com", timeout=5)
        return True
    except requests.ConnectionError:
        return False

def get_local_ip():
    """
    Obtém o endereço IP local real do dispositivo (não o loopback).
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))  # Usando o DNS público do Google
            local_ip = s.getsockname()[0]  # Obtém o IP local usado na conexão
        return local_ip
    except Exception as e:
        print(f"Erro ao obter o IP local: {e}")
        return "IP local desconhecido"

def get_external_ip():
    """
    Obtém o endereço IP externo (IP público) do dispositivo.
    """
    try:
        response = requests.get("https://api.ipify.org?format=json", timeout=5)
        response.raise_for_status()
        external_ip = response.json().get("ip", "IP externo desconhecido")
        return external_ip
    except Exception as e:
        print(f"Erro ao obter o IP externo: {e}")
        return "IP externo desconhecido"

def send_message(chat_id, text):
    """
    Envia uma mensagem para o chat do Telegram.
    """
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
    #external_ip = get_external_ip()

    print("Enviando IPs para o Telegram...")
    message = (
        f"O dispositivo conectou à internet!\n"
        f"IP Local: {local_ip}\n"
        #f"IP Externo: {external_ip}"
    )
    send_message(CHAT_ID, message)
