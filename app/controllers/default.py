from flask import render_template, url_for, jsonify, request, redirect
from flask_login import login_user, logout_user, current_user
from app import app, db, lm
from pixqrcode import PixQrCode
from werkzeug.security import generate_password_hash
from app.models.tables import Config, Login, Devedores

@lm.user_loader
def load_user(user_id):
    return Login.query.get(user_id)

@app.route('/')
def home():
    devedores = Devedores.query.all()
    return render_template('home.html', devedores=devedores)


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        
        usuario = request.form['usuario']
        senha = request.form['senha']

        if usuario and senha:

            user = Login.query.first()

            if user == None:
                user = Login(usuario='admin', senha='admin')

                db.session.add(user)
                db.session.commit()
            
            if user.usuario == usuario and user.verify_senha(senha):
                login_user(user)
                return redirect(url_for('home'))
            else: print('Dados incorretos')
        
    return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/dashboard')
def dashboard():
    if current_user.is_authenticated:
        config = Config.query.first()
        config.valor = f'{config.valor:.2f}'

        devedores = Devedores.query.all()

        for devedor in devedores:
            if (not devedor.meses_devendo):
                devedor.meses_devendo = 0

        return render_template('dashboard.html', config=config, devedores=devedores)
    else:
        return redirect(url_for('home'))


@app.route('/api/pagamento/<int:id>')
def api_get_pagamento(id):
    devedor = Devedores.query.filter_by(id=id).first()
    config = Config.query.first()

    if not config:
        config = Config(dia_cobranca=13, valor=5.82)
        db.session.add(config)
        db.session.commit()

    pixTotal = PixQrCode('Luiz Gustavo Soares', '38998381255', 'Diamantina', str(config.valor*devedor.meses_devendo))
    pix = PixQrCode('Luiz Gustavo Soares', '38998381255', 'Diamantina', str(config.valor))



    body = {
        'id':devedor.id,
        'meses_devendo': devedor.meses_devendo,
        'valor': config.valor,
        'nome': devedor.nome,
        'email': devedor.email,
        'pix': url_for('static', filename='imgs/qrcode-pix.png'),
        'pix_total': url_for('static', filename='imgs/qrcode-pix.png')
    }

    if pix.is_valid():
        body['pix'] = pix.export_base64()

    if pixTotal.is_valid():
        body['pix_total'] = pixTotal.export_base64()
    
    return jsonify(body)


@app.route('/api/config', methods=['GET', 'POST'])
def config():

    if not current_user.is_authenticated:
        return redirect(url_for('home'))
    

    config = Config.query.first()

    if not config:
        config = Config(dia_cobranca=13, valor=5.82)
        db.session.add(config)


    if request.method == 'POST':
        dia = request.form['dia']
        valor = request.form['valor']

        if dia.isnumeric and dia != '': 
            config.dia_cobranca = int(dia)
        

        if valor.isnumeric and valor != '': 
            config.valor = float(valor)

        db.session.commit()

        return redirect(url_for('dashboard'))

    body = {
        'valor':config.valor,
        'dia_cobranca': config.dia_cobranca
    }

    return jsonify(body)



@app.route('/api/login', methods=['GET', 'POST'])
def api_login():

    if not current_user.is_authenticated:
        return redirect(url_for('home'))
    

    if request.method == 'POST':
        user = Login.query.first()
         
        usuario = request.form['new_user']
        senha = request.form['new_senha']
        senha_anterior = request.form['senha_anterior']

        if usuario and senha:
            if user.verify_senha(senha_anterior):
                user.usuario = usuario
                user.senha = generate_password_hash(senha)

                db.session.commit()

    
    return redirect(url_for('dashboard'))
    


@app.route('/api/devedores/divida/<int:id>', methods=['GET', 'POST'])
def api_devedores(id):

    if not current_user.is_authenticated:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        meses_devendo = request.form['meses_devendo']
        if meses_devendo:
            devedor = Devedores.query.get(id)
            devedor.meses_devendo = meses_devendo
            db.session.commit()

    return redirect(url_for('dashboard'))
    

@app.route('/api/devedores/add', methods=['GET', 'POST'])
def api_devedores_add():

    if not current_user.is_authenticated:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['mail']
        foto_perfil = request.form['foto_perfil']

        if nome and email:
            dev = Devedores(nome=nome, email=email, foto_perfil=foto_perfil, meses_devendo=0)
            db.session.add(dev)
            db.session.commit()

    
    return redirect(url_for('dashboard'))
    
