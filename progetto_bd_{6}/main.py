import pymysql
import datetime
from tabulate import tabulate
db = pymysql.connect(db='hairdresser', user='root', passwd = '*********', host='localhost')
curs = db.cursor()


lista = (f'''istruzione comandi:\n digitare 1 per inserire una prenotazione\n digitare 2 per inserire un cliente\n digitare 3 per inserire un prodotto\n digitare 4 per inserire un personale\n digitare 5 per inserire un trattamento\n digitare 6 per visualizzare lo storico di un cliente \n digitare 7  per visualizzare quante colte ha prenotato un cliente \n digitare 8 per visualizzare le performance di uno o tutti i membri dello staff \n digitare 9 per ottenere il numero di trattamenti effetuati da uno o tutti i membri dello staff \n digitare 10 per visualizzare il fatturato giornaliero \n digitare 11 per visualizzare il fatturato prodotto in un periodo \n digitare 12 per ottenere in ordine in base al numero di volte che snono stati effettuati i trattamenti \n digitare 13 per visualizzare il fatturato derivante dai diversi trattamenti \n digitare 14 per visualizzare i giorni ordinati in base al numero di prenotazioni \n digitare 15 per visualizzare i clienti ordinati in base al numero di prenotazioni che hanno effettuato \n digitare 16 per visualizzare l'importo medio pagato da un cliente in un periodo \n digitare 17 per visualizzare quali sono i prodotti la cui giacenza e minore della giacenza minima \n digitare 18 per ottenere le quantita di prodotti utilizzati in un periodo \n digitare 19 per visualizzare la giacenza di prodotti in unita''')





#inserire una prenotazione e aggiornare appuntamento
def prenotazione():    
    datcale = input('inserisci la data in cui prendere prenotazione: ')
    calendario = ('select * from prenotazione_t where data_prenotazione = %s')
    curs.execute(calendario, datcale)
    dateprenotate = curs.fetchall()
    if dateprenotate == ():
        print('non ci sono prenotazioni in questo giorno')
    
    else:
        tpe = []
        for i in dateprenotate:
            tpe.append(list(i))
        print(tabulate(tpe, headers = ['id_prenotazione', 'data_prenotazione','ora_prenotazione','id_cliente']))

    
    y = input('inserisci ora: ')
    z = input('inserisci id_cliente: ')
    pren=("insert into prenotazione_t (data_prenotazione, ora_prenotazione, id_cliente) values (%s,%s,%s)")
    val_pren = (datcale,y,z)
    try:
        curs.execute(pren, val_pren)
    except:
        print('il cliente non è nel db')
        prenotazione()
    result1 = curs.fetchall()
    db.commit()
    id_pre = curs.lastrowid
    
    an = input('inserisci anagrafica che deve effettuare il cliente: ')
    app=("insert into appuntamento_t (id_prenotazione, id_anagrafica) values (%s,%s)")
    app_val = (id_pre,an)
    curs.execute(app,app_val)
    result2 = curs.fetchall()
    db.commit()

    ric_na = input('inserire una nuova anagrafica?: ')
    if ric_na == 'si':
        ann = input('inserisci anagrafica che deve effettuare il cliente: ')
        appn=("insert into appuntamento_t (id_prenotazione, id_anagrafica) values (%s,%s)")
        appn_val = (id_pre,ann)
        curs.execute(appn,appn_val)
        result_na = curs.fetchall()
        db.commit()        
        
    
#inserire un cliente
def cliente():
    n = input(str('inserire il nome: '))
    c = input(str('inserire il cognome: '))
    s = input(str('inserire il sesso(M per maschio, F per femmina): '))
    i = input(str('inserire indirizzo: '))
    e = input(str('inserire email: '))
    t = input(str('inserire num telefono: '))
    d = input(str('inserire data nascita: '))
    clie = ('insert into cliente_t (nome,cognome,sesso,indirizzo,email,numero_telefono,data_nascita) values (%s,%s,%s,%s,%s,%s,%s)')
    clie_val = (n,c,s,i,e,t,d)
    curs.execute(clie, clie_val)
    result3 = curs.fetchall()
    db.commit()

