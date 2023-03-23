from flask_mail import Message

from app import mail

from app.models.tables import Config,  Devedores

def enviar_email_by_id(id):
    devedor = Devedores.query.filter_by(id=id).first()
    config = Config.query.first()


    corpo_email_header = '''
    <!DOCTYPE html>
    <head>
        <meta charset="UTF-8">
        <style>
            
            body {
                margin: auto;
            }
            
            body * {
                text-align: center;
                color: #000;
            }

            h1 {
                padding: 15px 8px;
                font-weight: 800;

                text-decoration: underline;
                text-decoration-color: #04D94F;
            }

            h2 {
                text-decoration: underline;
                text-decoration-color: #04D94F;
            }

            strong {
                color: #04D94F;
            }

            p.envio {
                font-size: 0.7em;
            }
        </style>
    </head>
    '''

    corpo_email_body = f'''<body>
            <h1>Pagamento <strong>Spotify</strong></h1>
            <p>Olá, {devedor.nome}</p>
            <p>Fiquei sabendo que você está devendo <strong>{devedor.meses_devendo} meses</strong> do Spotify para o kirito <br> Estou passando aqui somente para té lembrar de realizar o pagamento ;)</p>
            <p class="envio">Enviado por KiritoBOT</p>

            <h2>Pagamento</h2>

            <p>Valor Devendo: <strong> R$ {devedor.meses_devendo * config.valor}</strong></p>

            <p>Valor Parcela:  <strong>R$ {config.valor}</strong></p>


            <h2>Dados Pix</h2>
            <p>Nome: <strong>Luiz Gustavo Soares</strong></p>
            <p>Chave PIX: <strong>gustavo120wa@gmail.com</strong></p>
        </body>
        </html>
    '''

    msg = Message('Pagamento Spotify', recipients=[devedor.email])
    msg.html = corpo_email_header + corpo_email_body
    with open('app/static/imgs/barriga.jpg', 'rb') as img:
        msg.attach("image.png", "image/png", img.read())
    mail.send(msg)
    return True