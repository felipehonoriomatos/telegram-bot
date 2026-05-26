from sqlalchemy import create_engine, Column, String, Text, DateTime, Integer, BigInteger
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

DATABASE_URL = "sqlite:///./telegram_bot.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Conversation(Base):
    """Armazena o histórico de mensagens por usuário do Telegram."""
    __tablename__ = "conversations"

    id         = Column(Integer, primary_key=True, index=True)
    user_id    = Column(BigInteger, index=True, nullable=False)  # ID do usuário no Telegram
    username   = Column(String(100), nullable=True)              # @username (opcional)
    role       = Column(String(10), nullable=False)              # "user" ou "assistant"
    content    = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
