from flask import Flask, render_template, request
from flask_mysqldb import MySQL
app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '***************'
app.config['MYSQL_DB'] = 'hairdresser'
mysql=MySQL(app)

#homepage
@app.route("/")
def main():
    return render_template('index.html', title = 'Gruppo 6: Gestione attività')

#inserisci nuova prenotazione
@app.route("/InsPrenotazione", methods=['GET','POST'])
def Query1():
    if request.method == 'POST':
        use = request.form
        data_prenotazione = use['data_prenotazione']
        ora_prenotazione = use['ora_prenotazione']
        id_cliente = use['id_cliente']
        id_anagrafica = use['id_anagrafica']
        cur = mysql.connection.cursor()
        cur.execute("insert into prenotazione_t(data_prenotazione,ora_prenotazione,id_cliente) VALUES (%s,%s,%s)", (data_prenotazione,ora_prenotazione,id_cliente))
        mysql.connection.commit()
        id_pre = cur.lastrowid
        cur.execute("insert into appuntamento_t (id_prenotazione, id_anagrafica) values (%s,%s)", (id_pre, id_anagrafica))
        mysql.connection.commit()
        cur.close()
        return 'Prenotazione inserita con successo'
    return render_template("Query4.html", title ="Inserire Prenotazione")
                    
#inserisci nuovo dipendente
@app.route("/InsDipendente", methods=['GET','POST'])
def Query2():
    if request.method == 'POST':
        user = request.form
        nome = user['nome']
        cognome = user['cognome']
        numero_telefono = user['numero_telefono']
        data_nascita = user['data_nascita']
        cur = mysql.connection.cursor()
        cur.execute("insert into personale_t(nome,cognome,numero_telefono,data_nascita) VALUES (%s,%s,%s,%s)", (nome,cognome,numero_telefono,data_nascita))
        mysql.connection.commit()
        cur.close()
        return """<h1>Dipendente inserito con successo!</h1>
                <a href="http://localhost:5000/">Home<a/>
                """
    return render_template("Query2.html", title="Inserire Dipendente")

#inserisci nuovo prodotto
@app.route("/InsProdotto", methods=['GET','POST'])
def Query3():
    if request.method == 'POST':
        userDetails = request.form
        nome = userDetails['nome']
        giacenza_minima = userDetails['giacenza_minima']
        descrizione = userDetails['descrizione']
        giacenza = userDetails['giacenza']
        tasso_conversione = userDetails['tasso_conversione']
        unita_misura = userDetails['unita_misura']
        cur = mysql.connection.cursor()
        cur.execute("insert into prodotto_t(nome,giacenza_minima,descrizione,giacenza,tasso_conversione,unita_misura) VALUES(%s,%s,%s,%s,%s,%s)",(nome,giacenza_minima,descrizione,giacenza,tasso_conversione,unita_misura))
        mysql.connection.commit()
        cur.close()
        return """<h1>Prodotto inserito con successo!</h1>
                <a href="http://localhost:5000/">Home<a/>
                """
    return render_template('Query3.html', title="Inserire Prodotto")

#visualizza i dati di una prenotazione scelto l'id
@app.route("/VisPrenotazioni1")
def prenotazioni():
    return """
<h1>Cerca una prenotazione per id da 1 a 200</h1>
<form method="get" action="/VisPrenotazioni1/search">
    <input type="number" name="id_prenotazione" value="">
    <input type="submit" value="Invia">
</form>
<br>
<a href="http://localhost:5000/">Home<a/>

"""

@app.route('/VisPrenotazioni1/search', methods=['GET'])
def searchPrenotazioni():
    args = request.args
    id_prenotazione = args.get('id_prenotazione')
    return prenotazioneQuery(id_prenotazione)

@app.route('/VisPrenotazione1/<id_prenotazione>')
def getid_prenotazione(id_prenotazione):
    return prenotazioneQuery(id_prenotazione)
            
