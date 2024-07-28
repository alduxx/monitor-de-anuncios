import os
import requests

from dotenv import load_dotenv

# https://www.iemoji.com/#?category=symbols&version=36&theme=appl&skintone=default

def envia_notificacao(anuncio):
    load_dotenv()
    token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')

    preco = float(anuncio['preco'])

    TEXTO = f"""📣  Novo Anúncio Encontrado!
📍<b>{anuncio['endereco']},</b>
{anuncio['caracteristicas']},
💵<b>R$ {preco:.2f}</b>
({anuncio['custos_adicionais']})

{anuncio['url']}
    """

    message_data = {
        'chat_id': chat_id,
        'text': TEXTO,
        'parse_mode': 'HTML'
    }

    URL = f'https://api.telegram.org/bot{token}/sendMessage'

    response = requests.post(URL, data=message_data)

    if response.status_code == 200:
        print('NOTIFICA: Mensagem enviada com sucesso!')
        # TODO: update bd
        return 1
    else:
        print('NOTIFICA: Falha ao enviar a mensagem Telegram.')
        return 0
