#TODO
#Adicionar um comando de resetar para que apareça a mensagem inicial e zere a lista de atividades

# pip install python-telegram-bot
import re, random, json
from typing import Final
from telegram import Bot, Update
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, ConversationHandler, CallbackContext, Application, ContextTypes, filters, CallbackQueryHandler

LISTA_ATIVIDADES = []
OPCAO_MENU_REGEX = re.compile(r'^\/adicionar_atividade$|^\/remover_atividade$|^\/listar_atividade$|^\/reiniciar$|^\/help$', re.IGNORECASE)
START, SELECIONAR_ATIVIDADE, ADICIONAR_ATIVIDADE, REMOVER_ATIVIDADE, LISTAR_ATIVIDADE, HANDLE_MESSAGE, REINICIAR_MESSAGE \
    , HELP_MESSAGE = range(8)

def carregar_mensagens_do_arquivo(nome_arquivo):
    with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
        dados = json.load(arquivo)
    return dados['mensagens']

# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    start_text = """
                Olá! Obrigado por conversar comigo! \n\nO que você gostaria de fazer?
    1. /adicionar_atividade
    2. /remover_atividade
    3. /listar_atividade
    4. /reiniciar
    5. /help
    """

    # await context.bot.send_message(
    #     chat_id=update.effective_chat.id,
    #     text=start_text
    # )
    await update.message.reply_text(start_text,
        reply_markup=ReplyKeyboardMarkup([['/adicionar_atividade', '/remover_atividade', '/listar_atividade', '/reiniciar', '/help']], one_time_keyboard=True)
    )

    # await update.message.reply_text(start_text)

    message_type: str = update.message.chat.type
    text: str = update.message.text
    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')
    
    # caso o comando seja chamado novamente, zera a lista de atividades
    LISTA_ATIVIDADES.clear()
    
    return SELECIONAR_ATIVIDADE

async def menu_opcoes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text.lower() == '/adicionar_atividade':
        text_atv = """ 
            Digite as atividades que deseja inserir. Por favor, enviar neste formato:
        
        atividade_1
        atividade_2
        """
        await update.message.reply_text(text_atv)
        return ADICIONAR_ATIVIDADE
    elif update.message.text.lower() == '/remover_atividade':
        text_remove = """ 
            Digite o NÚMERO da atividade que você deseja remover!
        """
        await update.message.reply_text(text_remove)
        await listar_atividade(update, context)
        return REMOVER_ATIVIDADE
    elif update.message.text.lower() == '/help':
        text_help = """
            Os comandos dos bots são os seguintes:
        /start - Start de Bot
        /help - Provides helps for Bot
        /custom - Custom command
        /adicionar_atividade - add tasks
        /remover_atividade - remove tasks
        /listar_atividade - list taks
        /mensagem - get a motivacional message
        /reiniciar - restart the bot
        """
        await update.message.reply_text(text_help)
        return HELP_MESSAGE

# Responses
def handle_response(text: str) -> str:
    # por conta do Python ser case sensitive, colocar tudo em minúsculo
    processed: str = text.lower()
    
    if 'oi' in processed:
        return """Olá! Eu sou o Bot e estou aqui para te auxiliar nas suas atividades!\n\nClique no '/start' para começar!"""
    elif 'como vc está?' in processed:
        return 'Estou bem!'
    elif '/start' in processed:
        return processed
    # elif '/custom' in processed:
    #     return processed
    else:
        return "Não consigo entender o que você quer dizer! \n\nDigite '/help' para ver a lista de comandos!"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # nos informa se é um grupo ou chat privado
    message_type: str = update.message.chat.type
    text: str = update.message.text

    # informa o id do usuário que enviou a mensagem
    print(f'User ({update.message.chat.first_name}) in {message_type}: "{text}"')

    response: str = handle_response(text)
    
    print('Bot: ', response)
    await update.message.reply_text(response)
    if response == '/start':
        return SELECIONAR_ATIVIDADE

async def adicionar_atividade(update: Update, context: CallbackContext) -> int:
    # text_atv = """ 
    #     Digite as atividades que deseja inserir. Por favor, enviar neste formato:
    
    # atividade_1
    # atividade_2
    # """
    # await update.message.reply_text(text_atv
    #     # reply_markup=ReplyKeyboardMarkup([['Yes', 'No']], one_time_keyboard=True)
    # )
    # await context.bot.send_message(
    #     chat_id=update.effective_chat.id,
    #     text=text_atv
    # )
    message_type: str = update.message.chat.type
    text = update.message.text
    # text = context.args
    print(f'User ({update.message.chat.first_name}) in {message_type}: "{text}"')
    
    if not text:
        await update.message.reply_text("Por favor, forneça uma atividade para adicionar.")
        return START
    
    atividade = re.split(r'\n|,', text)

    for a in atividade:
        LISTA_ATIVIDADES.append(a.capitalize())
    
    await update.message.reply_text('Atividades adicionadas com sucesso!')

    await update.message.reply_text("""O que deseja fazer agora? 
    1. /adicionar_atividade 
    2. /remover_atividade 
    3. /listar_atividade
    4. /reiniciar
    5. /help""")

    return SELECIONAR_ATIVIDADE

