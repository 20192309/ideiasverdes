from calendar import c
from email.policy import default
from ssl import ALERT_DESCRIPTION_ACCESS_DENIED
from flask import Flask, render_template, request, flash, session, redirect, url_for     # Importa-se a biblioteca do Flask
from datetime import datetime
#from operator import truediv
from os import curdir
import os
#from pickle import TRUE
import sqlite3
import hashlib , string, random
from werkzeug.utils import secure_filename
import urllib.request
import csv

app = Flask(__name__)       # Cria-se uma "Aplicação Flask"
#from asyncio.windows_events import NULL
#from re import L, S
#from markupsafe import escape

'''
connection = sqlite3.connect("/var/www/webApp/webApp/ideiasverdes.db")
cursor = connection.cursor()
'''

path="/var/www/webApp/webApp/static/"
UPLOAD_FOLDER = path#'/path/to/the/uploads'
ALLOWED_EXTENSIONS = { 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def cheaninput(input):
    print("a limpar**********")
    print(input)
    inputsplited = input.split()
    file = open("/var/www/webApp/webApp/static/cleaninputs.csv", "r")
    csv_reader = csv. reader(file)
    listacsv=[]
    for row in csv_reader:
        listacsv.append(row)
    listacsv=listacsv[0]

    file2 = open("/var/www/webApp/webApp/static/cleaninputswords.csv", "r")
    csv_reader2 = csv. reader(file2)
    listacsv2=[]
    for row in csv_reader2:
        listacsv2.append(row)
    listacsv2=listacsv2[0]

    print(inputsplited)
    listaclean = []
    listacleaned=[]
    listacleanwords=[]
    for i in inputsplited:
        for j in listacsv:
            i=i.replace(j," ")
        listaclean.append(i)
    print (listaclean)
    #listaclean = listaclean.split()
    for i in listaclean: 
        splitme=i.split()
        print (splitme)
        for k in splitme:
            k=k.lower()
            print (k)
            if k not in listacsv2:
                listacleaned.append(k)
    cleaned=listacleaned
    print(cleaned)
    print("limpeza feita*****")
    return cleaned

def dataagora():
    dataatual= datetime.now()
    dataatual=dataatual.strftime("%d/%m/%Y")
    return dataatual

def verificaPalavraPasse(salt, hash, passwd):
    bytes = (salt+passwd).encode()
    return(hashlib.sha256(bytes).digest() == hash)
    
def geraHash(passwd):
    caracteres = string.ascii_letters+string.digits+string.punctuation
    # Gera um salt de 16 bits aleatoriamente
    salt = ''.join(random.choices(caracteres, k=16))
    # Gera o hash (SHA 256) do salt + palavra-passe
    hash = hashlib.sha256((salt+passwd).encode())
    return (salt, hash.digest())


def verificaLogin(username, password):
    connection = sqlite3.connect("/var/www/webApp/webApp/logins.db")
    cursor = connection.cursor()
    consulta=cursor.execute('select * from login where user = (?)',(username,))
    consulta=cursor.fetchone()
    print(consulta)
    #verificaPalavraPasse(dic[user]["salt"], dic[user]["hash"], passwd_in))
    connection.close()
    if consulta is not None:
        if username == consulta[1]:
            if verificaPalavraPasse(consulta[3], consulta[2], password):
        #if password==consulta[2]:
        #if username == "pedro" and password == "123456":
                return True
        return False
    return False

def organizardicionario(lista):
    print(lista)
    chaves=["id", "nome", "url"]
    dicionario={}
    for i in chaves:
        dicionario[i]=''
    print (dicionario)
    for i in lista:
        print (i)
        for k in i:
            print (k)
            for i in range(len(chaves)):
                print (k[i])
                #dicionario.append[chaves[i]]=k[i]


def inseirlojas(lojasinserir, id):
    connection = sqlite3.connect("/var/www/webApp/webApp/ideiasverdes.db")
    cursor = connection.cursor()
    for i in lojasinserir:
        consulta=cursor.execute('select id from lojas where loja_nome = (?)',(i[1],) )
        consulta=cursor.fetchone()
        if consulta is None:
            cursor.execute('INSERT INTO lojas(id, loja_nome, url) VALUES (null,?,?)',(i[1],i[2],))
            connection.commit()
            consulta=cursor.execute('select id from lojas where loja_nome = (?)',(i[1],) )
            consulta=cursor.fetchone()
        else:
            idloja=consulta[0]
            cursor.execute('UPDATE lojas SET loja_nome=?, url=? WHERE id=?',(i[1],i[2],idloja,))
            connection.commit()
        print(consulta[0])
        cursor.execute('INSERT INTO loja_ideia(id, ideia_id, loja_id) VALUES (null,?,?)',(id, consulta[0],))
        connection.commit()
    connection.close()

def inserireditor(neweditor, id):
    connection = sqlite3.connect("/var/www/webApp/webApp/ideiasverdes.db")
    cursor = connection.cursor()
    neweditor=neweditor[0]
    print(neweditor)
    consulteditornome=cursor.execute('select id from editores where editor_nome = (?)',(neweditor,) )   
    consulteditornome=cursor.fetchone()
    if consulteditornome is None:
        cursor.execute('INSERT INTO editores(id, editor_nome, teamplace) VALUES (null,?,?)',(neweditor,"",))
        connection.commit()
        print("inserido")
    consulteditor2=cursor.execute('select id from editores where editor_nome = (?)',(neweditor,) )
    consulteditor2=cursor.fetchone()
    print(consulteditor2)
    print(consulteditor2[0])
    cursor.execute('INSERT INTO editor_ideia(id, ideia_id, editor_id) VALUES (null,?,?)',(id, consulteditor2[0],))
    connection.commit()
    connection.close()

def inserirpalavras(adicionar, id):
    connection = sqlite3.connect("/var/www/webApp/webApp/ideiasverdes.db")
    cursor = connection.cursor()
    for i in adicionar:
        consulta5=cursor.execute('select id from palavras where palavra = (?)',(i,) )
        consulta5=cursor.fetchone()
        print(i)
        if consulta5 is None:
            cursor.execute('INSERT INTO palavras(id, palavra, familia) VALUES (null,?,?)',(i,"",))
            connection.commit()
            consulta5=cursor.execute('select id from palavras where palavra = (?)',(i,) )
            consulta5=cursor.fetchone()
        print(consulta5[0])
        cursor.execute('INSERT INTO palavra_ideia(id, ideia_id, palavra_id) VALUES (null,?,?)',(id, consulta5[0],))
        connection.commit()
    connection.close()

def procurarideia(ideia):
    ideianum=ideia
    connection = sqlite3.connect("/var/www/webApp/webApp/ideiasverdes.db")
    cursor = connection.cursor()
    ideiaconsulta=cursor.execute('select * from ideias where id = (?)',(ideia,) )
    ideiaconsulta=cursor.fetchone()
    print(ideia)
    listaideia=[]
    ideia={}
    ideia["id"]=ideiaconsulta[0]
    ideia["nome_ideia"]=ideiaconsulta[1]
    ideia["impacto_ind"]=ideiaconsulta[2]
    ideia["impacto_col"]=ideiaconsulta[3]
    ideia["esforco"]=ideiaconsulta[4]
    ideia["fact_cient"]=ideiaconsulta[5]
    ideia["descricao"]=ideiaconsulta[6]
    ideia["curiosidade"]=ideiaconsulta[7]
    ideia["mais_info"]=ideiaconsulta[8]
    ideia["videos"]=ideiaconsulta[9]
    ideia["estudos"]=ideiaconsulta[10]
    ideia["imagem"]=ideiaconsulta[11]
    ideia["data_cria"]=ideiaconsulta[12]
    ideia["data_revi"]=ideiaconsulta[13]
    editorconsulta=cursor.execute('select editor_id from editor_ideia where ideia_id = (?)',(ideianum,) )
    editorconsulta=cursor.fetchone()
    print(editorconsulta)
    editorconsulta=editorconsulta[0]
    print(editorconsulta)
    editorconsulta=cursor.execute('select editor_nome from editores where id = (?)',(editorconsulta,) )
    editorconsulta=cursor.fetchone()
    editorconsulta=editorconsulta[0]
    print (editorconsulta)
    ideia["editor"]=editorconsulta
    
    lojaconsulta=cursor.execute('select loja_id from loja_ideia where ideia_id = (?)',(ideianum,) )
    lojaconsulta=cursor.fetchall()
    listalojas=[]
    lista=[]
    for i in range(len(lojaconsulta)):
        l=lojaconsulta[i]
        lista.append(l[0])
    print (lista)
    print(lojaconsulta)
    for i in range(len(lista)):
        listaid=lista[i]
        lojaconsulta=cursor.execute('select * from lojas where id = (?)',(listaid,) )
        lojaconsulta=cursor.fetchall()
        print(lojaconsulta)
        listalojas.append(lojaconsulta)
        #listalojas.append(lojaconsulta)
    print(listalojas)
    #listalojasorg=organizardicionario(listalojas)
    #print(listalojasorg)
    ideia["lojas"]=listalojas
    
    palavrasconsulta=cursor.execute('select palavra_id from palavra_ideia where ideia_id = (?)',(ideianum,) )
    palavrasconsulta=cursor.fetchall()
    listapalavras=[]
    lista2=[]
    for i in range(len(palavrasconsulta)):
        p=palavrasconsulta[i]
        lista2.append(p[0])
    for i in range(len(lista2)):
        palavraid=lista2[i]
        palavraconsulta=cursor.execute('select palavra from palavras where id = (?)',(palavraid,) )
        palavraconsulta=cursor.fetchone()
        print(palavraconsulta)
        palavraconsulta=palavraconsulta[0]
        print(palavraconsulta)
        listapalavras.append(palavraconsulta)
    print(listapalavras)
    ideia["palavras"]=listapalavras

    listaideia.append(ideia.copy())
    print (ideia)
    print(listaideia)
    connection.close()

    return listaideia


def removerideiaderelacoes(ideia, tabela):# a enviar 1- id da ideia, 2-tabela onde é para remover a ideia
        connection = sqlite3.connect("/var/www/webApp/webApp/ideiasverdes.db")
        cursor = connection.cursor()
        print("remover dados de "+tabela)
        consultaremedit=cursor.execute('select id from '+tabela+' where ideia_id = (?)',(ideia,) )
        consultaremedit=cursor.fetchall()
        print(consultaremedit)
        if consultaremedit is not None:
            for i in consultaremedit:
                cursor.execute('DELETE FROM '+tabela+' WHERE id=(?)',(i[0],) )
                connection.commit()
        connection.close()

@app.route("/failedwords", methods=["POST", "GET"])#https://stackoverflow.com/questions/21498694/flask-get-current-route
@app.route("/", methods=["POST", "GET"])
def home():
    if 'username' in session:
        #return f"Seja bem-vindo, {session['username']}"
        print("in session")
        return redirect(('loginadmin'))
    else:
        print("not in session")
        connection = sqlite3.connect("/var/www/webApp/webApp/ideiasverdes.db")
        cursor = connection.cursor()
        ids=cursor.execute('select palavra_id from palavra_ideia')
        ids=cursor.fetchall()
        palavras=[]
        print(ids)
        for i in ids:
            consultawords=cursor.execute('select palavra from palavras WHERE id = (?)',(i[0],) )
            consultawords=cursor.fetchone()
            if consultawords[0] not in palavras:
                palavras.append(consultawords[0])
        print(palavras)
        rule = request.url_rule
        print(rule)
        alerta='Não foi possivel encontrar resultados com a sua pesquisa, sugerimos utilizar as palavras sugeridas abaixo'
        if 'failedwords' in rule.rule:
            return render_template('home.html', palavras=palavras, alerta=alerta)
        return render_template('home.html', palavras=palavras) 

@app.route("/conceitos", methods=['GET', 'POST'])
def conceitos():
    return render_template('conceitos.html')


@app.route("/loginadmin", methods=['GET', 'POST'])
def backbutton():
    return redirect(('urldopaineldeadministracao'))

@app.route("/urldopaineldeadministracao", methods=['GET', 'POST'])
def login():
    if 'username' in session:
        print("in session")
        #return f"Seja bem-vindo, {session['username']}"
        return render_template('adminhome.html')
    else:
        if request.method == 'POST':
            if verificaLogin(request.form['username'], 
                    request.form['password']):
                session['username'] = request.form['username']
                return render_template('adminhome.html')
            else:
                return render_template('loginfailed.html')
        return render_template('login.html')

@app.route("/logout", methods=['GET', 'POST'])
def logout():

    if 'username' in session:
        print("removed session")
        session.clear()
        #return f"Seja bem-vindo, {session['username']}"
        return redirect(('/'))
    else:
        return redirect(('/'))

@app.route("/newuser", methods=['GET', 'POST'])
def newuser():
    return render_template('registerlogin.html')
'''
@app.route("/newlogin", methods=['GET', 'POST'])
def newlogin():
    newpass=request.form['password']
    newemail=request.form['email']
    newuser=request.form['username']
    print(newemail)
    print(newpass)
    print(newuser)
    newpasswordhashed = geraHash(newpass)
    connection = sqlite3.connect("/var/www/webApp/webApp/logins.db")
    cursor = connection.cursor()
    cursor.execute('INSERT INTO login(id, user, password, passwords, email) VALUES (null,?,?,?,?)',(newuser, newpasswordhashed[1], newpasswordhashed[0], newemail,))
    connection.commit()
    connection.close()
    return redirect(('loginadmin'))
'''

@app.route("/criarID", methods=['GET', 'POST'])
def criaridideia():
    connection = sqlite3.connect("/var/www/webApp/webApp/ideiasverdes.db")
    cursor = connection.cursor()
    id=1
    lastid=cursor.execute('select id from ideias ORDER BY id DESC LIMIT 1', ) #ORDER BY id DESC LIMIT 1
    lastid=cursor.fetchall()
    print(lastid[0])
    id=lastid[0]
    newid=id[0]+1
    print(newid)        
    connection.close()

    return render_template('criarideia.html',newid=newid)

@app.route("/criarideia", methods=['GET', 'POST'])
def criarideia():
    connection = sqlite3.connect("/var/www/webApp/webApp/ideiasverdes.db")
    cursor = connection.cursor()
    dictnewideia=request.form.to_dict(flat=False)
    print("ideia recolhida do FORM")
    print(dictnewideia)
    id=request.form['id']
    ideiaexistente=cursor.execute('select * from ideias where id = (?)',(id,) )
    ideiaexistente=cursor.fetchone()
    if ideiaexistente is None:
        print("criar ideia")
        newideia=[]
        newideiapalavras=[]
        newideialojas=[]
        newideialojasurl=[]
        newideiaeditor=[]
        newideia.append(request.form['id'])
        newideia.append(request.form['nome'])
        newideia.append(request.form['Impacto individual'])
        newideia.append(request.form['Impacto coletivo'])
        newideia.append(request.form['Esforco'])
        newideia.append(request.form['Facto Cientifico'])
        newideia.append(request.form['Descricao'])
        newideia.append(request.form['Curiosidade'])
        newideia.append(request.form['moreinfo'])
        newideia.append(request.form['Videos'])
        newideia.append(request.form['Estudos'])
                
        now = datetime.now()
        print("em upload")
        if request.method == 'POST':
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            print(request.files)
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                print("gravar file")
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                #return redirect(url_for('download_file', name=filename))
        print("File saved maybe")
        ideiaimg=str(id)+".png"
        newideia.append(filename)
        '''
        #if request.method == 'POST':
        file = request.files.get('files')
        print(file)
        #for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print("gravar file")
            file.save(os.path.join('/var/www/webApp/webApp/static/uploads', filename))#app.config['UPLOAD_FOLDER'] no lugar do caminho
            #cursor.execute("INSERT INTO images (id, file_name, uploaded_on, status) VALUES (null,?,?,null)",(filename, now))
            #connection.commit()
            print(file)
            #filename=allowed_file(file.filename)
        #name =request.FILES['filename'].name
        #print(name)
        #newideia.append(filename)
        '''

        agoranovo=dataagora()
        newideia.append(agoranovo)
        newideia.append("")
        print(newideia)
        newideiapalavras = dictnewideia['palavrainserir']
        newideialojas = dictnewideia['lojainserir']
        newideialojasurl = dictnewideia['loja urlinserir']
        newideiaeditor = dictnewideia['Editor']
        if "tudo" not in newideiapalavras:
            newideiapalavras.append("tudo")
        newlistapalavras=[]
        for i in newideiapalavras:
            if i not in newlistapalavras:
                newlistapalavras.append(i)#remover duplicados
        print(newlistapalavras)
        print(newideialojas)
        print(newideialojasurl)
        listaideialojaseurl=[]
        for i in range(len(newideialojas)):
            tupla=("0", newideialojas[i],newideialojasurl[i])
        listaideialojaseurl.append(tupla)
        print(listaideialojaseurl)
        print(newideiaeditor)
        #ate este ponto foi trabalhado o conteudo inserido pelo utilizador
        #e preparado para ser introduzido na base de dados
        #passo esse que sera realizado de seguida
        print("inserir ideia")
        cursor.execute('INSERT INTO ideias(id, nome_ideia, impacto_ind, impacto_col, esforco, fact_cient, descricao, curiosidade, mais_info, videos, estudos, imagem, data_cria, data_revi) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)',newideia)
        connection.commit()
        print("inserir palavras")
        inserirpalavras(newlistapalavras, id)
        print("inserir loja")
        inseirlojas(listaideialojaseurl, id)
        print("inserir editor")
        inserireditor(newideiaeditor, id)



        print("terminado processo de inserir dados")
    else:
        print("ideia existe")
        print(ideiaexistente)
    
    connection.close()
    return render_template('adminhome.html')

@app.route("/search/<string:search>",defaults={'search':"tudo"}, methods=["POST", "GET"]) #não seria necessário neste     # O decorator app.route() associa a função ao caminho "/" no servidor
@app.route("/search", defaults={'search':"tudo"}, methods=["POST", "GET"]) #não seria necessário neste     # O decorator app.route() associa a função ao caminho "/" no servidor
def search(search):
    connection = sqlite3.connect("/var/www/webApp/webApp/ideiasverdes.db")
    cursor = connection.cursor()
    if request.form['search'] is not None:
        words=request.form['search']
    else:
        words=request.args.get('search')    
    #words=request.form['search']
    print (words)
    wordscleaned=cheaninput(words)
    listaidwords=[]
    listawords=wordscleaned
    for i in range(len(listawords)):
        consultaid=cursor.execute('select id from palavras where palavra = (?)',(listawords[i],) )
        consultaid=cursor.fetchone()
        if consultaid is not None:
            consultaid=consultaid[0]
            listaidwords.append(consultaid)
    print (listaidwords)
#----------------------------------------------------------------
    idslista=[]
    for i in range(len(listaidwords)):
        consult2id=cursor.execute('select ideia_id from palavra_ideia where palavra_id = (?)',(listaidwords[i],) )
        consult2id=cursor.fetchall()
        if consult2id is not None:
            print (consult2id)
            for i in consult2id:
                i=i[0]
                print (i)
                if i not in idslista:
                    idslista.append(i)
    print (idslista)
    #connection.commit()
    ideiasnomes = []
    ideiasimagens = []
    for i in range(len(idslista)):
        consultideia=cursor.execute('select nome_ideia from ideias where id = (?)',(idslista[i],) )
        consultideia=cursor.fetchone()
        consultideia=consultideia[0]
        ideiasnomes.append(consultideia)
        consulimg=cursor.execute('select imagem from ideias where id = (?)',(idslista[i],) )
        consulimg=cursor.fetchone()
        consulimg= consulimg[0]
        ideiasimagens.append(consulimg)
    print(idslista)
    print(ideiasimagens)
    print(ideiasnomes)
    listagrelha = []
    grelha={}
    for i in range(len(idslista)):
        grelha["id"]=idslista[i]
        grelha["nome"]=ideiasnomes[i]
        grelha["imagem"]=ideiasimagens[i]
        listagrelha.append(grelha.copy())
        print (grelha)
        print(listagrelha)
    print(listagrelha)

    '''
    1- receber uma string 
    2- passar para lista e fazer split, e limprar a mesma
    3- for i in len lista, fazer query sql 
        se ja existir na lista o id da ideia ignora
        se nao adiciona (apendd)-----
    4- consulta sql para cirar uma lista com
        imagem e descrição por ordem da lista de ideias
    5- passar as listas para o user
        no html, for de div para criar a grelha
    '''
    connection.close()
    if listagrelha:
        return render_template('ideiasgrelha.html', listagrelha=listagrelha)
    else:
        return redirect(('/failedwords'))
        

@app.route("/consultideia", methods=["POST", "GET"])
def consultideia():

    if request.args.get('id') is not None:
        id=str(request.args.get('id'))
        print(id)
        id=int(id)
    else:        
        ideia=request.form['consultideia']
    
    print(ideia)
    ideianum=ideia
    listaideia=procurarideia(ideianum)
    return render_template("ideia.html", listaideia=listaideia)    # Valor retornado é simplesmente uma string enviada como (corpo) da resposta HTTP.


@app.route("/procurar", methods=['GET', 'POST'])
def procurar():
    ideia=request.form['findID']
    print(ideia)
    ideianum=ideia
    ideiaalterar=procurarideia(ideianum)
    return render_template('alterideia.html',ideiaalterar=ideiaalterar)


@app.route("/ideiaalterar", methods=['GET', 'POST'])
def alteraideia():
    #img=request.files['file']
    file= request.files['file']
    #print(img)
    print(file)
    print("********************Request***********")
    formall=[]
    formall=request.form.to_dict(flat=False)
    print(formall)  
    connection = sqlite3.connect("/var/www/webApp/webApp/ideiasverdes.db")
    cursor = connection.cursor()
    id=request.form['id']
    print (id)
    cursor.execute('SELECT * from ideias WHERE id= (?)',id)
    ideiaold=cursor.fetchall()
    print("OLD IDEIA***************************")
    print(ideiaold)
    ideiaold=ideiaold[0]
    alteradaideia=[]
    alteradaideia.append(request.form['nome'])
    alteradaideia.append(request.form['Impacto individual'])
    alteradaideia.append(request.form['Impacto coletivo'])
    alteradaideia.append(request.form['Esforco'])
    alteradaideia.append(request.form['Facto Cientifico'])
    alteradaideia.append(request.form['Descricao'])
    alteradaideia.append(request.form['Curiosidade'])
    alteradaideia.append(request.form['moreinfo'])
    alteradaideia.append(request.form['Videos'])
    alteradaideia.append(request.form['Estudos'])
    filename=ideiaold[11]
    print("em upload")
    #if request.method == 'POST':
    # check if the post request has the file part
    print(request.files)
    print(formall["loja"])
    formall["loja"]
    if 'file' not in request.files:
        print("nao foi submetido nenhum ficheiro")
        #return redirect(request.url)
    if 'file' in request.files:
        file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
        if file.filename == '':
            print('No selected file')
        #return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print("gravar file")
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #return redirect(url_for('download_file', name=filename))
            print("File saved maybe")
#ideiaimg=str(id)+".png"
    alteradaideia.append(filename)
    #alteradaideia.append(ideiaold[11])
    
    alteradaideia.append(ideiaold[12])
    agoraalterar=dataagora()
    alteradaideia.append(agoraalterar)
    alteradaideia.append(request.form['id'])
    print("***************_______________*************")
    print(alteradaideia) 
    cursor.execute('UPDATE ideias SET nome_ideia=?, impacto_ind=?, impacto_col=?, esforco=?, fact_cient=?, descricao=?, curiosidade=?, mais_info=?, videos=?,estudos=?, imagem=?, data_cria=?, data_revi=? WHERE id=?',alteradaideia)
    connection.commit()
   
    print("********************Lojas***********")
    lojaconsulta=cursor.execute('select loja_id from loja_ideia where ideia_id = (?)',(id,) )
    lojaconsulta=cursor.fetchall()
    listalojas=[]
    lista=[]
    for i in range(len(lojaconsulta)):
        l=lojaconsulta[i]
        lista.append(l[0])
    print (lista)
    for i in range(len(lista)):
        listaid=lista[i]
        lojaconsulta=cursor.execute('select * from lojas where id = (?)',(listaid,) )
        lojaconsulta=cursor.fetchone()
        print(lojaconsulta)
        listalojas.append(lojaconsulta)
    novaslojas=[]
    novaslojas=formall["loja"]
    novaslojasurl=formall["loja url"]
    listanewlojas=[]
    for i in range(len(novaslojas)):
        val=False
        for k in listalojas:
            if novaslojas[i] == k[1]:
                idloja=k[0]
                val=True
        if val==False:
            idloja='new'        
        tupla=(idloja, novaslojas[i],novaslojasurl[i])
        listanewlojas.append(tupla)
    print ("old lojas" )
    print(listalojas)
    print ("novas lojas" )
    print(listanewlojas)
    adicionarlojas=[]
    removerlojas=[]
    atualizarlojas=[]
    #o seginte passo apesar de estranho é necessário 
    #serve para atualizar o url de lojas em que possa ter sido atulizado o url da loja
    #assim mantem-se todas as ideias que tenham essa loja atualizadas
    #sem ter de ir loja a loja atualizar
    #o exempo estara no relatorio final
    for i in listanewlojas:
        if i not in listalojas:
            adicionarlojas.append(i)
    print("adcionar not filter:")
    print(adicionarlojas)
    for i in listalojas:
        if i not in listanewlojas:
            removerlojas.append(i)
    print("remover not filter:")
    print(removerlojas)
    for i in adicionarlojas:
        for k in listalojas:
            if i[1] in k:
                atualizarlojas.append(i)
                adicionarlojas.remove(i)
    print("adcionar:")
    print(adicionarlojas)
    print("atualizar:")
    print(atualizarlojas)
    for i in removerlojas:
        for k in listanewlojas:
            if i[1] in k:
                atualizarlojas.append(k)
                removerlojas.remove(i)
    print("remover:")
    print(removerlojas)
    print("atualizar")
    print(atualizarlojas)
    atualizarclean=[]
    for i in atualizarlojas:
        if i not in atualizarclean:
            atualizarclean.append(i)
    print("atualizados limpos:"+ str(atualizarclean))
    #uma vez limpa e tratada a informação agora será feita a interacao com a DB
    #vamos adicionar, remover, e atualizar dados
    #adicionar
    for i in adicionarlojas:
        consulta=cursor.execute('select id from lojas where loja_nome = (?)',(i[1],) )
        consulta=cursor.fetchone()
        if consulta is None:
            cursor.execute('INSERT INTO lojas(id, loja_nome, url) VALUES (null,?,?)',(i[1],i[2],))
            connection.commit()
            consulta=cursor.execute('select id from lojas where loja_nome = (?)',(i[1],) )
            consulta=cursor.fetchone()
        else:
            idloja=consulta[0]
            cursor.execute('UPDATE lojas SET loja_nome=?, url=? WHERE id=?',(i[1],i[2],idloja,))
            connection.commit()
        print(consulta[0])
        cursor.execute('INSERT INTO loja_ideia(id, ideia_id, loja_id) VALUES (null,?,?)',(id, consulta[0],))
        connection.commit()
    
    for k in removerlojas:
        consultarem=cursor.execute('select id from lojas where loja_nome = (?)',(k[1],) )#talvez seja escusado uma vez que temos o id em k[0]
        consultarem=cursor.fetchone()
        consultarem1=cursor.execute('select id from loja_ideia where ideia_id = (?) and loja_id = (?)',(id, consultarem[0]) )
        consultarem1=cursor.fetchone()
        print(k)
        print(consultarem[0])
        print(consultarem1[0]) 
        cursor.execute('DELETE FROM loja_ideia WHERE id=(?)',(consultarem1[0],) )
        connection.commit()
    
    for j in atualizarlojas:
        consultaalt=cursor.execute('select id from lojas where loja_nome = (?)',(j[1],) )
        consultaalt=cursor.fetchone()
        print(consultaalt[0])
        cursor.execute('UPDATE lojas SET loja_nome=?, url=? WHERE id=?',(j[1],j[2],consultaalt[0],))
        connection.commit()


    print("********************Palavras***********")
    novaspalavras=[]
    novaspalavras=formall["palavra"]
    if "tudo" not in novaspalavras:
        novaspalavras.append("tudo")
    oldpalavras=[]
    oldidpalavras=[]
    consult3id=cursor.execute('select palavra_id from palavra_ideia where ideia_id = (?)',(id,) )    
    consult3id=cursor.fetchall()
    for i in consult3id:
        oldidpalavras.append(i[0])
    print(oldidpalavras)
    for i in range(len(consult3id)):
        consultaid=cursor.execute('select palavra from palavras where id = (?)',(oldidpalavras[i],) )
        consultaid=cursor.fetchone()
        if consultaid is not None:
            consultaid=consultaid[0]
            oldpalavras.append(consultaid)
    oldpalavras.sort()
    novaspalavras.sort()
    while '' in oldpalavras:
        oldpalavras.remove('')
    while '' in novaspalavras:
        novaspalavras.remove('')
    print (oldpalavras)
    print (novaspalavras)
    adicionar=[]
    remover=[]
    if oldpalavras != novaspalavras:
        for i in oldpalavras:
            if i in novaspalavras:
                print (i+ " existe")
            else:
                remover.append(i)
        for k in novaspalavras:
            if k in oldpalavras:
                print (k+ " existe")
            else:
                adicionar.append(k)
    print (adicionar)
    print (remover)
    for i in adicionar:
            consulta5=cursor.execute('select id from palavras where palavra = (?)',(i,) )
            consulta5=cursor.fetchone()
            print(i)
            #consulta5=consulta5[0]
            if consulta5 is None:
                cursor.execute('INSERT INTO palavras(id, palavra, familia) VALUES (null,?,?)',(i,"",))
                connection.commit()
                consulta5=cursor.execute('select id from palavras where palavra = (?)',(i,) )
                consulta5=cursor.fetchone()
            print(consulta5[0])
            cursor.execute('INSERT INTO palavra_ideia(id, ideia_id, palavra_id) VALUES (null,?,?)',(id, consulta5[0],))
            connection.commit()
    for k in remover:
        consulta6=cursor.execute('select id from palavras where palavra = (?)',(k,) )
        consulta6=cursor.fetchone()
        consulta7=cursor.execute('select id from palavra_ideia where ideia_id = (?) and palavra_id = (?)',(id, consulta6[0]) )
        consulta7=cursor.fetchone()
        print(k)
        print(consulta6[0])
        print(consulta7[0]) 
        cursor.execute('DELETE FROM palavra_ideia WHERE id=(?)',(consulta7[0],) )
        connection.commit()

    print("*************************EDITOR******************")
    neweditor=formall["Editor"]
    print(neweditor)
    neweditor=neweditor[0]
    print(neweditor)
    consulteditor=cursor.execute('select editor_id from editor_ideia where ideia_id = (?)',(id,) )    
    consulteditor=cursor.fetchall()
    print(consulteditor)
    consulteditor=consulteditor[0]
    consulteditor=cursor.execute('select editor_nome from editores where id = (?)',(consulteditor[0],) )    
    consulteditor=cursor.fetchall()
    print(consulteditor[0])
    if consulteditor[0] != neweditor:
        consulteditor4=cursor.execute('select id from editores where editor_nome = (?)',(neweditor,) )   
        consulteditor4=cursor.fetchone()
        if consulteditor4 is None:
            cursor.execute('INSERT INTO editores(id, editor_nome, teamplace) VALUES (null,?,?)',(neweditor,"",))
            connection.commit()
            print("inserido")
        consulteditor2=cursor.execute('select id from editores where editor_nome = (?)',(neweditor,) )
        consulteditor2=cursor.fetchone()
        print(consulteditor2)
        print(consulteditor2[0])
        cursor.execute('DELETE FROM editor_ideia WHERE ideia_id=(?)',(id,) )
        cursor.execute('INSERT INTO editor_ideia(id, ideia_id, editor_id) VALUES (null,?,?)',(id, consulteditor2[0],))
        connection.commit()
    #if "loja" not in request.form:
    #    print("Não contem loja1")
    connection.close()
    return render_template('adminhome.html')



@app.route("/deleteID", methods=['GET', 'POST'])
def apagarideia():
    connection = sqlite3.connect("/var/www/webApp/webApp/ideiasverdes.db")
    cursor = connection.cursor()
    ideia=request.form['deleteID']
    print(ideia)
    removerideiaderelacoes(ideia, "loja_ideia")
    removerideiaderelacoes(ideia, "editor_ideia")
    removerideiaderelacoes(ideia, "palavra_ideia")

    print("remover ideia")
    consultarem=cursor.execute('select * from ideias where id = (?)',(ideia,) )
    if consultarem is not None:
        cursor.execute('DELETE FROM ideias WHERE id=(?)',(ideia,) )
        connection.commit()
    
    connection.close()
    return render_template('adminhome.html')




if __name__ == "__main__":#default Flask
    app.run(debug=True, ssl_context=('cert.crt', 'cert.key'))



