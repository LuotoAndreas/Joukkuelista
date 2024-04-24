from flask import Flask, request, Response, render_template
import time
import json
from datetime import datetime

app = Flask(__name__)

# Ota tämä tiedosto käyttöön eu.pythonanywhere-palvelimella
# Täydennä funktiot toimimaan oikealla tavalla

# Mikään funktio ei saa missään tilanteessa palauttaa server erroria (500 Internal Server Error)

#sijoita pohja.xhtml-tiedosto templates-kansioon, niin sivu toimii
#suoraan osoitteesta /vt1
@app.route('/vt1')
def vt1():
    return render_template('pohja.xhtml')


@app.route('/jarjestaLeimaustavat', methods = ['POST', 'GET'])
def jarjestaLeimaustavat():
    """
    TASO 1

    Järjestää leimaustavat aakkosjärjestykseen
    Järjestämisen täytyy olla caseinsensitive

    request.form["ltavat"] sisältää json-muodossa järjestettävät leimaustavat

    Tämä funktio ei saa kaatua vaikka requestissa tulisi epäkelpoa sisältöä. 
    Mahdollisessa virhetilanteessa tämä funktio palauttaa http-koodin 400 Bad Request
    ja mahdollisen virheilmoituksen. Esim.
    return Response("Leimaustavat olivat väärässä muodossa", mimetype="text/plain"), 400
    kts. https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/400

    Huom. nämä olisi oikeasti järkevämpää järjestää tämän sovelluksen javascript-osassa

    Returns:
          Response-objektin, jonka sisältö on aakkosjärjestetty lista leimaustavoista JSON-muodossa
          mediatyypin on oltava "application/json"
    """

    leimaustavat = json.loads(request.form["ltavat"])
    return Response("Virhetilanne 400", mimetype="text/plain"), 400

    return Response(json.dumps(leimaustavat), mimetype="application/json")

@app.route('/jarjestaSarjat', methods = ['POST', 'GET'])
def jarjestaSarjat():
    """
    TASO 1

    Järjestää sarjat numeeriseen järjestykseen sarjan nimen perusteella. Esim. sarjat "2h", "10h" ja "8h"
    pitää palauttaa järjestyksessä "2h", "8h", "10h"

    Järjestäminen on caseinsensitive.
    Järjestämisessä ei huomioida whitespacea nimen alussa tai lopussa

    request.form["sarjat"] sisältää json-muodossa järjestettävät sarjat

    Tämä funktio ei saa kaatua vaikka requestissa tulisi epäkelpoa sisältöä.
    Mahdollisessa virhetilanteessa tämä funktio palauttaa http-koodin 400 Bad Request
    ja mahdollisen virheilmoituksen. vrt. jarjestaLeimaustavat

    Huom. nämä olisi oikeasti järkevämpää järjestää tämän sovelluksen javascript-osassa

    Returns:
          Response-objektin, jonka sisältö on aakkosjärjestetty lista sarjoista JSON-muodossa
          mediatyypin on oltava "application/json"
    """

    return Response(request.form["sarjat"], mimetype="application/json")




@app.route('/lisaaSarja', methods = ['POST', 'GET'])
def lisaaSarja():
    """
    TASO 1

    Lisää sarjalistaan uuden sarjan

    request.form["sarjalista"] sisältää json-muodossa sarjalistauksen
    request.form["nimi"] sisältää lisättävän sarjan nimen
    request.form["kesto"] sisältää lisättävän sarjan keston
    request.form["alkuaika"] sisältää lisättävän sarjan alkuajan
    request.form["loppuaika"] sisältää lisättävän sarjan loppuajan

    sarjaa ei lisätä, jos on jo olemassa samanniminen sarja. Sarjojen 
    nimien vertailu on caseinsensitive eikä whitespacea huomioida nimen 
    alussa tai lopussa. Nimi ei saa olla tyhjä.
    sarjaa ei lisätä, jos kesto ei ole kelvollinen nollaa suurempi kokonaisluku
    alkuaika ei ole pakollinen, mutta jos alkuaika on annettu, on sen oltava ISO8601-muotoa paitsi ilman T- ja Z-kirjaimia ( 2023-01-04 15:51:52 )
    loppuaika ei ole pakollinen, mutta jos loppuaika on annettu, on sen oltava ISO8601-muotoa paitsi ilman T- ja Z-kirjaimia ( 2023-01-04 15:51:52 ) ja loppuajan on oltava suurempi kuin alkuajan
    sarjaa ei lisätä, jos mahdollinen alkuaika tai loppuaika ei ole kelvollista muotoa
    Lisätylle sarjalle on keksittävä uusi uniikki id
    Uusi sarja on muotoa:
    {
      "nimi": <String>,
      "kesto": <Integer>,
      "alkuaika": <String>,
      "loppuaika": <String>,
      "id": <Integer>
    }


    Tämä funktio ei saa kaatua vaikka requestissa tulisi epäkelpoa sisältöä.
    Kaatumistilanteessa tämä funktio palauttaa http-koodin 400 Bad Request
    ja mahdollisen virheilmoituksen. vrt. jarjestaLeimaustavat

    Validoinnin epäonnistuessa funktio palauttaa http-koodin 422 ja mahdollisen virheilmoituksen
    kts. https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/422


    Returns:
          Response-objektin, jonka sisältö on muutettu tai muuttumaton sarjalista JSON-muodossa
          mediatyypin on oltava "application/json"
    """


    return Response(request.form["sarjalista"], mimetype="application/json")