async def remover_atividade(update: Update, context: CallbackContext) -> int:
    # atividade = update.message.text # -> ele pega o texto digitado pelo usuário Ex: /remover_atividade estudar
    # atividade = context.args[0] # -> nesse caso pega os argumentos passados, que seria o estudar
    message_type: str = update.message.chat.type
    text = update.message.text
    print(f'User ({update.message.chat.first_name}) in {message_type}: "{text}"')

    if not text:
        await update.message.reply_text("Por favor, forneça uma atividade para remover.")
        return SELECIONAR_ATIVIDADE
    
    # subtrai 1 pois a lista começa do 0
    posicao = int(text) - 1
    # pega o valor da posição na lista
    if posicao >= 0 and posicao < len(LISTA_ATIVIDADES):
        valor = LISTA_ATIVIDADES[posicao]
    
    # atividade = re.split(r'\n|,', text)
    if valor in LISTA_ATIVIDADES:
        await update.message.reply_text(f'Atividade "{valor}" removida com sucesso!')
        await enviar_mensagem_motivacional(update, context)
        LISTA_ATIVIDADES.remove(valor)
    else:
        await update.message.reply_text(f'Atividade "{valor}" não encontrada na lista.')

    return SELECIONAR_ATIVIDADE

async def listar_atividade(update: Update, context: CallbackContext) -> int:
    list_atv = []
    cont = 1

    for atv in LISTA_ATIVIDADES:
        pendentes = f'{cont}. {atv}'
        cont += 1
        list_atv.append(pendentes)

    enum = "\n".join(list_atv)
    if enum:
        await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Atividades Pendentes:\n\n' + enum
        )
    else:
        await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Atividades Pendentes:\n\n Não existe tarefas pendentes'
        )

async def enviar_mensagem_motivacional(update: Update, context: CallbackContext) -> int:
    # user = update.message.from_user
    # if not LISTA_ATIVIDADES:
    msg_file = carregar_mensagens_do_arquivo('mensagem.json')

    await update.message.reply_text(random.choice(msg_file))
    # else:
        # await update.message.reply_text('Ainda existem atividades a serem concluídas.')

    return SELECIONAR_ATIVIDADE

def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Operação cancelada. O que você gostaria de fazer agora?')
    return SELECIONAR_ATIVIDADE

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text = update.message.text
    # text = context.args
    print(f'User ({update.message.chat.first_name}) in {message_type}: "{text}"')
    
    if text == '/start':
        await start_command(update, context)
    else:
        return HANDLE_MESSAGE
    

async def reiniciar(update: Update, context: CallbackContext):
    await update.message.reply_text('Bot está sendo reiniciado e lista será apagada!')
    await start_command(update, context)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    start_text = """
        Digite algo!
    """
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=start_text
    )
    """context.args -> argumento passado com a chamada da função
        /caps a b
    """
    print(context.args)
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

def main(TOKEN):
    app = Application.builder().token(TOKEN).build()


    app.add_handler(CommandHandler('listar_atividade', listar_atividade ))
    app.add_handler(CommandHandler('mensagem', enviar_mensagem_motivacional))
    app.add_handler(CommandHandler('reiniciar', reiniciar))
    app.add_handler(CommandHandler('help', help))

    # handle the messages
    # app.add_handler(MessageHandler(filters.TEXT, handle_message))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start_command), MessageHandler(filters.TEXT, handle_message)],
        states={
            START: [
                MessageHandler(filters.Regex('.'), start_command)
            ],
            SELECIONAR_ATIVIDADE:[
                MessageHandler(filters.Regex(OPCAO_MENU_REGEX), menu_opcoes)
            ],
            ADICIONAR_ATIVIDADE: [
                MessageHandler(filters.Regex('.'), adicionar_atividade)
            ],
            REMOVER_ATIVIDADE: [
                MessageHandler(filters.Regex('.'), remover_atividade)
            ],
            HANDLE_MESSAGE: [
                MessageHandler(filters.TEXT, handle_message)
            ],
            # HELP_MESSAGE: [
            #     MessageHandler(filters.Regex('.'), help)
            # ]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    app.add_handler(conv_handler)

    print('Polling...')
    app.run_polling(poll_interval=3)


if __name__ == '__main__':
    """
    Os comandos devem ser setados pelo Telegram via configuração do Bot no BotFather.
    Usando o comando /setcommands
        start - Start de Bot
        help - Provides helps for Bot
        custom - Custom command
    """
    print('Começando o Bot...')

    # # Commands
    # app.add_handler(CommandHandler('start', start_command))
    # app.add_handler(CommandHandler('help', help_command))
    # app.add_handler(CommandHandler('custom', custom_command))
    
    # # Messages
    # app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # # Errors
    # app.add_error_handler(error)

    token_file = 'bot_token.json'
    with open(token_file, 'r', encoding='utf-8') as arquivo:
        dados = json.load(arquivo)
    
    TOKEN = dados['TOKEN']
    main(TOKEN)