#inserire un prodotto
def prodotto():
    np = input(str('inserire il nome prodotto: '))
    gmp = input('inserire la gaicenza minima: ')
    dp = input(str('inserire la descrizione: '))
    gap = input('inserire giacenza iniziale: ')
    tcp = input('inserire tasso di conversione: ')
    ump = input(str('inserire unita di misura: '))
    prod = ('insert into prodotto_t (nome, giacenza_minima, descrizione, giacenza, tasso_conversione, unita_misura) values (%s, %s, %s, %s, %s, %s)')
    prod_val = (np,gmp,dp,gap,tcp,ump)
    curs.execute(prod, prod_val)
    result4 = curs.fetchall()
    db.commit()
    
#inserire un personale
def personale():
    npe = input(str('inserire il nome del membro: '))
    cpe = input(str('inserire il cognome del membro: '))
    numpe = input(str('inserire il num tel: '))
    datpe = input(('inserire data di nascita: '))
    pers = ("insert into personale_t (nome, cognome, numero_telefono, data_nascita) values (%s,%s,%s,%s)")
    pers_val = (npe,cpe,numpe,datpe)
    curs.execute(pers,pers_val)
    result5 = curs.fetchall()
    db.commit()

#inserire un trattamento un eventuale creazione della scheda, pagamento e feedback
def trattamento():
    datcale = input('inserisci la data nella quale la prenotazione viene effettuata: ')
    calendario = ('select * from prenotazione_t where data_prenotazione = %s')
    curs.execute(calendario, datcale)
    dateprenotate = curs.fetchall()
    if dateprenotate == ():
        print('in questo giorno non ci sono prenotazioni')
        return(trattamento())
    tpdg = []
    for i in dateprenotate:
        tpdg.append(list(i))
    print(tabulate(tpdg, headers = ['id_prenotazione', 'data_prenotazione','ora_prenotazione','id_cliente']))

    idp = input('inserire id della prenotazione da trasformare in trattamento: ')
    idcl = input('inserire id del cliente che deve effettuare il trattamento: ')
    anagrafica = ('select * from appuntamento_t where id_prenotazione = %s')
    anagrafica_val = (idp)
    curs.execute(anagrafica, anagrafica_val)
    appunt = curs.fetchall()
    id_anagrafiche = []
    for i in range(len(appunt)):
        id_anagrafiche.append((appunt[i][1]))
    

    l_sc = []
    for j in id_anagrafiche:    
        scheda = ('select id_prodotto, quantita from scheda_cliente_t where id_cliente = %s and id_anagrafica = %s')
        scheda_val = (idcl,j)
        curs.execute(scheda, scheda_val)
        result_sc = curs.fetchall()
        
        
        if result_sc == ():
            scheda_cliente(j, idcl)
            curs.execute(scheda, scheda_val)
            result_sc = curs.fetchall()
        print(result_sc)

        
##        for k in range(len(result_sc)):
##            prodotto_dauti = (result_sc[k][0])
##            quantita_dauti = (result_sc[k][1])
##            scarico(prodotto_dauti,quantita_dauti)


        
      
    
    
    orat = input('inserire ora trattamento: ')
    idpe = input('inserire id personale: ' )
    tratt = ("insert into trattamento_t (ora_inizio, id_prenotazione, id_personale) values (%s,%s,%s)")
    tratt_val = (orat,idp,idpe)
    curs.execute(tratt,tratt_val)
    result6 = curs.fetchall()
    db.commit()
    id_tra = curs.lastrowid

    
    
    
    print('inserire i dati per il pagamento')
    
    modp = input('inserire modalità: ')
    prezzo = 0
    for e in id_anagrafiche:
        importo = ('select prezzo from anagrafica_t where id_anagrafica = %s')
        curs.execute(importo,e)
        result_importo = curs.fetchall()
        prezzo = prezzo + result_importo[0][0]


    datp = datcale
    orap = input('inserire ora pagamento: ')
    pag = ("insert into pagamento_t (modalità_pagamento, importo,data_pagamento,ora_pagamento,id_trattamento) values (%s,%s,%s,%s,%s)")
    pag_val = (modp,prezzo,datp,orap,id_tra)
    curs.execute(pag,pag_val)
    result7 = curs.fetchall()
    db.commit()

    fe = input('inserire un feedback?: ')
    if fe == 'si':
        pt_fe = input('inserire il punteggio da 1 a 5: ')
        feedb = ('insert into feedback_t (punteggio, id_trattamento) values (%s, %s)')
        feedb_val = (pt_fe, id_tra)
        curs.execute(feedb, feedb_val)
        result_feed = curs.fetchall()
        db.commit()
        