@app.route('/poistaJoukkue', methods = ['POST', 'GET'])
def poistaJoukkue():
    """
    TASO 1

    Poistaa joukkueen

    request.form["id"] sisältää poistettavan joukkueen id:n
    request.form["joukkuelista"] sisältää listan kaikista joukkueista JSON-muodossa

    Poistamista ei tehdä, jos id:tä vastaavaa joukkuetta ei löydy

    Poistamisen epäonnistuessa (id:tä ei löydy) funktio palauttaa http-koodin 422 ja selkeän virheilmoituksen

    Tämä funktio ei saa kaatua vaikka requestissa tulisi epäkelpoa sisältöä.
    Kaatumistilanteessa tämä funktio palauttaa http-koodin 400 Bad Request
    ja mahdollisen virheilmoituksen. vrt. jarjestaLeimaustavat

    Returns:
          Response-objektin, jonka sisältö on muutettu tai muuttumaton joukkuelista JSON-muodossa.
          mediatyypin on oltava "application/json"
    """


    return Response(request.form["joukkuelista"], mimetype="application/json")


@app.route('/jarjestaRastit', methods = ['POST', 'GET'])
def jarjestaRastit():
    """
   TASO 3

   Järjestää rastit taulukkoon aakkosjärjestykseen rastikoodin perustella siten, että
   numeroilla alkavat rastit ovat kirjaimilla alkavien jälkeen. Huom! Tämä ei ole sama kuin natural sort.
   isoilla ja pienillä kirjaimilla ei ole järjestämisessä merkitystä (case insensitive). Järjestämisessä ei huomioida whitespacea nimen alussa tai lopussa

   palauttaa JSON-muodossa järjestetyn listan, joka sisältää kaikki rastiobjektit. Rastiobjektit ovat muotoa:
                                                     {
                                                        "id": rastit-objektissa käytetty kunkin rastiobjektin avain
                                                        "koodi": rastikoodi merkkijonona
                                                        "lat:: latitude liukulukuna
                                                        "lon": longitude liukulukuna
                                                     }



    request.form["rastit"] sisältää json-muodossa dictiin tallennetut järjestettävät rastit

    Tämä funktio ei saa kaatua vaikka requestissa tulisi epäkelpoa sisältöä.
    Kaatumistilanteessa tämä funktio palauttaa http-koodin 400 Bad Request
    ja mahdollisen virheilmoituksen. vrt. jarjestaLeimaustavat

    Huom. nämä olisi oikeasti järkevämpää järjestää tämän sovelluksen javascript-osassa

    Returns:
          Response-objektin, jonka sisältö on aakkosjärjestetty lista rasteista JSON-muodossa
          mediatyypin on oltava "application/json"
    """

    #tässä palautetaan vain esimerkki eikä vielä oikeaa dataa. täydennä toimivaksi
    return Response(json.dumps( [{"id":1, "koodi": "mallirasti", "lat": 64.1, "lon": 25.1}]), mimetype="application/json")



