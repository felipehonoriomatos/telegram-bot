
import logging
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    CallbackQueryHandler, filters,
)

from app.config import get_settings
from app.models.database import init_db
from app.handlers.message_handler import start, handle_message, handle_callback

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def main():
    settings = get_settings()

    logger.info(" Iniciando Telegram AI Bot...")
    init_db()
    logger.info("✅ Banco de dados inicializado")

    app = Application.builder().token(settings.telegram_token).build()

    # Registra handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu",  start))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("✅ Bot iniciado — aguardando mensagens...")
    logger.info("   Pressione Ctrl+C para parar")

    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
