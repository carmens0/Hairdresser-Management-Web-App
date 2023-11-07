USE HAIRDRESSER;

#QUERY 1: Inserire una prenotazione
INSERT INTO prenotazione_t(ID_PRENOTAZIONE, Data_prenotazione, Ora_prenotazione, ID_CLIENTE) 
VALUES ('2022-04-21', '08:30', 4);
INSERT INTO appuntamento_t (appuntamento_t.id_prenotazione, id_anagrafica) 
VALUES ((SELECT DISTINCT last_insert_id() from prenotazione_t), 3);
#QUERY 2: Inserire un cliente nella tabella
INSERT INTO `hairdresser`.`cliente_t` (`nome`, `cognome`, `sesso`, `indirizzo`, `email`, `numero_telefono`, `data_nascita`) 
VALUES ('101', 'Jhonny', 'Depp', 'M', '252 California', 'j.depp@gmail.com', '5263875489', '1968-05-23');

#QUERY 3: Inserire un prodotto nella tabella prodotti
INSERT INTO `hairdresser`.`prodotto_t` ( `Nome`, `Giacenza_minima`, `Descrizione`, `Giacenza`, `Tasso_di_conversione`, 
`Unità_di_misura`) VALUES ('15', 'schiuma', '2.00', 'cura capelli', '5', '1', 'lt');

#QUERY 4: Inserire un membro del personale
INSERT INTO `hairdresser`.`personale_t` ( `Nome`, `Cognome`, `Numero_di_Telefono`, `Data_di_nascita`)
 VALUES ('4', 'Anthony', 'Bridgerton', '2563696586', '1989-06-02', '37');

#QUERY 5: Inserire un trattamento 
insert into trattamento_t (ora_inizio, id_prenotazione, id_personale) values ('10:00:00','10', '3');
insert into pagamento_t (modalità_pagamento, importo, data_pagamento, ora_pagamento, id_trattamento) 
values ('carta di credito', '40', '2022-04-10', '11:00:00', '110');
INSERT INTO feedback_t (`id_feedback`, `punteggio`, `id_trattamento`) VALUES ('201', '2', '301');



#QUERY 6: Visualizzare lo storico di un cliente (ID=30)
SELECT nome, cognome, descrizione, Data_prenotazione
FROM cliente_t, prenotazione_t, anagrafica_t, appuntamento_t
WHERE (cliente_t.ID_CLIENTE=prenotazione_t.ID_CLIENTE 
AND prenotazione_t.ID_PRENOTAZIONE=appuntamento_t.ID_PRENOTAZIONE
AND appuntamento_t.ID_ANAGRAFICA=anagrafica_t.ID_ANAGRAFICA
AND PRENOTAZIONE_T.ID_CLIENTE=30);

#QUERY7: Visualizzare solo quante volte ha prenotato un cliente 
SELECT nome, cognome, COUNT(*) as totale_prenotazioni
FROM cliente_t, prenotazione_t
WHERE (cliente_t.ID_CLIENTE=prenotazione_t.ID_CLIENTE 
AND PRENOTAZIONE_T.ID_CLIENTE=30);



#QUERY 8: Visualizzare le performance del personale tramite i feedback lasciati dai clienti
#PERFORMANCE DI TUTTO IL PERSONALE
SELECT Nome, Cognome, AVG(punteggio) AS Media_punteggio 
FROM personale_t, feedback_t, trattamento_t
WHERE (feedback_t.ID_TRATTAMENTO=trattamento_t.ID_TRATTAMENTO
AND trattamento_t.ID_PERSONALE=personale_t.ID_PERSONALE) 
GROUP BY nome, cognome;
#PERFORMANCE DI UN SOLO MEMBRO DEL PERSONALE
SELECT Nome, Cognome, AVG(punteggio) AS Media_punteggio 
FROM personale_t, feedback_t, trattamento_t
WHERE feedback_t.ID_TRATTAMENTO=trattamento_t.ID_TRATTAMENTO
AND trattamento_t.ID_PERSONALE=personale_t.ID_PERSONALE AND personale_t.id_personale=1;




#QUERY 9: Controllare il numero di trattamenti eseguiti da un membro del personale (o intero staff) in un determinato periodo 