#inserisce scheda cliente richiamata da trattamento
def scheda_cliente(j, idcl):
    print('inserisci la scheda del cliente')
    id_cl = idcl
    id_pr = input('inserire id prodotto: ')
    id_an = j
    qua = input('inserire quantità: ')
    sche = ("insert into scheda_cliente_t values (%s,%s,%s,%s)")
    sche_val = (id_cl, id_an, id_pr, qua)
    curs.execute(sche,sche_val)
    result_sche = curs.fetchall()
    db.commit()

##def scheda_cliente_mod():
##    id_cliente = input('inserire id cliente: ')
##    id_anagrafica = input('inserire id anagrafica: ')
##    mod_sc = ('uptade scheda_cliente_t set quantita = %s where id_cliente=%s and id_anagrafica = %s')
##    mod_sc_val = (id_cliente, id_anagrafica)
##    curs.execute(mod_sc, mod_sc_val)
##    result_mod = curs.fetchall()
##    db.commit()
    
##def scarico(prodotto_dauti, quantita_dauti):
##    mod_pro = ('update prodotto_t set giacenza = giacenza - %s where id_prodotto = %s')
##    mod_pro_val = (quantita_dauti, prodotto_dauti)
##    curs.execute(mod_pro, mod_pro_val)
##    db.commit()
    
#visualizza lo storico di un cliente
def storico5():
    print('Di quale cliente si vuole visualizzare lo storico?')
    x=input()
    sql_select_query = """SELECT nome, cognome, descrizione, Data_prenotazione
    FROM cliente_t, prenotazione_t, anagrafica_t, appuntamento_t
    WHERE (cliente_t.ID_CLIENTE=prenotazione_t.ID_CLIENTE 
    AND prenotazione_t.ID_PRENOTAZIONE=appuntamento_t.ID_PRENOTAZIONE
    AND appuntamento_t.ID_ANAGRAFICA=anagrafica_t.ID_ANAGRAFICA
    AND PRENOTAZIONE_T.ID_CLIENTE=%s)"""
    curs.execute(sql_select_query, x)
    record = curs.fetchall()
    t_st = []
    for i in record:
        t_st.append(list(i))
    print(tabulate(t_st, headers = ['nome','cognome','descrizione','data_prenotazione']))

#numero di prenotazioni di un cliente
def storico5_1():
    print('Di quale cliente si vuole visualizzare il numero di prenotazioni?')
    x=input()
    sql_select_query="""SELECT nome, cognome, COUNT(*) as totale_prenotazioni
    FROM cliente_t, prenotazione_t
    WHERE (cliente_t.ID_CLIENTE=prenotazione_t.ID_CLIENTE 
    AND PRENOTAZIONE_T.ID_CLIENTE=%s)"""
    curs.execute(sql_select_query, x)
    record = curs.fetchall()
    t_st5_1 = []
    for i in record:
        t_st5_1.append(list(i))
    print(tabulate(t_st5_1, headers = ['nome','cognome','num_prenotazioni']))

#visualizza il punteggio medio di uno o tutti i membri dello staff
def feedback():
    print('Visualizzare i feedback relativi a tutto il personale?(inserire si o no)')
    answer=input(str())
    if answer=='si':
        sql_select_query = """SELECT Nome, Cognome, AVG(punteggio) AS Media_punteggio 
        FROM personale_t, feedback_t, trattamento_t
        WHERE (feedback_t.ID_TRATTAMENTO=trattamento_t.ID_TRATTAMENTO
        AND trattamento_t.ID_PERSONALE=personale_t.ID_PERSONALE) 
        GROUP BY nome, cognome;"""
        curs.execute(sql_select_query)
        record = curs.fetchall()
        tfs = []
        for i in record:
            tfs.append(list(i))
        print(tabulate(tfs, headers = ['nome','cognome','media_pt']))
    else:
        print("inserire l'id del personale di cui si vuole visualizzare i feedback")
        x=input()
        sql_select_query="""SELECT Nome, Cognome, AVG(punteggio) AS Media_punteggio 
        FROM personale_t, feedback_t, trattamento_t
        WHERE feedback_t.ID_TRATTAMENTO=trattamento_t.ID_TRATTAMENTO
        AND trattamento_t.ID_PERSONALE=personale_t.ID_PERSONALE AND personale_t.id_personale=%s;"""
        curs.execute(sql_select_query,x)
        record = curs.fetchall()
        tfi = []
        for i in record:
            tfi.append(list(i))

            print(tabulate(tfi, headers = ['nome','cognome','media_pt']))