def prenotazioneQuery(id_prenotazione):
    cursor = mysql.connection.cursor()
        
    sql_select_query = """
        SELECT data_prenotazione,ora_prenotazione,id_cliente
        FROM prenotazione_t
        WHERE id_prenotazione = %s
    """
    cursor.execute(sql_select_query, [id_prenotazione])
    record = cursor.fetchall()
    return render_template('prenotazioni.html', record=record)

#visualizzare il flusso di cassa
@app.route("/VisCassa")
def cassa():
    return render_template('cassa.html')
@app.route("/VisCassa/search", methods=["GET"])
def searchcassa():
    args = request.args
    data = args.get('data')
    return cassaQuery(data)
@app.route('/VisCassa/<data>')
def getdata(data):
    return cassaQuery(data)
def cassaQuery(data):
    cur = mysql.connection.cursor()
    sql_select_query = """
        SELECT data_prenotazione as 'DATA', sum(importo) AS fatturato_giornaliero
        FROM pagamento_t, prenotazione_t, trattamento_t
        WHERE pagamento_t.id_trattamento=trattamento_t.id_trattamento
        AND trattamento_t.id_prenotazione=prenotazione_t.id_prenotazione
        AND data_prenotazione=%s;

"""
    cur.execute(sql_select_query, [data])
    record = cur.fetchall()
    return render_template('cassa1.html', record = record)

#visualizzare storico cliente
@app.route("/VisCliente")
def cliente():
    return render_template('cliente.html')
@app.route("/VisCliente/search", methods=['GET'])
def searchcliente():
    args = request.args
    id_cliente = args.get('id_cliente')
    return clientequery(id_cliente)
@app.route('/VisCliente/<id_cliente>')
def getcliente(id_cliente):
    return clientequery(id_cliente)
def clientequery(id_cliente):
    cur = mysql.connection.cursor()
    sql_select_query="""
        SELECT nome, cognome, descrizione, data_prenotazione, ora_prenotazione
        FROM cliente_t, prenotazione_t, anagrafica_t, appuntamento_t
        WHERE (cliente_t.ID_CLIENTE=prenotazione_t.ID_CLIENTE
        AND prenotazione_t.ID_PRENOTAZIONE=appuntamento_t.ID_PRENOTAZIONE
        AND appuntamento_t.ID_ANAGRAFICA=anagrafica_t.ID_ANAGRAFICA
        AND PRENOTAZIONE_T.ID_CLIENTE=%s);
"""
    cur.execute(sql_select_query, [id_cliente])
    record = cur.fetchall()
    return render_template ('cliente1.html', record = record)

#visualizzare i feedback di 1 personale
@app.route('/VisFeed')
def feed():
    return render_template ('feed.html')
@app.route('/VisFeed/search')
def searchfeed():
    args=request.args
    id_personale = args.get('id_personale')
    return feedbackquery(id_personale)
app.route('/VisFeed/<id_personale>')
def getfeed():
    return feedbackquery(id_personale)
def feedbackquery(id_personale):
    cur = mysql.connection.cursor()
    sql_select_query ="""
        SELECT Nome, Cognome, AVG(punteggio) AS Media_punteggio 
        FROM personale_t, feedback_t, trattamento_t
        WHERE (feedback_t.ID_TRATTAMENTO=trattamento_t.ID_TRATTAMENTO
        AND trattamento_t.ID_PERSONALE=personale_t.ID_PERSONALE AND personale_t.id_personale=%s);
"""
    cur.execute(sql_select_query, [id_personale])
    record = cur.fetchall()
    return render_template ('feed1.html', record = record)