#intero staff
SELECT Nome, cognome, count(*) AS trattamenti_effettuati_totali
FROM trattamento_t, personale_t, prenotazione_t
WHERE personale_t.ID_PERSONALE=trattamento_t.ID_PERSONALE 
AND trattamento_t.id_prenotazione=prenotazione_t.id_prenotazione
AND data_prenotazione BETWEEN '2022-04-21' AND '2022-05-01'
GROUP BY Nome, Cognome;
#un solo membro del personale
SELECT Nome, cognome, count(*) AS trattamenti_effettuati_totali
FROM trattamento_t, personale_t, prenotazione_t
WHERE personale_t.ID_PERSONALE=trattamento_t.ID_PERSONALE 
AND trattamento_t.id_prenotazione=prenotazione_t.id_prenotazione
AND data_prenotazione BETWEEN '2022-04-21' AND '2022-05-01'
AND personale_t.id_personale=2
GROUP BY Nome, Cognome;

#QUERY 10: Determinare il fatturato Giornaliero 
SELECT data_prenotazione as 'DATA', sum(importo) AS fatturato_giornaliero 
FROM pagamento_t, prenotazione_t, trattamento_t
WHERE pagamento_t.id_trattamento=trattamento_t.id_trattamento
AND trattamento_t.id_prenotazione=prenotazione_t.id_prenotazione
AND data_prenotazione='2022-04-24'; 




#QUERY 11: Calcolare il guadagno in un determinato lasso di tempo
SELECT sum(importo) AS importo, datediff('2022-05-01','2022-04-27') AS arcotemporale
FROM pagamento_t, prenotazione_t, trattamento_t
WHERE  (pagamento_t.ID_TRATTAMENTO=trattamento_t.ID_TRATTAMENTO 
AND trattamento_t.ID_PRENOTAZIONE=prenotazione_t.ID_PRENOTAZIONE 
AND Data_prenotazione BETWEEN '2022-04-27'AND '2022-05-01') ;

#QUERY 12: Verificare qual è il trattamento più effettuato o in ordine quelli più effettuati

CREATE VIEW Tratt AS
SELECT descrizione, count(*) AS numerotrattamenti
FROM anagrafica_t, prenotazione_t, appuntamento_t
WHERE  ( prenotazione_t.ID_PRENOTAZIONE=appuntamento_t.ID_PRENOTAZIONE
AND appuntamento_t.ID_ANAGRAFICA=anagrafica_t.ID_ANAGRAFICA)
GROUP BY descrizione;

SELECT * FROM Tratt WHERE numerotrattamenti=(select max(numerotrattamenti) FROM Tratt);



#QUERY 13: Calcolare il guadagno derivato da ogni tipo di trattamento 
SELECT descrizione, sum(prezzo) AS guadagno_da_trattamento
FROM anagrafica_t, pagamento_t, trattamento_t, prenotazione_t, appuntamento_t
WHERE (anagrafica_t.id_anagrafica= appuntamento_t.id_anagrafica
AND appuntamento_t.id_prenotazione=prenotazione_t.id_prenotazione
AND prenotazione_t.ID_PRENOTAZIONE=trattamento_t.ID_PRENOTAZIONE
AND trattamento_t.ID_TRATTAMENTO= pagamento_t.ID_TRATTAMENTO)
GROUP BY descrizione; 



#QUERY 14: Verificare quali sono i periodi con maggiori prenotazioni 

CREATE VIEW PrenotazGiornaliere AS
SELECT data_prenotazione, count(*) AS conteggio
FROM prenotazione_t
GROUP BY data_prenotazione; 

CREATE VIEW r2 AS
SELECT  AVG(conteggio) cont FROM prenotazgiornaliere;

SELECT data_prenotazione, conteggio, round(cont) media
FROM PrenotazGiornaliere ,r2
WHERE conteggio > cont;

#giorni ordinati in base alle prenotazioni 
SELECT data_prenotazione, count(*) AS conteggio
FROM prenotazione_t
GROUP BY data_prenotazione
ORDER BY conteggio desc;