#controllare il numero di trattamenti effettauti da uno o tutti i membri dello staff
def numtratt():
    print('si vuole visualizzare i trattamenti eseguiti dal singolo a dall intero staff?')
    print('rispondi singolo o intero')
    answer=input(str())
    if answer=='singolo':
        print('qual è il periodo che si vuole visualizzare?')
        print('data inizio periodo')
        inizio=input(str())
        print('data fine periodo')
        fine=input(str())
        print('id personale da controllare')
        idz=input(str())
        my_data=[inizio, fine, idz]
        sql_select_query="""SELECT Nome, cognome, count(*) AS trattamenti_effettuati_totali
        FROM trattamento_t, personale_t, prenotazione_t
        WHERE personale_t.ID_PERSONALE=trattamento_t.ID_PERSONALE 
        AND trattamento_t.id_prenotazione=prenotazione_t.id_prenotazione
        AND data_prenotazione BETWEEN %s AND %s
        AND personale_t.id_personale=%s
        GROUP BY Nome, Cognome;"""
        curs.execute(sql_select_query,my_data)
        record = curs.fetchall()
        tnts = []
        for i in record:
            tnts.append(list(i))
        print(tabulate(tnts, headers = ['nome','cognome','num_tratt']))

    if answer=='intero':
        print('qual è il periodo che si vuole visualizzare?')
        print('data inizio periodo')
        inizio=input(str())
        print('data fine periodo')
        fine=input(str())
        my_data=[inizio, fine]
        sql_select_query="""SELECT Nome, cognome, count(*) AS trattamenti_effettuati_totali
        FROM trattamento_t, personale_t, prenotazione_t
        WHERE personale_t.ID_PERSONALE=trattamento_t.ID_PERSONALE 
        AND trattamento_t.id_prenotazione=prenotazione_t.id_prenotazione
        AND data_prenotazione BETWEEN %s AND %s
        GROUP BY Nome, Cognome;"""
        curs.execute(sql_select_query,my_data)
        tnti = []
        record = curs.fetchall()
        for i in record:
            tnti.append(list(i))
        print(tabulate(tnti, headers = ['nome','cognome','num_tratt']))
        
#fatturato giornaliero
def fatturato():
    print('qual è il giorno che si vuole visualizzare?')
    print('inserisci giorno:')
    inizio=input(str())
    my_data=(inizio)
    sql_select_query="""SELECT data_prenotazione as 'DATA', sum(importo) AS fatturato_giornaliero 
    FROM pagamento_t, prenotazione_t, trattamento_t
    WHERE pagamento_t.id_trattamento=trattamento_t.id_trattamento
    AND trattamento_t.id_prenotazione=prenotazione_t.id_prenotazione
    AND data_prenotazione=%s; """
    curs.execute(sql_select_query,my_data)
    record = curs.fetchall()
    tf = []
    for i in record:
        tf.append(list(i))
    print(tabulate(tf, headers = ['data','fatturato']))

#fatturato in un periodo
def fatt_periodo():
    print('qual è il periodo che si vuole visualizzare?')
    print('data inizio periodo')
    inizio=input(str())
    print('data fine periodo')
    fine=input(str())
    my_data=(fine, inizio, inizio, fine)
    sql_select_query="""SELECT sum(importo) , datediff(%s,%s) AS arcotemporale
    FROM pagamento_t, prenotazione_t, trattamento_t
    WHERE  (pagamento_t.ID_TRATTAMENTO=trattamento_t.ID_TRATTAMENTO 
    AND trattamento_t.ID_PRENOTAZIONE=prenotazione_t.ID_PRENOTAZIONE 
    AND Data_prenotazione BETWEEN %s AND %s) ;"""
    curs.execute(sql_select_query,my_data)
    record = curs.fetchall()
    tfp = []
    for i in record:
        tfp.append(list(i))
    print(tabulate(tfp, headers = ['importo','arco_temp_giorni']))
    
#trattamenti ordinati in base al numero di volte che sono stati effettuati
def num_max_tratt():
    qnumm = ('''SELECT descrizione, count(*) AS numtratt
            FROM anagrafica_t, prenotazione_t, appuntamento_t
            WHERE   prenotazione_t.ID_PRENOTAZIONE=appuntamento_t.ID_PRENOTAZIONE
            AND appuntamento_t.ID_ANAGRAFICA=anagrafica_t.ID_ANAGRAFICA
            GROUP BY anagrafica_t.id_anagrafica;''')
    curs.execute(qnumm)
    rnum_max = curs.fetchall()
    trnm = []
    for i in rnum_max:
        trnm.append(list(i))
    trnm_m = max(trnm)
    print(trnm)
    print(tabulate(trnm, headers = ['trattamento','num_tratt']))
    