@app.route('/lisaaJoukkue', methods = ['POST', 'GET'])
def lisaaJoukkue():
    """
    TASO 3

     Lisää uuden joukkueen joukkueet-listaan ja palauttaa muuttuneen datan
    Joukkue lisätään vain jos kaikki seuraavat ehdot täyttyvät:
    - Toista samannimistä joukkuetta ei ole olemassa. Nimien vertailussa
      ei huomioida isoja ja pieniä kirjaimia tai nimen alussa ja lopussa välilyöntejä etc. (whitespace). Nimien vertailu on siis caseinsensitive.
      Joukkueen nimi ei voi olla pelkkää whitespacea.
    - Leimaustapoja on annettava vähintään yksi kappale. Leimaustapojen
       on löydyttävä leimaustavat-taulukosta
    - Jäseniä on annettava vähintään kaksi kappaletta.
    - Saman joukkueen jäsenillä ei saa olla kahta samaa nimeä (caseinsensitive eikä huomioida alussa lopussa whitespacea)
    - Sarjan id, jota vastaava sarja on löydyttävä sarjat-listasta

    Uusi joukkue tallennetaan joukkueet-taulukkoon. Joukkueen on oltava seuraavaa muotoa:
    {
       "id": {Number}, // jokaisella joukkueella oleva uniikki kokonaislukutunniste
       "nimi": {String}, // Joukkueen uniikki nimi
       "jasenet": {Array}, // taulukko joukkueen jäsenien uniikeista nimistä
       "leimaustapa": {Array}, // taulukko joukkueen leimaustapojen indekseistä (kts. data["leimaustavat"])
       "rastileimaukset": {Array}, // taulukko joukkueen rastileimauksista. Oletuksena tyhjä eli []
       "sarja": {Number}, // joukkueen sarjan id
       "pisteet": {Number}, // joukkueen pistemäärä, oletuksena 0
       "matka": {Number}, // joukkueen kulkema matka, oletuksena 0
       "aika": {String}, // joukkueen käyttämä aika "h:min:s", oletuksena "00:00:00"
    }


    request.form["data"] sisältää json-muodossa koko käsiteltävän tietorakenteen
    request.form["nimi"] sisältää lisättävän joukkueen nimen
    request.form["leimaustavat"] joukkueen leimaustavat json-muodossa
    request.form["sarja"] joukkueen sarja
    request.form["jasenet"] lista joukkueen jäsenistä json-muodossa

    Tämä funktio ei saa kaatua vaikka requestissa tulisi epäkelpoa sisältöä.
    Kaatumistilanteessa tämä funktio palauttaa http-koodin 400 Bad Request
    ja mahdollisen virheilmoituksen. vrt. jarjestaLeimaustavat

    Validoinnin epäonnistuessa funktio palauttaa http-koodin 422 ja mahdollisen virheilmoituksen
    kts. https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/422

    Returns:
          Response-objektin, jonka sisältö on muutettu tai muuttumaton data JSON-muodossa
          mediatyypin on oltava "application/json"
    """


    return Response(request.form["data"], mimetype="application/json")



def laskeAika(joukkue):
    """
    Taso 3

    Laskee joukkueen käyttämän ajan. Tulos tallennetaan joukkue["aika"]-ominaisuuteen.
    Käytä merkkijonoa, jossa aika on muodossa "hh:mm:ss". Esim. "07:30:35"
    Jos aikaa ei kyetä laskemaan, funktio palauttaa tyhjän merkkijonon "00:00:00"
    Aika lasketaan viimeisestä (leimausajan mukaan) LAHTO-rastilla tehdystä leimauksesta alkaen aina
    ensimmäiseen (leimausajan mukaan) MAALI-rastilla tehtyyn leimaukseen asti. Leimauksia jotka tehdään
    ennen viimeistä lähtöleimausta tai ensimmäisen maalileimauksen jälkeen ei huomioida.

    Täydennä funktiolle tarpeelliset parametrit. Kutsu tätä funktiota jarjestaJoukkueet-funktiosta
    tarpeellisiksi katsomillasi parametreilla.

    """
    return joukkue

