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

# Adicione aqui as outras rotas (editar, visualizar, etc.)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)