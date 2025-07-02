from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# cria o banco de dados e a tabela se não existir
def init_db():
    conn = sqlite3.connect('agenda.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contatos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            telefone TEXT NOT NULL,
            email TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
init_db()

#página inicial - mostra a lista de contatos
@app.route('/')
def index():
    conn = sqlite3.connect('agenda.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM contatos')
    contatos = cursor.fetchall()
    conn.close()
    return render_template('index.html', contatos=contatos)

# Rota para adicionar novo contato
@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar():
    if request.method == 'POST':
        nome = request.form['nome']
        telefone = request.form['telefone']
        email = request.form['email']

        conn = sqlite3.connect('agenda.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO contatos (nome, telefone, email) VALUES (?, ?, ?)', (nome, telefone, email))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))
        
    return render_template('form.html')
    
# Rota para excluir contato
@app.route('/excluir/<int:id>')
def excluir(id):
    conn = sqlite3.connect('agenda.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM contatos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect (url_for('index'))

# inicializa o banco de dados e executa o app

if __name__ == '__main__':
    
    app.run(debug=True)