@app.route('/jarjestaJoukkueet', methods = ['POST', 'GET'])
def jarjestaJoukkueet():
    """
    Taso 3 ja 5
    Järjestää joukkueet järjestykseen haluttujen tietojen perusteella
    järjestetään ensisijaisesti kasvavaan aakkosjärjestykseen mainsort-parametrin mukaisen tiedon perusteella. mainsort voi olla joukkueen nimi, sarjan nimi, matka, aika tai pisteet
    Joukkueen jäsenet järjestetään aina kasvavaan aakkosjärjestykseen.
    Joukkueen leimaustavat järjestetään myös aina aakkosjärjestykseen leimaustapojen nimien mukaan
    Isoilla ja pienillä kirjaimilla ei ole missään järjestämisissä merkitystä (case insensitive) eikä myöskään alussa tai lopussa olevalla whitespacella. Vertailu on siis aina caseinsensitive.

    sortorder-parametrin käsittely vain tasolla 5
    jos sortorder-parametrina on muuta kuin tyhjä taulukko, käytetään
    sortorderin ilmoittamaa järjestystä eikä huomioida mainsort-parametria:
    ensisijaisesti järjestetään sortorder-taulukon ensimmäisen alkion tietojen perusteella,
    toissijaisesti sortorder-taulukon toisen jne.
    sortorder-taulukko sisältää dicteja, joissa kerrotaan järjestysehdon nimi (key),
    järjestyssuunta (order, 1 = nouseva, -1 = laskeva) ja järjestetäänkö numeerisesti (True)
    vai aakkosjärjestykseen (False)
    Toteuta sortorder-taulukon käsittely siten, että taulukossa voi olla vaihteleva määrä rivejä
    esimerkki sortorder-taulukosta:
        sortorder = [
        {"key": "sarja", "order": 1, "numeric": False},
        {"key": "nimi", "order": 1, "numeric": False},
        {"key": "matka", "order": -1, "numeric": True},
        {"key": "aika", "order": 1, "numeric": False},
        {"key": "pisteet", "order": -1, "numeric": True}
       ]

    request.form["joukkueet"] sisältää json-muodossa järjestettävät joukkueet
    request.form["mainsort"] sisältää json-muodossa käytettävän järjestysavaimen
    request.form["sortorder"] sisältää json-muodossa järjestysehdot
    request.form["leimaustavat"] sisältää json-muodossa listan kaikista leimaustavoista
    request.form["rastit"] sisältää json-muodossa dictin, jossa ovat kaikki tapahtuman rastit
    request.form["sarjat"] sisältää json-muodossa sarjat-listan

    Tämä funktio myös kutsuu jokaiselle joukkueelle laskeAika-funktiota (taso 3) sekä laskePisteet- ja laskeMatka-funktiota (taso 5).

    Tämä funktio ei saa kaatua vaikka requestissa tulisi epäkelpoa sisältöä.
    Kaatumistilanteessa tämä funktio palauttaa http-koodin 400 Bad Request
    ja mahdollisen virheilmoituksen. vrt. jarjestaLeimaustavat

    Huom. nämä olisi oikeasti järkevämpää järjestää tämän sovelluksen javascript-osassa

    Returns:
          Response-objektin, jonka sisältö on aakkosjärjestetty lista joukkueista JSON-muodossa
          mediatyypin on oltava "application/json"
    """



    return Response(request.form["joukkueet"], mimetype="application/json")



def laskeMatka(joukkue, rastit):
    """
   Taso 5

   Laskee joukkueen kulkeman matkan. Matka tallennetaan 
   joukkue["matka"]-ominaisuuteen liukulukuna Laske kuinka pitkän matkan 
   kukin joukkue on kulkenut eli laske kunkin rastivälin pituus ja laske 
   yhteen kunkin joukkueen kulkemat rastivälit. Jos rastille ei löydy 
   sijaintitietoa (lat ja lon), niin kyseistä rastia ei lasketa matkaan 
   mukaan. Matka lasketaan viimeisestä LAHTO-rastilla tehdystä 
   leimauksesta alkaen aina ensimmäiseen MAALI-rastilla tehtyyn 
   leimaukseen asti. Leimauksia jotka tehdään ennen viimeistä 
   lähtöleimausta tai ensimmäisen maalileimauksen jälkeen ei huomioida.
   Huom. ennen lähtöleimausta tehtyjä maalileimauksia ei myöskään huomioida
   Rastikäynneistä huomioidaan aina vain ensimmäinen eli jos joukkue on 
   leimannut saman rastin useampaan kertaan, vain ensimmäinen leimaus 
   huomioidaan matkassa

   Täydennä funktiolle tarpeelliset parametrit
    """
    return joukkue

def laskePisteet(joukkue, rastit):
    """
   Taso 5

   Laskee joukkueen saamat pisteet. Pistemäärä tallennetaan joukkue["pisteet"]-ominaisuuteen
   Joukkue saa kustakin rastista pisteitä rastin koodin ensimmäisen merkin
   verran. Jos rastin koodi on 9A, niin joukkue saa yhdeksän (9) pistettä. Jos rastin
   koodin ensimmäinen merkki ei ole kokonaisluku, niin kyseisestä rastista saa nolla
   (0) pistettä. Esim. rasteista LÄHTÖ ja F saa 0 pistettä.
   Samasta rastista voi sama joukkue saada pisteitä vain yhden kerran. Jos
   joukkue on leimannut saman rastin useampaan kertaan lasketaan kyseinen rasti
   mukaan pisteisiin vain yhden kerran.
   Rastileimauksia, jotka tehdään ennen lähtöleimausta tai maalileimauksen jälkeen, ei
   huomioida.
   Maalileimausta ei huomioida kuin vasta lähtöleimauksen jälkeen.
   Jos joukkueella on useampi lähtöleimaus, niin pisteet lasketaan vasta
   viimeisen lähtöleimauksen jälkeisistä rastileimauksista.
   Joukkue, jolla ei ole ollenkaan rastileimauksia, saa 0 pistettä


   Täydennä funktiolle tarpeelliset parametrit
    """
    return joukkue






