#records

Sovellus on albumien arviointisovellus, jossa käyttäjä voi antaa albumeille arvosanoja asteikolla 1–10.
Käyttäjä voi luoda tunnuksen ja kirjautua sisään sovellukseen.
Kirjautunut käyttäjä voi lisätä uusia albumeita, muokata niitä ja poistaa niitä.
Käyttäjä näkee kaikki lisätyt albumit listana.
Käyttäjä voi etsiä albumeita hakusanalla (esim. albumin nimi tai artisti).
Sovelluksen testaaminen omalla koneella:
Kloonaa projekti omalle koneelle
Asenna tarvittavat kirjastot komennolla pip install -r requirements.txt
Luo tietokanta ajamalla .sql-tiedosto (esim. sqlite3 database.db < schema.sql)
Käynnistä sovellus komennolla python app.py
Avaa selain ja mene osoitteeseen http://localhost:5000
Huomaa, että database.db-tiedosto ei ole mukana repositoriossa, vaan se täytyy luoda itse .sql-tiedostojen avulla.
