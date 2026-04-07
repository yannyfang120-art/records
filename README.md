# Records
Records on yksinkertainen sovellus, jossa käyttäjät voivat arvioida albumeita asteikolla 1-10, selata muiden lisäämiä albumeita ja hallita omia tietojaan. 

## Ominaisuudet
- Käyttäjä voi luoda tunnuksen ja kirjautua sisään.
- Kirjautunut käyttäjä voi:
  - Lisätä uusia albumeita
  - Muokata olemassa olevia albumeita
  - Poistaa albumeita
- Kaikki lisätyt albumit näkyvät listana.
- Albumeita voi etsiä hakusanalla (esim. albumin nimi tai artisti).
- Arvosteluasteikko: 1–10.

## Käyttöönotto
Asenna Flask kirjasto:
```bash
pip install flask
```
Luo tietokannan taulut ja lisää alkutiedot:
```bash
sqlite3 database.db < schema.sql
sqlite3 database.db < init.sql
```
Käynnistä sovellus:
```bash
flask run
```
