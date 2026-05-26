#  Telegram AI Bot

Bot de atendimento automático para Telegram com Inteligência Artificial, desenvolvido em Python.
Utiliza **python-telegram-bot** para conexão com Telegram e **Google Gemini** para respostas contextuais.

---

##  Funcionalidades

- ✅ Menu interativo com botões inline (sem digitar números)
- ✅ Respostas automáticas com IA (Google Gemini)
- ✅ Comportamento diferente da IA para cada opção do menu
- ✅ Histórico de conversa por usuário no banco de dados
- ✅ Botão "Menu principal" em toda resposta
- ✅ Indicador de digitação enquanto a IA processa
- ✅ Configuração 100% por variáveis de ambiente
- ✅ Sem necessidade de servidor — roda direto no PC ou VPS

---

##  Estrutura

```
telegram-bot/
├── app/
│   ├── config.py                # Configurações via .env
│   ├── models/
│   │   └── database.py          # Histórico SQLite
│   ├── services/
│   │   ├── ai_service.py        # Integração Google Gemini
│   │   └── menu_service.py      # Menu com botões inline
│   └── handlers/
│       └── message_handler.py   # Comandos e mensagens
├── run.py                       # Inicia o bot
├── requirements.txt
└── .env.example
```

---

##  Como rodar

### 1. Instale as dependências

```bash
pip install -r requirements.txt
```

### 2. Crie o bot no Telegram

1. Abra o Telegram e busque por **@BotFather**
2. Digite `/newbot`
3. Escolha um nome e username para o bot
4. Copie o **token** gerado (ex: `1234567890:ABCdef...`)

### 3. Configure o `.env`

```bash
cp .env.example .env
```

Edite o `.env`:
```env
TELEGRAM_TOKEN=1234567890:ABCdef...
GEMINI_API_KEY=AIzaSyXXXXXXXXXXXXX
BOT_SYSTEM_PROMPT=Você é atendente da Empresa X...
```

### 4. Inicie o bot

```bash
python run.py
```

Abra o Telegram, busque seu bot e mande `/start` para testar!

---

##  Fluxo do menu

```
Usuário: /start
Bot: Exibe menu com 4 botões

Usuário: clica em "Suporte técnico"
Bot: ✅ Suporte técnico selecionado! Como posso te ajudar?

Usuário: "Meu sistema não abre"
Bot: IA responde como especialista em suporte

Usuário: clica em "Menu principal"
Bot: Exibe menu novamente
```

---

##  Personalizando para seu cliente

Edite o `BOT_SYSTEM_PROMPT` no `.env`:

```env
# Exemplo: pet shop
BOT_SYSTEM_PROMPT=Você é atendente do Pet Shop Amigo Fiel. Informe sobre produtos, serviços de banho e tosa, vacinas e horários.

# Exemplo: imobiliária
BOT_SYSTEM_PROMPT=Você é corretor virtual da Imobiliária Lar Doce Lar. Apresente imóveis disponíveis e agende visitas.
```

---

##  Tecnologias

| Tecnologia | Uso |
|---|---|
| Python 3.11+ | Linguagem principal |
| python-telegram-bot | Conexão com Telegram |
| Google Gemini | IA para respostas |
| SQLAlchemy + SQLite | Histórico de conversa |

---

##  Licença
MIT — livre para uso comercial.