#QUERY 15: Controllare i clienti che prenotano con maggiore frequenza
CREATE VIEW ClientiFrequenza AS
SELECT Nome, Cognome , count(*) AS frequenza
FROM cliente_t, prenotazione_t
WHERE prenotazione_t.id_cliente=cliente_t.ID_CLIENTE 
GROUP BY prenotazione_t.id_cliente; 

SELECT * FROM ClientiFrequenza 
WHERE frequenza=(SELECT max(frequenza) FROM ClientiFrequenza); 




#QUERY 16:Calcolare l’importo medio pagato dal cliente in una determinata fascia temporale
SELECT Nome, Cognome, AVG(importo) AS importo_medio
FROM prenotazione_t, cliente_t, pagamento_t, trattamento_t
WHERE prenotazione_t.id_prenotazione=trattamento_t.id_prenotazione
AND trattamento_t.id_trattamento=pagamento_t.id_trattamento
AND prenotazione_t.id_cliente=cliente_t.id_cliente
AND `prenotazione_t`.`id_cliente`=49 AND data_pagamento BETWEEN '2022-04-21' AND '2022-05-10'
GROUP BY prenotazione_t.id_cliente;



#QUERY 17: Verificare quali sono i prodotti la cui giacenza è minore della giacenza minima 

SELECT prodotto_t.nome, prodotto_t.giacenza giacenza_iniziale, prodotto_t.tasso_conversione, prodotto_t.giacenza_minima,
sum(scheda_cliente_t.quantita) AS quantita_usata, 
prodotto_t.giacenza - sum(scheda_cliente_t.quantita) AS giacenza,
ceiling((prodotto_t.giacenza - sum(scheda_cliente_t.quantita))/prodotto_t.tasso_conversione) AS  giacenza_unita
FROM  trattamento_t , prenotazione_t , scheda_cliente_t , prodotto_t 
WHERE trattamento_t.id_prenotazione = prenotazione_t.id_prenotazione 
and prenotazione_t.id_cliente = scheda_cliente_t.id_cliente 
and prodotto_t.id_prodotto = scheda_cliente_t.id_prodotto 
group by prodotto_t.nome, prodotto_t.giacenza, prodotto_t.tasso_conversione
HAVING (prodotto_t.giacenza - sum(scheda_cliente_t.quantita)<prodotto_t.giacenza_minima);


#QUERY 18: Verificare quanti prodotti sono stati utilizzati dato un tempo
SELECT prodotto_t.nome, prodotto_t.giacenza AS giacenza_iniziale,
sum(scheda_cliente_t.quantita) AS quantita_usata, 
prodotto_t .giacenza - sum(scheda_cliente_t.quantita) AS giacenza_attuale,
ceiling((prodotto_t.giacenza - sum(scheda_cliente_t.quantita))/prodotto_t.tasso_conversione) AS  giacenza_unita
FROM  trattamento_t , prenotazione_t , scheda_cliente_t , prodotto_t 
WHERE trattamento_t.id_prenotazione = prenotazione_t.id_prenotazione 
and prenotazione_t.id_cliente = scheda_cliente_t.id_cliente 
and prodotto_t.id_prodotto = scheda_cliente_t.id_prodotto 
and data_prenotazione BETWEEN '2022-04-25' AND '2022-05-01'
group by prodotto_t.nome, prodotto_t.giacenza, prodotto_t.tasso_conversione;







#QUERY 19: Verificare la quantità di prodotti in unità presenti in magazzino


SELECT prodotto_t.nome,  prodotto_t.tasso_conversione, prodotto_t.giacenza_minima,
ceiling((prodotto_t.giacenza - sum(scheda_cliente_t.quantita))/prodotto_t.tasso_conversione) AS  giacenza_unita
FROM  trattamento_t , prenotazione_t , scheda_cliente_t , prodotto_t 
WHERE trattamento_t.id_prenotazione = prenotazione_t.id_prenotazione 
and prenotazione_t.id_cliente = scheda_cliente_t.id_cliente 
and prodotto_t.id_prodotto = scheda_cliente_t.id_prodotto 
group by prodotto_t.nome, prodotto_t.giacenza, prodotto_t.tasso_conversione




























