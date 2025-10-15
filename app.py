from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import sqlite3
from datetime import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
import os

app = Flask(__name__)
app.secret_key = 'chave_secreta_para_o_projeto'

# Configuração do banco de dados
def init_db():
    conn = sqlite3.connect('bullying.db')
    cursor = conn.cursor()
    
    # Tabela para denúncias
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS denuncias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            email TEXT,
            tipo_bullying TEXT,
            local TEXT,
            descricao TEXT,
            data_denuncia TEXT,
            status TEXT DEFAULT 'Pendente'
        )
    ''')
    
    # Tabela para estatísticas (dados simulados)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS estatisticas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT,
            valor INTEGER,
            ano INTEGER
        )
    ''')
    
    # Inserir dados simulados se a tabela estiver vazia
    cursor.execute("SELECT COUNT(*) FROM estatisticas")
    if cursor.fetchone()[0] == 0:
        dados_simulados = [
            ('Cyberbullying', 45, 2023),
            ('Bullying Físico', 30, 2023),
            ('Bullying Verbal', 60, 2023),
            ('Bullying Social', 25, 2023),
            ('Cyberbullying', 50, 2024),
            ('Bullying Físico', 25, 2024),
            ('Bullying Verbal', 55, 2024),
            ('Bullying Social', 30, 2024)
        ]
        cursor.executemany("INSERT INTO estatisticas (tipo, valor, ano) VALUES (?, ?, ?)", dados_simulados)
    
    conn.commit()
    conn.close()

# Rota principal
@app.route('/')
def index():
    return render_template('index.html')

# Rota sobre o tema
@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

