'''
CREATE SCHEMA IF NOT EXISTS vet;

USE vet;

CREATE TABLE IF NOT EXISTS tbl_tutor 
(  
    Nome           CHAR(50)     NOT NULL,
    Sobrenome      VARCHAR(50)  NOT NULL,
    Email          VARCHAR(50)  NOT NULL,
    Endereco 	   VARCHAR(50)  NOT NULL,
    Telefone       INT          NOT NULL, 
    CPF            INT          NOT NULL,
    Idade          FLOAT(2,2),
    Pet            VARCHAR(20),
CONSTRAINT uqcpf UNIQUE (CPF)
,CONSTRAINT tutor_cpf_pk PRIMARY KEY(CPF)
,CONSTRAINT pet_name_fk FOREIGN KEY(Pet) REFERENCES tbl_pets(Nome)
,CONSTRAINT ckidade CHECK (Idade >= 18)
,CONSTRAINT ckTelefone CHECK (
Telefone LIKE '[0-9][0-9][0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]' OR
Telefone LIKE '([0-9][0-9]) [0-9][0-9][0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]'
)
);

CREATE TABLE IF NOT EXISTS tbl_pets
(
PetID BIGINT NOT NULL AUTO_INCREMENT
, Nome VARCHAR(20) NOT NULL
, Especie CHAR(30) NOT NULL
, Raca VARCHAR(20)
, Cor CHAR(20)
, Idade FLOAT(2,2)
, CPFTutor INT NOT NULL
,CONSTRAINT pet_nome_pk PRIMARY KEY(Nome)
,CONSTRAINT tutor_cpf_fk FOREIGN KEY(CPFTutor) REFERENCES tbl_tutor(CPF)
);

SELECT * FROM tbl_pets

COMO FUNCIONOU:

CREATE SCHEMA IF NOT EXISTS vet;

USE vet;

CREATE TABLE IF NOT EXISTS tbl_tutor 
(  
    Nome           CHAR(50)     NOT NULL,
    Sobrenome      VARCHAR(50)  NOT NULL,
    Email          VARCHAR(50)  NOT NULL,
    Endereco 	   VARCHAR(50)  NOT NULL,
    Telefone       BIGINT       NOT NULL, 
    CPF            BIGINT       NOT NULL,
    Idade          FLOAT(5,2),
CONSTRAINT uqcpf UNIQUE (CPF)
,CONSTRAINT tutor_cpf_pk PRIMARY KEY(CPF)
,CONSTRAINT ckidade CHECK (Idade >= 18)
);

CREATE TABLE IF NOT EXISTS tbl_pets
(
PetID BIGINT NOT NULL AUTO_INCREMENT
, Nome VARCHAR(20) NOT NULL
, Especie CHAR(30) NOT NULL
, Raca VARCHAR(20)
, Cor CHAR(20)
, Idade FLOAT(5,2)
, CPF  INT  NOT NULL
,CONSTRAINT pet_nome_pk PRIMARY KEY(Nome)
,CONSTRAINT tutor_cpf_fk FOREIGN KEY(CPF) REFERENCES tbl_tutor(CPF)
);

SELECT * FROM tbl_pets

'''

import os
from flask import Flask, render_template, json, request
from flask_mysqldb import MySQL


mysql = MySQL()
app = Flask(__name__) 

#MySQL configurations 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Impacta2024'
app.config['MYSQL_DB'] = 'vet'
app.config['MYSQL_HOST'] = 'localhost'
#app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'
mysql.init_app(app)

@app.route('/')
def main():
    return render_template('form.html')

@app.route('/cadastro',methods=['POST','GET'])
def cadastro():
    try:
        _namet = request.form['inputNameT']
        _lastnamet = request.form['inputLastName']
        _email = request.form['inputEmail']
        _addresst = request.form['inputAddress']
        _phoneT = request.form['inputPhone']
        _cpf = request.form['inputCpf']
        _ageT = request.form['inputAgeT']

        print(_namet)
        print(_lastnamet)
        print(_email)
        print(_addresst)
        print(_phoneT)
        print(_cpf)
        print(_ageT)

        
        conn = mysql.connection
        cursor = conn.cursor()
        cursor.execute('SELECT CPF FROM tbl_tutor WHERE CPF = %s',(_cpf,))
        resultado = conn.fetchone()
        print(resultado)
            
        if resultado:
            msg = (f'CPF {_cpf} ja cadastrado no banco de dados')
            return render_template('form.html', mensagem = msg)
        else:
                
            conn = mysql.connection
            cursor = conn.cursor()
            cursor.execute('INSERT INTO tbl_tutor (Nome, Sobrenome, Email, Endereco, Telefone, CPF, Idade) VALUES (%s, %s, %s, %s, %s, %s, %s)', (_namet,_lastnamet,_email,_addresst,_phoneT,_cpf,_ageT ))
            #Alt  + Z para quebra linhas grandes
            conn.commit()
            msg = 'Tutor cadastrado com sucesso'
            return render_template('form.html', mensagem = msg)
        
    except Exception as e:
        return json.dumps({'error': str(e)})
    
