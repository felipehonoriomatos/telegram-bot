import logging
from telegram import Update
from telegram.ext import ContextTypes

from app.models.database import SessionLocal
from app.services.ai_service import generate_ai_response
from app.services.menu_service import (
    MENU_TEXT, get_menu_keyboard,
    get_user_state, set_user_state,
    should_show_menu, get_prompt_for_option,
)

logger = logging.getLogger(__name__)

OPCAO_NOMES = {
    "suporte":   "🛠 Suporte técnico",
    "precos":    "💰 Informações e preços",
    "atendente": "👤 Falar com atendente",
    "outros":    "💬 Outros assuntos",
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /start — exibe menu de boas-vindas."""
    user_id = update.effective_user.id
    set_user_state(user_id, "menu")
    await update.message.reply_text(MENU_TEXT, reply_markup=get_menu_keyboard())


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Processa mensagens de texto."""
    user    = update.effective_user
    user_id = user.id
    username = user.username or user.first_name or str(user_id)
    text    = update.message.text

    logger.info(f"Mensagem de @{username} ({user_id}): {text[:80]}")

    # Mostra menu se for primeira mensagem ou palavra-chave
    if should_show_menu(text, user_id):
        set_user_state(user_id, "menu")
        await update.message.reply_text(MENU_TEXT, reply_markup=get_menu_keyboard())
        return

    # Responde com IA usando o prompt da opção escolhida
    state  = get_user_state(user_id)
    prompt = get_prompt_for_option(state) if state != "menu" else None

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    db = SessionLocal()
    try:
        ai_response = generate_ai_response(db, user_id, username, text, system_prompt=prompt)
    finally:
        db.close()

    # Adiciona botão para voltar ao menu
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    voltar = InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Menu principal", callback_data="menu")]])

    await update.message.reply_text(ai_response, reply_markup=voltar)


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Processa cliques nos botões inline do menu."""
    query   = update.callback_query
    user_id = query.from_user.id
    opcao   = query.data

    await query.answer()

    if opcao == "menu":
        set_user_state(user_id, "menu")
        await query.edit_message_text(MENU_TEXT, reply_markup=get_menu_keyboard())
        return

    # Usuário escolheu uma opção
    set_user_state(user_id, opcao)
    nome = OPCAO_NOMES.get(opcao, opcao)

    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    voltar = InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Menu principal", callback_data="menu")]])

    await query.edit_message_text(
        f"✅ *{nome}* selecionado!\n\nComo posso te ajudar? Digite sua mensagem:",
        parse_mode="Markdown",
        reply_markup=voltar,
    )
