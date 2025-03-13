# Analisi delle Prestazioni tra PostgreSQL e MongoDB

## Introduzione

Ho eseguito un benchmark per confrontare le prestazioni di PostgreSQL (database relazionale) e MongoDB (database non relazionale) su diverse operazioni: INSERT, SELECT, SELECT_ALL, UPDATE, DELETE. I dati sono stati testati sia in formato CSV che JSON per valutare eventuali differenze di efficienza.

## Risultati del Benchmark

| Operazione | PostgreSQL CSV (s) | MongoDB CSV (s) | PostgreSQL JSON (s) | MongoDB JSON (s) |
| ---------- | ------------------ | --------------- | ------------------- | ---------------- |
| INSERT     | 0.7719             | 0.1328          | 0.7565              | 0.1123           |
| SELECT     | 0.8759             | 2.3201          | 0.8548              | 2.2677           |
| SELECT_ALL | 0.0096             | 0.0226          | 0.0087              | 0.0202           |
| UPDATE     | 1.0218             | 2.6915          | 1.0485              | 3.1689           |
| DELETE     | 0.0084             | 0.1792          | 0.0097              | 0.3635           |

## Interpretazione dei Risultati

- **INSERT**: MongoDB è molto più veloce di PostgreSQL perché gestisce documenti JSON in modo nativo e non ha vincoli di schema rigido come PostgreSQL, che deve validare le chiavi e mantenere la consistenza referenziale.
- **SELECT (ricerca per ID)**: PostgreSQL è più veloce rispetto a MongoDB. Questo accade perché il linguaggio SQL utilizza indici ottimizzati per la ricerca su chiavi primarie, mentre MongoDB esegue la ricerca all'interno di documenti JSON, risultando più lento.
- **SELECT_ALL (lettura di tutti i dati)**: Entrambi i database sono molto efficienti in questa operazione, con PostgreSQL leggermente più veloce.
- **UPDATE**: PostgreSQL è più veloce nell'aggiornamento dei record rispetto a MongoDB. Questo perché nel database relazionale, la modifica dei dati avviene con un'operazione ottimizzata a livello di riga, mentre in MongoDB ogni documento deve essere aggiornato separatamente.
- **DELETE**: PostgreSQL elimina i record in modo quasi istantaneo, mentre MongoDB impiega più tempo. Questo può essere dovuto alla modalità di gestione dello storage e alla necessità di rimuovere i documenti in un formato JSON strutturato.

## Conclusione

I risultati mostrano che MongoDB è più veloce nelle operazioni di INSERT, mentre PostgreSQL è generalmente più efficiente nelle ricerche e nelle operazioni di modifica e cancellazione. Per applicazioni con molte operazioni di lettura e aggiornamento, un database relazionale come PostgreSQL potrebbe essere la scelta migliore. Se invece il focus è sulla velocità di scrittura e sulla flessibilità del modello dati, MongoDB offre vantaggi significativi.

L'uso di CSV o JSON non influisce drasticamente sulle prestazioni di PostgreSQL, mentre per MongoDB il formato JSON risulta più naturale e leggermente più veloce in alcune operazioni.

## Come Avviare il Progetto

Per avviare questo progetto, segui i passaggi seguenti dopo aver creato un db su postgres tramite ```script.sql``` :
### Creazione di un Ambiente Virtuale

1. Apri il terminale e naviga nella directory del progetto

2. Crea un ambiente virtuale:

```sh
python -m venv venv
```

3. Attiva l'ambiente virtuale:

- Su Windows:
  ```sh
  .\venv\Scripts\activate
  ```
- Su macOS/Linux:
  ```sh
  source venv/bin/activate
  ```

### Installazione delle Dipendenze

4. Installa le dipendenze richieste:

```sh
pip install -r requirements.txt
```

### Modifica dei Dati di Collegamento ai Database

5. Prima di eseguire il benchmark, è necessario configurare i dati di collegamento ai database PostgreSQL e MongoDB. Apri il file `script.py` e modifica le seguenti sezioni con le informazioni corrette per il tuo ambiente:

#### Configurazione PostgreSQL

```python
SQL_DB = {
  "host": "localhost",
  "user": "postgres",
  "password": "password",
  "database": "benchmark"
}
```

#### Configurazione MongoDB

Se il tuo MongoDB richiede autenticazione, fornisci `username` e `password`. Se non è richiesta autenticazione, imposta `username` e `password` su `None`.

```python
MONGO_DB = {
    "host": "localhost",
    "port": 27017,
    "username": None,
    "password": None,
    "authSource": "admin",
    "database": "benchmark_db"
}
```

Assicurati che i database siano in esecuzione e accessibili con le credenziali fornite. Salva le modifiche e procedi con l'esecuzione del benchmark.

### Creazione dei dati necessari per il Benchmark:

6. Esegui il file per la creazione dei dati:

```sh
python generate_data.py
```

### Esecuzione del Benchmark

7. Esegui il file di benchmark:

```sh
python benchmark.py
```

I risultati saranno visibili da terminale

### Disattivazione dell'Ambiente Virtuale

8. Una volta terminato, puoi disattivare l'ambiente virtuale:

```sh
deactivate
```

Seguendo questi passaggi, sarai in grado di configurare l'ambiente e avviare il benchmark per confrontare le prestazioni di PostgreSQL e MongoDB.
