from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, DecimalField, SelectField
from wtforms.validators import DataRequired
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:senha@db/gestao_bens_escolares'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret-key'
db = SQLAlchemy(app)

# Forms
class BemForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    descricao = TextAreaField('Descrição')
    rfid_tag = StringField('RFID Tag', validators=[DataRequired()])
    categoria = StringField('Categoria')
    data_aquisicao = DateField('Data de Aquisição', format='%Y-%m-%d')
    valor = DecimalField('Valor')
    status = SelectField('Status', choices=[
        ('disponivel', 'Disponível'),
        ('em_uso', 'Em Uso'),
        ('manutencao', 'Manutenção'),
        ('descartado', 'Descartado')
    ])

class AmbienteForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    descricao = TextAreaField('Descrição')
    rfid_tag = StringField('RFID Tag', validators=[DataRequired()])
    localizacao = StringField('Localização')

class UsuarioForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    rfid_tag = StringField('RFID Tag')
    cargo = StringField('Cargo')
    senha = PasswordField('Senha', validators=[DataRequired()])
    confirmar_senha = PasswordField('Confirmar Senha', validators=[
        DataRequired(),
        EqualTo('senha', message='Senhas devem ser iguais')
    ])

class MovimentacaoForm(FlaskForm):
    bem_id = SelectField('Bem', coerce=int, validators=[DataRequired()])
    origem_id = SelectField('Origem', coerce=int)
    destino_id = SelectField('Destino', coerce=int, validators=[DataRequired()])
    observacao = TextAreaField('Observação')

# Rotas para Bens
@app.route('/bens')
def listar_bens():
    bens = Bem.query.all()
    return render_template('bens/listar.html', bens=bens)

@app.route('/bens/adicionar', methods=['GET', 'POST'])
def adicionar_bem():
    form = BemForm()
    if form.validate_on_submit():
        novo_bem = Bem(
            nome=form.nome.data,
            descricao=form.descricao.data,
            rfid_tag=form.rfid_tag.data,
            categoria=form.categoria.data,
            data_aquisicao=form.data_aquisicao.data,
            valor=form.valor.data,
            status=form.status.data
        )
        db.session.add(novo_bem)
        db.session.commit()
        flash('Bem adicionado com sucesso!', 'success')
        return redirect(url_for('listar_bens'))
    return render_template('bens/adicionar.html', form=form)

# Rotas para Ambientes
@app.route('/ambientes')
def listar_ambientes():
    ambientes = Ambiente.query.all()
    return render_template('ambientes/listar.html', ambientes=ambientes)

@app.route('/ambientes/adicionar', methods=['GET', 'POST'])
def adicionar_ambiente():
    form = AmbienteForm()
    if form.validate_on_submit():
        novo_ambiente = Ambiente(
            nome=form.nome.data,
            descricao=form.descricao.data,
            rfid_tag=form.rfid_tag.data,
            localizacao=form.localizacao.data
        )
        db.session.add(novo_ambiente)
        db.session.commit()
        flash('Ambiente adicionado com sucesso!', 'success')
        return redirect(url_for('listar_ambientes'))
    return render_template('ambientes/adicionar.html', form=form)

# Rotas para Usuários
@app.route('/usuarios')
def listar_usuarios():
    usuarios = Usuario.query.all()
    return render_template('usuarios/listar.html', usuarios=usuarios)

@app.route('/usuarios/adicionar', methods=['GET', 'POST'])
def adicionar_usuario():
    form = UsuarioForm()
    if form.validate_on_submit():
        novo_usuario = Usuario(
            nome=form.nome.data,
            email=form.email.data,
            rfid_tag=form.rfid_tag.data,
            cargo=form.cargo.data,
            senha=generate_password_hash(form.senha.data)
        )
        db.session.add(novo_usuario)
        db.session.commit()
        flash('Usuário adicionado com sucesso!', 'success')
        return redirect(url_for('listar_usuarios'))
    return render_template('usuarios/adicionar.html', form=form)

# Rotas para Relatórios
@app.route('/movimentacoes/relatorio')
def relatorio_movimentacoes():
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')
    
    query = Movimentacao.query.join(Bem).join(Ambiente, Movimentacao.destino_id == Ambiente.id)
    
    if data_inicio:
        query = query.filter(Movimentacao.data_movimentacao >= datetime.strptime(data_inicio, '%Y-%m-%d'))
    if data_fim:
        query = query.filter(Movimentacao.data_movimentacao <= datetime.strptime(data_fim, '%Y-%m-%d') + timedelta(days=1))
    
    movimentacoes = query.order_by(Movimentacao.data_movimentacao.desc()).all()
    
    if request.args.get('export') == 'csv':
        # Lógica para gerar CSV
        pass
    
    return render_template('movimentacoes/relatorio.html', movimentacoes=movimentacoes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