@app.route('/VisFeedTot')
def feedTot():
    cursore = mysql.connection.cursor()
    sql_select_query = """SELECT Nome, Cognome, AVG(punteggio) AS Media_punteggio 
        FROM personale_t, feedback_t, trattamento_t
        WHERE (feedback_t.ID_TRATTAMENTO=trattamento_t.ID_TRATTAMENTO
        AND trattamento_t.ID_PERSONALE=personale_t.ID_PERSONALE) 
        GROUP BY nome, cognome;"""
    cursore.execute(sql_select_query)
    record = cursore.fetchall()
    return render_template ('feed1.html', record = record)

#trattamenti effettuati da un membro del personale con 2 date
@app.route('/VisTratt')
def vistratt():
    return render_template('trattamenti.html')
@app.route('/VisTratt/search')
def searchratt():
    args = request.args
    id_personale = args.get('id_personale')
    data1 = args.get('data1')
    data2 = args.get('data2')
    lista = [data1,data2,id_personale]
    return trattquery(lista)
@app.route('/VisTratt/lista')

def trattquery(lista):
    
    cur = mysql.connection.cursor()
    sql_select_query = """
        SELECT Nome, cognome, count(*) AS trattamenti_effettuati_totali
        FROM trattamento_t, personale_t, prenotazione_t
        WHERE personale_t.ID_PERSONALE=trattamento_t.ID_PERSONALE 
        AND trattamento_t.id_prenotazione=prenotazione_t.id_prenotazione
        AND data_prenotazione BETWEEN %s AND %s
        AND personale_t.id_personale=%s
        GROUP BY Nome, Cognome;
        """
    cur.execute(sql_select_query, lista)
    record = cur.fetchall()
    return render_template('trattamento1.html', record=record)

#fatturato in un determinato lasso di tempo 
@app.route('/VisFatturato')
def visfatturato():
    return render_template('fatturato.html')
@app.route('/VisFatturato/search')
def searchfatturato():
    args = request.args
    data1 = args.get('data1')
    data2 = args.get('data2')
    lista = [data1,data2]
    return fatturatoquery(lista)
@app.route('/VisFatturato/lista')

def fatturatoquery(lista):
    cur = mysql.connection.cursor()
    sql_select_query = """
        SELECT sum(importo)
        FROM pagamento_t, prenotazione_t, trattamento_t
        WHERE  (pagamento_t.ID_TRATTAMENTO=trattamento_t.ID_TRATTAMENTO 
        AND trattamento_t.ID_PRENOTAZIONE=prenotazione_t.ID_PRENOTAZIONE 
        AND Data_prenotazione BETWEEN %s AND %s) ;

"""
    cur.execute(sql_select_query, lista)
    record = cur.fetchall()
    return render_template('fatturato1.html', record = record)

#visualizzare fatturato di 1 anagrafica scelta
@app.route('/VisFattTratt')
def fatttratt():
    return render_template('fatturato2.html')
@app.route('/VisFattTratt/search')
def fatttrattsearch():
    args = request.args
    id_anagrafica = args.get('id_anagrafica')
    return fatttrattquery(id_anagrafica)
app.route('/VisFattTratt/<id_anagrafica>')
def getfeed():
    return fatttrattquery(id_anagrafica)

def fatttrattquery(id_anagrafica):
    cur = mysql.connection.cursor()
    sql_select_query="""
        SELECT descrizione, sum(prezzo) AS guadagno_da_trattamento
        FROM anagrafica_t, pagamento_t, trattamento_t, prenotazione_t, appuntamento_t
        WHERE (anagrafica_t.id_anagrafica= appuntamento_t.id_anagrafica
        AND appuntamento_t.id_prenotazione=prenotazione_t.id_prenotazione
        AND prenotazione_t.ID_PRENOTAZIONE=trattamento_t.ID_PRENOTAZIONE
        AND trattamento_t.ID_TRATTAMENTO= pagamento_t.ID_TRATTAMENTO)
        and anagrafica_t.id_anagrafica = %s
"""
    cur.execute(sql_select_query, [id_anagrafica])
    record = cur.fetchall()
    return render_template('fatturato3.html', record = record)


if __name__=='__main__':
    app.run(debug=True)
