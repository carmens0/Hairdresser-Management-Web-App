# 💇‍♂️ Hairdresser Management Web App
<img src="./fig/portfolio-3.png" width="800" class="center">

## 📌 Descrizione
Questo progetto consiste in una **Web App** sviluppata con **Flask** per gestire un **database di un negozio di parrucchieri**. L'applicazione permette di gestire prenotazioni, dipendenti, prodotti e flussi di cassa in modo semplice e intuitivo.

## 🛠️ Tecnologie Utilizzate
- **Python** (Flask, MySQL Connector)
- **MySQL** (Database per la gestione dei dati)
- **HTML, CSS** (Interfaccia grafica per la Web App)

## 🚀 Installazione
### 1️⃣ Installare Flask
Aprire il terminale ed eseguire:
```bash
pip install flask
```

### 2️⃣ Configurare il Database
- Importare il file `hairdresser.sql` in MySQL.
- Aprire il file `app.py` e configurare le credenziali di accesso al database:
```python
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'hairdresser'
```

### 3️⃣ Avviare il Server
Eseguire il file `app.py`:
```bash
python app.py
```
Aprire il browser e visitare:
```
http://localhost:5000
```

---

## 🎯 Funzionalità Implementate
### 📅 Gestione Prenotazioni
- Inserimento di una nuova prenotazione (`POST`)
- Visualizzazione delle prenotazioni tramite ID (`GET`)

### 👥 Gestione Dipendenti
- Aggiunta di un nuovo dipendente (`POST`)
- Visualizzazione dei trattamenti effettuati da un dipendente in un intervallo di tempo (`GET`)
- Visualizzazione dei feedback ricevuti (`GET`)

### 🛒 Gestione Prodotti
- Aggiunta di un nuovo prodotto nel database (`POST`)

### 💰 Gestione Flusso di Cassa
- Visualizzazione del flusso di cassa in un giorno specifico (`GET`)
- Visualizzazione del fatturato in un intervallo di date (`GET`)
- Visualizzazione del totale fatturato da un cliente specifico (`GET`)

---

## 📄 Struttura del Progetto
📂 `hairdresser.sql` → File del database MySQL  
📂 `app.py` → Script principale Flask  
📂 `templates/` → Pagine HTML  
📂 `static/` → File CSS e immagini  

---

## 👨‍💻 Autori
**Gruppo 6: Web App**
- Capaldo Gennaro
- Diletto Alessandro Pio
- Senatore Carmela Pia

📌 **Università degli Studi di Salerno**

---

💡 Sentiti libero di contribuire e migliorare il progetto! 🚀

