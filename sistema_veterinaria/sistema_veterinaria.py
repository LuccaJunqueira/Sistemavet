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
,CONSTRAINT tutorcpf_tutor_pk PRIMARY KEY(CPF)
,CONSTRAINT petname_pet_fk FOREIGN KEY(Pet) REFERENCES tbl_pets(Nome)
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
,CONSTRAINT tutorcpf_tutor_fk FOREIGN KEY(CPFTutor) REFERENCES tbl_tutor(CPF)
);

SELECT * FROM tbl_pets

COMO FUNCIONOU:

CREATE SCHEMA IF NOT EXISTS vet;

USE vet;

CREATE TABLE IF NOT EXISTS tbl_tutor 
(	
    CPF			VARCHAR(30)		NOT NULL,
    Nome		VARCHAR(50)		NOT NULL,
	Sobrenome	VARCHAR(50)		NOT NULL,
    Email		VARCHAR(50)		NOT NULL,
    Endereco	VARCHAR(50)		NOT NULL,
    Telefone	VARCHAR(30)		NOT NULL,
    Idade		INT
,CONSTRAINT uqcpf UNIQUE (CPF)
,CONSTRAINT tutorcpf_tutor_pk PRIMARY KEY(CPF)
,CONSTRAINT ckidade CHECK (Idade >= 18)
);

CREATE TABLE IF NOT EXISTS tbl_pets
(
PetID BIGINT NOT NULL AUTO_INCREMENT
, Nome VARCHAR(20) NOT NULL
, Especie VARCHAR(30) NOT NULL
, Raca VARCHAR(20)
, Cor VARCHAR(20)
, Idade INT
, CPF VARCHAR(30)	NOT NULL
,CONSTRAINT pet_id_pk PRIMARY KEY(PetID)
,CONSTRAINT tutorcpf_tutor_fk FOREIGN KEY(CPF) REFERENCES tbl_tutor(CPF)
);

SELECT * FROM tbl_pets;

'''

import os
from flask import Flask, render_template, json, request,jsonify
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
    return render_template('index.html')

@app.route('/cadastrar/tutores')
def cadastrar_tutores():
    return render_template('form.html')

@app.route('/cadastrar/pets')
def cadastrar_pets():
    return render_template('formpets.html')

@app.route('/cadastro/tutores',methods=['POST','GET'])
def cadastro_tutores():
    try:
        cpf_tutor = request.form['inputCpfTutor']
        name_tutor = request.form['inputNameTutor']
        lastname_tutor = request.form['inputLastNameTutor']
        email_tutor = request.form['inputEmailTutor']
        address_tutor = request.form['inputAddressTutor']
        phone_tutor = request.form['inputPhoneTutor']
        age_tutor = request.form['inputAgeTutor']

        print(cpf_tutor)
        print(name_tutor)
        print(lastname_tutor)
        print(email_tutor)
        print(address_tutor)
        print(phone_tutor)
        print(age_tutor)

        
        cur = mysql.connection.cursor()
        cur.execute("SELECT CPF FROM tbl_tutor WHERE CPF = %s", (cpf_tutor,))
        #EXIJO ESPLICACOES DO PQ PRECISA DE UMA VIRGULA NO FINAL DESSA MERDA
        resultado = cur.fetchone()
        print(resultado)
            
        if resultado:
            msg = "CPF ja cadastrado no banco de dados"
            return render_template('form.html', mensagem = msg)
        else:
            conn = mysql.connection
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tbl_tutor (CPF,Nome,Sobrenome,Email,Endereco,Telefone,Idade) VALUES (%s, %s, %s, %s, %s, %s, %s)", ( cpf_tutor,name_tutor,lastname_tutor,email_tutor,address_tutor,phone_tutor,age_tutor ))
            #Alt  + Z para quebra linhas grandes
            conn.commit()
            msg = "Tutor cadastrado com sucesso"

            return render_template('form.html', mensagem = msg)
        
    except Exception as e:
        return json.dumps({'error': str(e)})
    
@app.route('/cadastro/pets',methods=['POST','GET'])
def cadastro_pets():
    try:
        name_pet = request.form['inputNamePet'].title().strip()
        specie_pet = request.form['inputSpeciePet']
        race_pet = request.form['inputRacePet']
        color_pet = request.form['inputColorPet']
        age_pet = request.form['inputAgePet']
        cpf_pet_tutor= request.form['inputCpfPetTutor']


        print(name_pet)
        print(specie_pet)
        print(race_pet)
        print(color_pet)
        print(age_pet)
        print(cpf_pet_tutor)

        if name_pet and specie_pet and race_pet:
        
            if int(age_pet) < 0 :
                raise ValueError
            
            cur = mysql.connection.cursor()
            cur.execute("SELECT Nome FROM tbl_pets WHERE Nome = %s", (name_pet,))
            resultado = cur.fetchone()
            print(resultado)

            if resultado:
                msg = 'Esse nome ja esta cadastrado'
                return render_template('formpets.html', mensagem = msg)
            
            else:
                conn = mysql.connection
                cursor = conn.cursor()
                cursor.execute("INSERT INTO tbl_pets (Nome,Especie,Raca,Cor,Idade,CPF) Values (%s, %s, %s, %s, %s, %s)", (name_pet, specie_pet, race_pet, color_pet, age_pet, cpf_pet_tutor))
                conn.commit()
                msg = "Pet cadastrado com sucesso"


                return render_template('formpets.html', mensagem = msg)
        
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
        cursor.execute('SELECT * FROM tbl_tutor')
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

        name_tutor = request.form['inputNameTutor']
        lastname_tutor = request.form['inputLastNameTutor']
        email_tutor = request.form['inputEmailTutor']
        address_tutor = request.form['inputAddressTutor']
        phone_tutor = request.form['inputPhoneTutor']
        cpf_tutor = request.form['inputCpfTutor']
        age_tutor = request.form['inputAgeTutor']

        print(name_tutor)
        
        cursor.execute('UPDATE tbl_tutor SET Nome = %s, Sobrenome = %s, Email = %s, Endereco = %s, Telefone = %s, CPF = %s, Idade = %s',(name_tutor, lastname_tutor, email_tutor, address_tutor, phone_tutor, cpf_tutor, age_tutor))
        conn.commit()
        msg = "Atualizado com sucesso"

        return render_template('editar.html', Lista = lista, mensagem = msg)

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

        return render_template('listar.html', Lista = lista, mensagem = msg)
    
    except Exception as e:
        return json.dumps({'error': str(e)})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True) 