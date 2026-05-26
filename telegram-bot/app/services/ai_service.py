import httpx
from sqlalchemy.orm import Session
from app.models.database import Conversation
from app.config import get_settings

settings = get_settings()

MAX_HISTORY_MESSAGES = 10

GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-2.0-flash:generateContent"
)


def get_history(db: Session, user_id: int) -> list[dict]:
    """Busca histórico do usuário no formato do Gemini."""
    rows = (
        db.query(Conversation)
        .filter(Conversation.user_id == user_id)
        .order_by(Conversation.created_at.desc())
        .limit(MAX_HISTORY_MESSAGES)
        .all()
    )
    rows = list(reversed(rows))

    history = []
    for row in rows:
        role = "model" if row.role == "assistant" else "user"
        history.append({"role": role, "parts": [{"text": row.content}]})

    return history


def save_message(db: Session, user_id: int, username: str, role: str, content: str):
    """Salva mensagem no banco de dados."""
    msg = Conversation(user_id=user_id, username=username, role=role, content=content)
    db.add(msg)
    db.commit()


def generate_ai_response(
    db: Session,
    user_id: int,
    username: str,
    user_message: str,
    system_prompt: str = None,
) -> str:
    """Gera resposta da IA com histórico e prompt específico."""
    prompt = system_prompt or settings.bot_system_prompt

    save_message(db, user_id, username, "user", user_message)
    history = get_history(db, user_id)

    payload = {
        "system_instruction": {"parts": [{"text": prompt}]},
        "contents": history,
    }

    response = httpx.post(
        GEMINI_URL,
        params={"key": settings.gemini_api_key},
        json=payload,
        timeout=30,
    )
    response.raise_for_status()

    ai_text = response.json()["candidates"][0]["content"]["parts"][0]["text"]
    save_message(db, user_id, username, "assistant", ai_text)

    return ai_text
