from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# Estado dos usuários em memória
user_states: dict[int, str] = {}

# ---------------------------------------------------------------
#  Texto do menu — edite para personalizar por cliente
# ---------------------------------------------------------------
MENU_TEXT = (
    "Olá! Seja bem-vindo! 👋\n\n"
    "Como posso te ajudar hoje?\n"
    "Escolha uma opção abaixo:"
)

# Prompts específicos por opção
OPTION_PROMPTS = {
    "suporte": (
        "Você é um especialista em suporte técnico. "
        "Ajude o usuário a resolver problemas técnicos de forma clara e objetiva. "
        "Responda sempre em português."
    ),
    "precos": (
        "Você é um consultor de vendas simpático e persuasivo. "
        "Apresente informações sobre produtos e preços de forma clara. "
        "Responda sempre em português."
    ),
    "atendente": (
        "Você é uma recepcionista virtual. Informe que um atendente humano "
        "entrará em contato em breve. Colete o nome e melhor horário para contato. "
        "Responda sempre em português."
    ),
    "outros": (
        "Você é um assistente virtual prestativo e educado. "
        "Responda sempre em português, de forma clara e objetiva."
    ),
}

PALAVRAS_MENU = {"menu", "início", "inicio", "voltar", "/start", "oi", "olá", "ola"}


def get_menu_keyboard() -> InlineKeyboardMarkup:
    """Retorna teclado inline com as opções do menu."""
    teclado = [
        [InlineKeyboardButton("🛠 Suporte técnico",      callback_data="suporte")],
        [InlineKeyboardButton("💰 Informações e preços", callback_data="precos")],
        [InlineKeyboardButton("👤 Falar com atendente",  callback_data="atendente")],
        [InlineKeyboardButton("💬 Outros assuntos",      callback_data="outros")],
    ]
    return InlineKeyboardMarkup(teclado)


def get_user_state(user_id: int) -> str:
    return user_states.get(user_id, "menu")


def set_user_state(user_id: int, state: str):
    user_states[user_id] = state


def should_show_menu(text: str, user_id: int) -> bool:
    state = get_user_state(user_id)
    return state == "menu" or text.strip().lower() in PALAVRAS_MENU


def get_prompt_for_option(option: str) -> str:
    return OPTION_PROMPTS.get(option, OPTION_PROMPTS["outros"])
