from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db
import sys
import time

bp = Blueprint('crud', __name__)

ts = time.gmtime()

#@bp.route('/crud')
#def crud():
@bp.route('/view')
def view():
    db = get_db()
    alunos = db.execute(
        ' SELECT id_aluno, Nome_Completo, RA, Data_Nascimento, RM, Data_Alteracao from Alunos;'

    ).fetchall()
    
    return render_template('crud/view.html', alunos=alunos)

@bp.route('/<string:Nome_Completo>/search')
#@bp.route('/search')
def search():
    Nome_Completo = None
    if request.method == 'POST':
        
        Nome_Completo = request.form['Nome_Completo']
        error = None

        if not Nome_Completo:
            error = 'Caracteres Utilizados Invalidos'

        if error is not None:
            flash(error)

        else:
            db = get_db()
            alunos = db.execute(
                ' SELECT id_aluno, Nome_Completo, from Alunos;'
                ' WHERE Nome_Completo = ?',
                (Nome_Completo,)

            ).fetchall()
            
            return redirect(url_for('crud.view'))
    
    return render_template('crud/view.html', alunos=alunos)

@bp.route('/')
def index():
    #db = get_db()
    #alunos = db.execute(
        #' SELECT id_aluno from Alunos '

        
    #).fetchall()
    #return render_template('crud/index.html', alunos=alunos)
    return render_template('crud/index.html')

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        
        Nome_Completo = request.form['Nome_Completo']
        RA = request.form['RA']
        #Criado_Por = session.get('user_id')
        Data_Nascimento = request.form['Data_Nascimento']
        RM = request.form['RM']
        
        error = None
        print(time.strftime("%Y-%m-%d %H:%M:%S", ts))
        if not Nome_Completo:
            error = 'Nome completo e um campo obrigatorio'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO Alunos (Nome_Completo, RA, Data_Nascimento, RM, Data_Alteracao)'
                'VALUES (?, ?, ?, ?, ?)',
                (Nome_Completo, RA, Data_Nascimento, RM, time.strftime("%Y-%m-%d %H:%M:%S", ts))

                
            )
            db.commit()
            #return redirect(url_for('crud.index'))
            return redirect(url_for('index'))

    return render_template('crud/create.html')

#def get_post(id, check_author=True):
def get_aluno(id_aluno):
    Aluno = get_db().execute(
        'SELECT Id_Aluno, Nome_Completo, RA, Criado_Por, Data_Nascimento, RM, Data_Alteracao'
        ' FROM Alunos '
        #' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE Id_Aluno = ?',
        (id_aluno,)
    ).fetchone()

    if Aluno is None:
        abort(404, f"Aluno {Id_Aluno} nao existe.")

    
    #if check_author and post['author_id'] != g.user['id']:
    #    abort(403)

    return Aluno

@bp.route('/<int:Id_Aluno>/update', methods=('GET', 'POST'))
@login_required
def update(Id_Aluno):
    Aluno = get_aluno(Id_Aluno)

    if request.method == 'POST':
        Nome_Completo = request.form['Nome_Completo']
        RA = request.form['RA']
        #Criado_Por = session.get('user_id')
        Data_Nascimento = request.form['Data_Nascimento']
        RM = request.form['RM']
    
        error = None

        if not Nome_Completo:
            error = 'Nome completo e um campo obrigatorio'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE Alunos SET Nome_Completo = ?, RA = ?, Data_Nascimento = ?, RM = ?'
                ' WHERE Id_Aluno = ?',
                (Nome_Completo, RA, Data_Nascimento, RM, Id_Aluno)
            )
            db.commit()
            #return redirect(url_for('crud'))
            return redirect(url_for('index'))

    return render_template('crud/update.html', Aluno=Aluno)

@bp.route('/<int:Id_Aluno>/delete', methods=('POST',))
@login_required
def delete(Id_Aluno):
    get_aluno(Id_Aluno)
    db = get_db()
    db.execute('DELETE FROM Alunos WHERE Id_Aluno = ?', (Id_Aluno,))
    db.commit()
    #return redirect(url_for('crud'))
    return redirect(url_for('index'))