# Rota de denúncia
@app.route('/denuncia', methods=['GET', 'POST'])
def denuncia():
    if request.method == 'POST':
        is_anon = request.form.get('denuncia_anonima') == 'on'
        nome = request.form.get('nome') if not is_anon else None
        email = request.form.get('email') if not is_anon else None
        tipo_bullying = request.form['tipo_bullying']
        local = request.form.get('local', '') if 'local' in request.form else ''
        descricao = request.form['descricao']
        data_denuncia = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        conn = sqlite3.connect('bullying.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO denuncias (nome, email, tipo_bullying, local, descricao, data_denuncia)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (nome, email, tipo_bullying, local, descricao, data_denuncia))
        conn.commit()
        conn.close()
        
        flash('Denúncia registrada com sucesso! (Anônima)' if is_anon else 'Denúncia registrada com sucesso!', 'success')
        return redirect(url_for('denuncia'))
    
    return render_template('denuncia.html')

# Rota de estatísticas
@app.route('/estatisticas')
def estatisticas():
    # Gerar gráfico de barras
    conn = sqlite3.connect('bullying.db')
    cursor = conn.cursor()
    
    # Dados para 2023
    cursor.execute("SELECT tipo, valor FROM estatisticas WHERE ano = 2023")
    dados_2023 = cursor.fetchall()
    
    # Dados para 2024
    cursor.execute("SELECT tipo, valor FROM estatisticas WHERE ano = 2024")
    dados_2024 = cursor.fetchall()
    
    conn.close()
    
    # Preparar dados para o gráfico
    tipos = [dado[0] for dado in dados_2023]
    valores_2023 = [dado[1] for dado in dados_2023]
    valores_2024 = [dado[1] for dado in dados_2024]
    
    # Criar gráfico
    plt.figure(figsize=(10, 6))
    x = range(len(tipos))
    width = 0.35
    
    plt.bar([i - width/2 for i in x], valores_2023, width, label='2023', color='#ff6b6b')
    plt.bar([i + width/2 for i in x], valores_2024, width, label='2024', color='#4ecdc4')
    
    plt.xlabel('Tipos de Bullying')
    plt.ylabel('Percentual (%)')
    plt.title('Estatísticas de Bullying (Dados Simulados)')
    plt.xticks(x, tipos, rotation=45)
    plt.legend()
    plt.tight_layout()
    
    # Salvar gráfico em memória
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    
    return render_template('estatisticas.html', graph_url=graph_url)


# Rota de contato
@app.route('/contato')
def contato():
    return render_template('contato.html')

# ====== ÁREA ADMINISTRATIVA ======
@app.route('/admin-login', methods=['POST'])
def admin_login():
    # Aceita JSON ou form-url-encoded
    password = ''
    data = request.get_json(silent=True)
    if isinstance(data, dict) and 'password' in data:
        password = data.get('password') or ''
    else:
        password = request.form.get('password', '')
    password = password.strip()
    if password == 'DanielGuilherme':
        session['is_admin'] = True
        return jsonify({'ok': True}), 200
    return jsonify({'ok': False, 'error': 'Senha inválida'}), 401


@app.route('/admin')
def admin_dashboard():
    if not session.get('is_admin'):
        flash('Acesso restrito. Autentique-se como administrador.', 'error')
        return redirect(url_for('index'))

    conn = sqlite3.connect('bullying.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, nome, email, tipo_bullying, local, substr(descricao,1,120)||CASE WHEN length(descricao)>120 THEN '...' ELSE '' END, data_denuncia, status
        FROM denuncias
        ORDER BY id DESC
        LIMIT 20
    ''')
    denuncias = cursor.fetchall()

    # Agregações para gráficos
    cursor.execute('''
        SELECT COALESCE(tipo_bullying, 'Não informado') as tipo, COUNT(*)
        FROM denuncias
        GROUP BY tipo
        ORDER BY COUNT(*) DESC
    ''')
    denuncias_por_tipo = cursor.fetchall()

    cursor.execute('''
        SELECT strftime('%Y-%m-%d', data_denuncia) as dia, COUNT(*)
        FROM denuncias
        GROUP BY dia
        ORDER BY dia ASC
    ''')
    denuncias_por_dia = cursor.fetchall()
    conn.close()

    # Gráfico 1: Denúncias por tipo (barra)
    chart_tipo_b64 = None
    if denuncias_por_tipo:
        tipos = [row[0] for row in denuncias_por_tipo]
        counts = [row[1] for row in denuncias_por_tipo]
        plt.figure(figsize=(8, 4))
        bars = plt.bar(tipos, counts, color=['#e53935', '#ff7043', '#42a5f5', '#66bb6a', '#ab47bc', '#ffa726'])
        plt.title('Denúncias por Tipo')
        plt.ylabel('Quantidade')
        plt.xticks(rotation=25, ha='right')
        for bar, v in zip(bars, counts):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height(), str(v), ha='center', va='bottom', fontsize=9)
        plt.tight_layout()
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        chart_tipo_b64 = base64.b64encode(buf.getvalue()).decode()
        plt.close()

    # Gráfico 2: Denúncias por dia (linha)
    chart_dia_b64 = None
    if denuncias_por_dia:
        dias = [row[0] for row in denuncias_por_dia]
        counts_dia = [row[1] for row in denuncias_por_dia]
        plt.figure(figsize=(8, 3.5))
        plt.plot(dias, counts_dia, marker='o', color='#1e88e5')
        plt.title('Denúncias por Dia')
        plt.ylabel('Quantidade')
        plt.xticks(rotation=45, ha='right')
        plt.grid(alpha=0.2)
        plt.tight_layout()
        buf2 = io.BytesIO()
        plt.savefig(buf2, format='png')
        buf2.seek(0)
        chart_dia_b64 = base64.b64encode(buf2.getvalue()).decode()
        plt.close()

    return render_template(
        'admin.html',
        denuncias=denuncias,
        chart_tipo_b64=chart_tipo_b64,
        chart_dia_b64=chart_dia_b64,
        total_denuncias=sum([c for _, c in (denuncias_por_tipo or [])])
    )


@app.route('/admin-logout')
def admin_logout():
    session.pop('is_admin', None)
    flash('Sessão de administrador encerrada.', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    app.run(debug=debug_mode, host='0.0.0.0', port=port)