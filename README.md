#records

1. Sovellus on albumien arviointisovellus, jossa käyttäjä voi antaa albumeille arvosanoja asteikolla 1–10.
2. Käyttäjä voi luoda tunnuksen ja kirjautua sisään sovellukseen.
3. Kirjautunut käyttäjä voi lisätä uusia albumeita, muokata niitä ja poistaa niitä.
4. Käyttäjä näkee kaikki lisätyt albumit listana.
5. Käyttäjä voi etsiä albumeita hakusanalla (esim. albumin nimi tai artisti).

Ohjeet:
Sovelluksen testaaminen omalla koneella:
- Kloonaa projekti omalle koneelle
- Asenna tarvittavat kirjastot komennolla pip install -r requirements.txt
- Luo tietokanta ajamalla .sql-tiedosto (esim. sqlite3 database.db < schema.sql)
- Käynnistä sovellus komennolla python app.py
  
Huomaa, että database.db-tiedosto ei ole mukana repositoriossa, vaan se täytyy luoda itse .sql-tiedostojen avulla.
