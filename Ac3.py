#Membros do grupo
#Leonardo Alves Vieira RA: 2201156
#Randal Pereira de Souza RA: 2200811
# Yago de Sousa Cardoso RA: 2201001

import mysql.connector
from mysql.connector import Error
from flask import Flask, jsonify, request
app = Flask(__name__)


@app.route('/')
def conectar():
    try:
        global con
        con = mysql.connector.connect(
            host='localhost', database='db_clientes', user='root',
            password='123456')
        if con.is_connected():
            db_info = con.get_server_info()
            print("Conectado ao servidor MySQL versão ", db_info)
            cursor = con.cursor()
            cursor.execute("select database();")
            linha = cursor.fetchone()
            print("Conectado ao banco de dados ", linha)
            print("Atividade continua 3 API"), 200
    except Error as e:
        print("Erro ao acessar a tabela", e)


@app.route('/consultar', methods=["GET"])
def consultar():
    try:
        conectar()
        consulta_sql = "SELECT * FROM tb_cliente"
        cursor = con.cursor()
        cursor.execute(consulta_sql)
        colunas = cursor.fetchall()
        print("\nMostrando os Clientes cadastrados")
        for coluna in colunas:
            print("Nome:", coluna[0])
            print("Sobrenome:", coluna[1])
            print("cpf:", coluna[2])
            print("Número total de registros retornados: ", cursor.rowcount)

    except Error as e:
        print("Erro ao acessar tabela", e)

    finally:
        if (con.is_connected()):
            con.close()
            cursor.close()
            print("Conexão ao MySQL encerrada")
            return jsonify(colunas)


@app.route('/cadastrar', methods=["POST"])
def cadastrar():
    try:
        conectar()
        cursor = con.cursor()
        nome = request.form['nome']
        sobrenome = request.form['sobrenome']
        cpf = request.form['cpf']
        sql = f"INSERT INTO tb_cliente (nome, sobrenome, cpf) VALUES ('{nome}', '{sobrenome}', '{cpf}')"
        cursor.execute(sql)
        con.commit()
        print("Cadastrado com Sucesso")

    except Error as e:
        print("Erro ao acessar tabela MySQL", e)

    finally:
        if (con.is_connected()):
            con.close()
            cursor.close()
            print("Conexão ao MySQL encerrada")
            return consultar()


@app.route('/deletar', methods=["DELETE"])
def deletar():
    try:
        conectar()
        cursor = con.cursor()
        consulta = "SET SQL_SAFE_UPDATES=0"
        parametro = request.form['parametro']
        valor = request.form['valor']
        consulta_sql = f"DELETE FROM tb_cliente WHERE {parametro} = '{valor}'"
        cursor.execute(consulta)
        cursor.execute(consulta_sql)
        con.commit()
        print("Registro apagado com sucesso")

    except Error as e:
        print("Erro ao acessar tabela MySQL", e)

    finally:
        if (con.is_connected()):
            con.close()
            cursor.close()
            print("Conexão ao MySQL encerrada")
            return consultar()


if __name__ == '__main__':
    app.run(debug=True)
