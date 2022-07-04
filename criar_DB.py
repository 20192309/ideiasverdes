from os import curdir
import sqlite3

connection = sqlite3.connect("backend/ideiasverdes.db")
cursor = connection.cursor()


cursor.execute("create table ideias (id INTEGER PRIMARY KEY AUTOINCREMENT, nome_ideia text NOT NULL, impacto_ind integer, impacto_col integer, esforco integer, fact_cient text, descricao text, curiosidade text, mais_info text, videos text, estudos text, imagem text, data_cria datetime NOT NULL, data_revi datetime)")
'''cursor.execute("create table ideias(
    id PK auto, name text NOT NULL, 
    impacto_ind integer, impacto_col integer, esforco integer, 
    fact_cient text, descricao text, curiosidade text, 
    mais_info text, videos text, estudos text, 
    imagem text, data_cria datetime NOT NULL, data_revi datetime)")'''
cursor.execute("create table editores (id INTEGER PRIMARY KEY AUTOINCREMENT, editor_nome text NOT NULL, teamplace text not null)")
'''id PK auto, editor_nome text NOT NULL, teamplace text not null'''
cursor.execute("create table lojas (id INTEGER PRIMARY KEY AUTOINCREMENT, loja_nome text NOT NULL, url text)")
'''id PK auto, loja_nome text NOT NULL, url text'''
cursor.execute("create table palavras (id INTEGER PRIMARY KEY AUTOINCREMENT, palavra text NOT NULL, familia text)")
'''id PK auto, palavra text NOT NULL, familia text'''
cursor.execute("create table editor_ideia (id INTEGER PRIMARY KEY AUTOINCREMENT, ideia_id integer, editor_id integer)")
cursor.execute("create table loja_ideia (id INTEGER PRIMARY KEY AUTOINCREMENT, loja_id integer, ideia_id integer)")
cursor.execute("create table palavra_ideia (id INTEGER PRIMARY KEY AUTOINCREMENT, ideia_id integer, palavra_id integer)")

editor = [('Ramiro Carlos','founder')]

cursor.executemany('INSERT INTO editores(id, editor_nome, teamplace) VALUES (null,?,?)', editor)
connection.commit()

for row in cursor.execute("select * from editores"):
    print(row)



connection.close()
