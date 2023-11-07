#OLAP
#FUNZIONALITA 1: 
SELECT anagrafica_t.descrizione, prodotto_t.nome, scheda_cliente_t.quantita
FROM  scheda_cliente_t, prodotto_t, anagrafica_t
WHERE scheda_cliente_t.id_anagrafica=anagrafica_t.id_anagrafica 
AND scheda_cliente_t.id_prodotto=prodotto_t.id_prodotto;
#FUNZIONALITA 2-4: 
SELECT anagrafica_t.descrizione, personale_t.id_personale, feedback_t.punteggio
FROM anagrafica_t, trattamento_t, personale_t, feedback_t, prenotazione_t, appuntamento_t
WHERE trattamento_t.id_prenotazione=prenotazione_t.id_prenotazione
AND prenotazione_t.id_prenotazione=appuntamento_t.id_prenotazione
AND appuntamento_t.id_anagrafica=anagrafica_t.id_anagrafica
AND personale_t.id_personale=trattamento_t.id_personale
AND trattamento_t.id_trattamento=feedback_t.id_trattamento;
#FUNZIONALITA 3-5:
SELECT pagamento_t.importo, prenotazione_t.data_prenotazione 
FROM prenotazione_t, trattamento_t, pagamento_t
WHERE prenotazione_t.id_prenotazione=trattamento_t.id_prenotazione
AND pagamento_t.id_trattamento=trattamento_t.id_trattamento;