@app.route('/cadastro/pets',methods=['POST','GET'])
def cadastroPets():
    try:
        _name = request.form['inputName']
        _specie = request.form['inputSpecie']
        _race = request.form['inputRace']
        _color = request.form['inputColor']
        _age = request.form['inputAge']


        print(_name)
        print(_specie)
        print(_race)
        print(_color)
        print(_age)

        if _name and _specie and _race:
        
            if int(_age) < 0 :
                raise ValueError
            
            cur = mysql.connection.cursor()
            cur.execute('SELECT Nome FROM tbl_pets WHERE Nome = %s',(_name))
            resultado = cur.fetchone()
            print(resultado)

            if resultado:
                msg = 'Esse nome ja esta cadastrado'
                return render_template('form.html', mensagem = msg)
            
            else:
                conn = mysql.connection
                cursor = conn.cursor()
                cursor.execute('INSERT INTO tbl_pets (Nome, Especie, Raca, Cor, Idade) Values (%s, %s, %s, %s, %s)', (_name, _specie, _race, _color, _age ))
                conn.commit()
                msg = ("Pet cadastrado com sucesso")


            return render_template('form.html', mensagem = msg)
        
        else:

            return json.dumps({'html':'<span>Preecha os campos obrigatorios'})
        
    except ValueError:
        return json.dumps({'error': "O campo idade deve ser preenchido. Exemplo: 1.2 (Anos.Meses) "})

    except Exception as e:
        return json.dumps({'error': str(e)})
    
@app.route('/lista/tutores',methods=['GET']) 
def listar():
    try:
        conn = mysql.connection
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tbl_pets')
        lista = cursor.fetchall()
        print(lista[0])

        return render_template('listar.html', Lista = lista)

    except Exception as e:
        return json.dumps({'error': str(e)})

@app.route("/lista/pets",methods=["GET"])
def listarpet():
    try:
        conn = mysql.connection
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tbl_pets')
        lista = cursor.fetchall()
        print(lista[0])

        return render_template('listarpets.html', Lista = lista)

    except Exception as e:
        return json.dumps({'error': str(e)})

@app.route('/lista/tutores/<int:cpf>',methods=["PUT","GET","POST"])
def update(cpf):
    try:
        cpf = int(cpf)
        conn = mysql.connection
        cursor = conn.cursor()
        cursor.execute('SELECT CPF FROM tbl_tutor WHERE CPF = %s', (cpf))
        lista = cursor.fetchall()
        print(lista[0])

        _namet = request.form['inputNameT']
        _lastnamet = request.form['inputLastName']
        _email = request.form['inputEmail']
        _addresst = request.form['inputAddress']
        _phoneT = request.form['inputPhone']
        _cpf = request.form['inputCpf']
        _ageT = request.form['inputAgeT']

        print(_namet)
        
        cursor.execute('UPDATE tbl_tutor SET Nome = %s, Sobrenome = %s, Email = %s, Endereco = %s, Telefone = %s, CPF = %s, Idade = %s',(_namet, _lastnamet, _email, _addresst, _phoneT, _cpf, _ageT))
        conn.commit()
        msg = "Atualizado com sucesso"

        return render_template('listarpets.html', Lista = lista, mensagem = msg)

    except Exception as e:
        return json.dumps({'error': str(e)})

@app.route('/lista/tutores/<int:cpf>',methods=['DELETE'])
def delete(cpf):
    try:
        cpf = int(cpf)
        conn = mysql.connection
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tbl_tutor WHERE CPF = %s', (cpf))
        conn.commit()
        lista = cursor.fetchall()
        msg = "Excluido com sucesso"
        print(lista[0])

        return render_template('listarpets.html', Lista = lista, mensagem = msg)
    
    except Exception as e:
        return json.dumps({'error': str(e)})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)