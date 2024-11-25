import asyncio
import socket
import logging
from telegram.ext import ApplicationBuilder
from config import BOT_TOKEN

# Usuário autorizado
AUTHORIZED_USER_ID = 6504237047  # Substitua pelo ID correto

logging.basicConfig(filename="bot_ip_report.log", level=logging.INFO)

async def get_local_ip():
    """Obtém o IP local da máquina."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))  # Usando o DNS público do Google
            return s.getsockname()[0]
    except Exception as e:
        logging.error(f"Erro ao obter o IP local: {e}")
        return "IP local desconhecido"

async def get_external_ip():
    """Obtém o IP externo da máquina."""
    try:
        import aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.ipify.org?format=json", timeout=5) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("ip", "IP externo desconhecido")
                else:
                    return "Falha ao obter IP externo"
    except Exception as e:
        logging.error(f"Erro ao obter o IP externo: {e}")
        return "IP externo desconhecido"

async def send_ip_report(application):
    """Obtém os IPs e envia o relatório para o usuário autorizado."""
    local_ip = await get_local_ip()
    external_ip = await get_external_ip()

    message = (
        f"Raspberry Pi conectado!\n\n"
        f"IP Local: {local_ip}\n"
        f"IP Externo: {external_ip}"
    )

    try:
        # Envia a mensagem para o usuário autorizado
        await application.bot.send_message(chat_id=AUTHORIZED_USER_ID, text=message)
        logging.info("Mensagem enviada com sucesso!")
    except Exception as e:
        logging.error(f"Erro ao enviar mensagem: {e}")

async def main():
    """Configura e executa o bot."""
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Envia os IPs ao iniciar
    await send_ip_report(app)

    # Mantém o bot rodando (polling vazio para não interromper)
    await app.start()
    await app.updater.start_polling()
    await app.updater.stop()
    await app.stop()

if __name__ == "__main__":
    asyncio.run(main())