#fatturato condizionato a tutti i tipi di trattamento
def fattu_condiz():
    print('questo è il totale derivato da ogni trattamento')
    sql_select_query="""SELECT descrizione, sum(prezzo) AS guadagno_da_trattamento
    FROM anagrafica_t, pagamento_t, trattamento_t, prenotazione_t, appuntamento_t
    WHERE (anagrafica_t.id_anagrafica= appuntamento_t.id_anagrafica
    AND appuntamento_t.id_prenotazione=prenotazione_t.id_prenotazione
    AND prenotazione_t.ID_PRENOTAZIONE=trattamento_t.ID_PRENOTAZIONE
    AND trattamento_t.ID_TRATTAMENTO= pagamento_t.ID_TRATTAMENTO)
    GROUP BY descrizione; """
    curs.execute(sql_select_query)
    record = curs.fetchall()
    tfc = []
    for i in record:
        tfc.append(list(i))
    print(tabulate(tfc, headers = ['trattamento','fatturato']))

#giorni ordinati in base al numero di prenotazioni
def per_max_pren():
    q_pmp = ('''SELECT data_prenotazione, count(*) AS conteggio
            FROM prenotazione_t
            GROUP BY data_prenotazione
            ORDER BY conteggio desc''')
    curs.execute(q_pmp)
    cf_pmp = curs.fetchall()
    tpmp = []
    for i in cf_pmp:
        tpmp.append(list(i))
    print(tabulate(tpmp, headers = ['data','num_prenotazioni']))

#visualizzare i clienti in ordine del numero di volte che ha prenotato
def max_fre_cl():
    q_mfc = ('''SELECT Nome, Cognome , count(*) AS frequenza
            FROM cliente_t, prenotazione_t
            WHERE prenotazione_t.id_cliente=cliente_t.ID_CLIENTE 
            GROUP BY prenotazione_t.id_cliente
            ORDER BY frequenza desc''')
    curs.execute(q_mfc)
    res_q = curs.fetchall()
    t_res_q = []
    for i in res_q:
        t_res_q.append(list(i))
    print(tabulate(t_res_q, headers=['nome','cognome', 'num_pren']))
    
#calcolare l'importo medio derivato da un cliente in un periodo
def importo_medio():
    print('qual è il periodo che si vuole visualizzare?')
    print('data inizio periodo')
    inizio=input(str())
    print('data fine periodo')
    fine=input(str())
    print('id cliente')
    idz=input(str())
    my_data=( idz,inizio, fine)
    sql_select_query="""SELECT Nome, Cognome, AVG(importo) AS importo_medio
    FROM prenotazione_t, cliente_t, pagamento_t, trattamento_t
    WHERE prenotazione_t.id_prenotazione=trattamento_t.id_prenotazione
    AND trattamento_t.id_trattamento=pagamento_t.id_trattamento
    AND prenotazione_t.id_cliente=cliente_t.id_cliente
    AND `prenotazione_t`.`id_cliente`=%s AND data_prenotazione BETWEEN %s AND %s
    GROUP BY prenotazione_t.id_cliente;
    """
    curs.execute(sql_select_query,my_data)
    record = curs.fetchall()
    tim = []
    for i in record:
        tim.append(list(i))
    print(tabulate(tim, headers=['nome','cognome','importo_medio']))

#prodotti la cui giacenza è minore della giacenza minima
def giacenza_prod_min():
    sql_select_query="""
    SELECT prodotto_t.nome, prodotto_t.giacenza giacenza_iniziale, prodotto_t.tasso_conversione, prodotto_t.giacenza_minima,
    sum(scheda_cliente_t.quantita) AS quantita_usata, 
    prodotto_t.giacenza - sum(scheda_cliente_t.quantita) AS giacenza,
    ceiling((prodotto_t.giacenza - sum(scheda_cliente_t.quantita))/prodotto_t.tasso_conversione) AS  giacenza_unita
    FROM  trattamento_t , prenotazione_t , scheda_cliente_t , prodotto_t 
    WHERE trattamento_t.id_prenotazione = prenotazione_t.id_prenotazione 
    and prenotazione_t.id_cliente = scheda_cliente_t.id_cliente 
    and prodotto_t.id_prodotto = scheda_cliente_t.id_prodotto 
    group by prodotto_t.nome, prodotto_t.giacenza, prodotto_t.tasso_conversione
    HAVING (prodotto_t.giacenza - sum(scheda_cliente_t.quantita)<prodotto_t.giacenza_minima);"""
    curs.execute(sql_select_query)
    record = curs.fetchall()
    tgpm = []
    for i in record:
        tgpm.append(list(i))
    print(tabulate(tgpm, headers = ['nome','giacenza_iniziale','tasso_di_conv', 'giacenza_minima', 'qauntita_usata', 'giacenza', 'giacenza_in_unita']))

