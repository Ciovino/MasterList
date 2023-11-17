# MasterList
Il bot telegram per gestire diversi tipi di liste: ricettario, inventario, serie e film da guardare, playlist, lista della spesa...

## Changelog
### Versione 0.5 (Usiamoli un po' meglio sti file)
Miglioramento nell'utilizzo delle liste: puoi vedere cosa hai salvato, cancellare alcune frasi, modificarne altre e basta per ora.
#### Novità
- _Aggiornamento comando /salva_: Ora puoi scrivere il messaggio da salvare dopo il comando;
- _Nuovo comando /mostra_: Visualizza l'intero contenuto del file attivo;
- _Comando /elimina_: Il comando _/cancella_ vecchio (per cancellare file interi) diventa _/elimina_;
- _Nuovo comando /cancella_: Cancella una riga dal file attivo;
- _Nuovo comando /modifica_: Modifica una riga dal file attivo.
#### Comandi
- _/salva \[messaggio da salvare\]_: Salva sul file attivo;
- _/mostra_: Visualizza file attivo;
- _/cancella_: Cancella una riga da un file;
- _/modifica_: Modifica una riga da un file;
- _/elimina_: Elimina un file esistente.

### Versione 0.4 (Praticamente come nuovo)
Nuovo codice, nuova organizzazione, anche nuovo nome.
#### Novità
- _State\_Machine_: Macchina a stati finiti per gli utenti;
- _Comando /state_: Per visualizzare in quale magnifico stato ti trovi ([Suggestion #10](https://github.com/Ciovino/Filmettini/issues/10)).
#### Comandi
- */start*: Manda un saluto all'utente;
- */file*: Tutto ciò che serve per salvare le robe utili;
- */crea*: Crea nuovi file;
- */cambia*: Cambia il file attivo;
- */salva*: Salva sul file attivo;
- */cancella*: Cancella un file esistente;
- */about*: Presentazione del bot, per sapere abilità, versione e residenza;
- */state*: Visualizza il nome dello stato;
- */back*: Annulla l'ultima operazione.

### Verisione 0.3 (Ma come parli bene)
Nuova gestione dei messaggi del bot: l'ordine è importante.
#### Novità
- _Mex\_Manager_: Gestione messaggi tramite tabelle e file json.
#### Bug Risolti
- _Creazione di un nuovo file_: [Issue #7](https://github.com/Ciovino/Filmettini/issues/7): Durante la creazione di un nuovo file, veniva erroneamente salvato il contenuto dell'ultimo file attivo nel file appena creato.
#### Comandi
- */start*: Manda un saluto all'utente;
- */file*: Tutto ciò che serve per salvare le robe utili;
- */save*: Salva sul file attivo;
- */delete*: Cancella un file esistente;
- */about*: Presentazione del bot, per sapere abilità, versione e residenza;
- */back*: Annulla l'ultima operazione.

### Versione 0.2.1 (Presentazioni e Bug)
Una presentazione migliorata, leggermente più tecnica, e poi qualche bug in meno (si spera)
#### Novità
- _Nuova presentazione_: Presentazione fatta meglio.
#### Bug Risolti
- _Riconoscimento utente_: [Issue #5](https://github.com/Ciovino/Filmettini/issues/5): Miglioramento dei controlli dell'utente che manda i messaggi.
#### Comandi
- */start*: Manda un saluto all'utente;
- */file*: Tutto ciò che serve per salvare le robe utili;
- */save*: Salva sul file attivo;
- */delete*: Cancella un file esistente;
- */about*: Presentazione;
- */back*: Annulla l'ultima operazione.

### Versione 0.2 (File-inator)
Cominciamo a salvare roba
#### Novità
- _Comando /file_: il bot ti presenta una serie di opzioni:
	- _Nuovo File_: crea un nuovo file in cui salvare robe (per ora solo frasi);
	- _Salva Roba_: salva in un file;
	- _Scancellamento_: cancella file.
- _Comando /back_: Annulla l'ultima operazione
#### Comandi
- */start*: Manda un saluto all'utente;
- */file*: Tutto ciò che serve per salvare le robe utili;
- */about*: Presentazione;
- */back*: Annulla l'ultima operazione.

### Versione 0.1 (Approcci)
Ora si presenta per bene e si ricorderà di te.
#### Novità
- _Comando /start_: Ora il bot si ricorda se hai usato il comando almeno una volta, e ti risponde in modo diverso.
- _Comando /about_: Presentazione del bot, per conoscere ciò che può fare, ciò che saprà fare e forse anche ciò che potrebbe fare.
#### Comandi
- */start*: Manda un saluto all'utente;
- */about*: Presentazione. 

### Versione 0.0 (Primo incontro)
Praticamente la prima versione del bot, non che ci sia molto da vedere
#### Comandi
- */start*: Manda un saluto all'utente.