#quantita di prodotti che sono stati utilizzati in un periodo
def util_prod():    
    print('qual è il periodo che si vuole visualizzare?')
    print('data inizio periodo')
    inizio=input(str())
    print('data fine periodo')
    fine=input(str())
    my_data=(inizio, fine)
    sql_select_query="""SELECT prodotto_t.nome, 
    sum(scheda_cliente_t.quantita) AS quantita_usata, 
    prodotto_t .giacenza - sum(scheda_cliente_t.quantita) AS giacenza,
    ceiling((prodotto_t .giacenza - sum(scheda_cliente_t.quantita))/prodotto_t.tasso_conversione) AS  giacenza_unita
    FROM  trattamento_t , prenotazione_t , scheda_cliente_t , prodotto_t 
    WHERE trattamento_t.id_prenotazione = prenotazione_t.id_prenotazione 
    and prenotazione_t.id_cliente = scheda_cliente_t.id_cliente 
    and prodotto_t.id_prodotto = scheda_cliente_t.id_prodotto 
    and data_prenotazione BETWEEN %s AND %s
    group by prodotto_t.nome, prodotto_t.giacenza, prodotto_t.tasso_conversione;
    """
    curs.execute(sql_select_query,my_data)
    record = curs.fetchall()
    tdt = []
    for i in record:
        tdt.append(list(i))
    print(tabulate(tdt,headers = ['nome','quantità_usata', 'giacenza_attuale', 'giacenza_in_unità']))

#unita di prodotti presenti in magazzino
def quant_pro():       
    print('quantità in unità dal magazzino')
    sql_select_query="""SELECT prodotto_t.nome,  prodotto_t.tasso_conversione, prodotto_t.giacenza_minima,
    ceiling((prodotto_t .giacenza - sum(scheda_cliente_t.quantita))/prodotto_t.tasso_conversione) AS  giacenza_unita
    FROM  trattamento_t , prenotazione_t , scheda_cliente_t , prodotto_t 
    WHERE trattamento_t.id_prenotazione = prenotazione_t.id_prenotazione 
    and prenotazione_t.id_cliente = scheda_cliente_t.id_cliente 
    and prodotto_t.id_prodotto = scheda_cliente_t.id_prodotto 
    group by prodotto_t.nome, prodotto_t.giacenza, prodotto_t.tasso_conversione"""
    curs.execute(sql_select_query)
    record = curs.fetchall()
    quant_p_t = []
    for i in record:
        quant_p_t.append(list(i))
    print(tabulate(quant_p_t, headers = ['nome_prodotto', 'tasso_di_conversione', 'giacenza_minima_lt', 'giacenza_in_unità']))

def azione():
    act = 'si'
    while act == 'si':
        print(lista)
        ins = input("digitare un numero per effettuare un'azione: ")

        if ins == '1':
            prenotazione()

        if ins == '2':
            cliente()

        if ins == '3':
            prodotto()

        if ins == '4':
            personale()

        if ins == '5':
            trattamento()

        if ins == '6':
            storico5()

        if ins == '7':
            storico5_1()

        if ins == '8':
            feedback()

        if ins == '9':
            numtratt()

        if ins == '10':
            fatturato()

        if ins == '11':
            fatt_periodo()

        if ins == '12':
            num_max_tratt()
            
        if ins == '13':
            fattu_condiz()

        if ins == '14':
            per_max_pren()

        if ins == '15':
            max_fre_cl()
            
        if ins == '16':
            importo_medio()

        if ins == '17':
            giacenza_prod_min()

        if ins == '18':
            util_prod()

        if ins == '19':
            quant_pro()
        act = input('digitare si per effettuare un altra azione: ')
azione()
    
