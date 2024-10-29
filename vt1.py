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
    try:
        if "ltavat" not in request.form:
            return Response("Error, virhe ladatessa leimaustapoja", mimetype="text/plain"), 422        

        leimaustavat = json.loads(request.form["ltavat"])

        jarjestetytLeimaustavat = sorted(leimaustavat, key=str.casefold)
        
        return Response(json.dumps(jarjestetytLeimaustavat), mimetype="application/json")
        
    except (KeyError, json.JSONDecodeError):
        return Response("Leimaustavat olivat väärässä muodossa", mimetype="text/plain"), 400

    

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

    try:
        if "sarjat" not in request.form:
            print("Error: sarjat eivät ole oikeassa muodossa")
            return Response("Error, sarjat eivät ole saatavilla", mimetype="text/plain"), 400

        sarjat = json.loads(request.form["sarjat"])

        if not isinstance(sarjat, list):
            return Response("Error, sarjat eivät ole listana", mimetype="text/plain"), 400

        jarjestetytSarjat = sorted(sarjat, key=lambda x: (len(x['nimi'].strip()), x['nimi'].strip().lower()))
        return Response(json.dumps(jarjestetytSarjat), mimetype=("application/json"))

    except (KeyError, json.JSONDecodeError):
        print("Virhe: Sarjat olivat väärässä muodossa JSON-dekoodauksen aikana.")
        return Response("Sarjat olivat väärässä muodossa", mimetype="text/plain"), 400
  




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
    try:
        required_fields = ["sarjalista", "nimi", "kesto", "alkuaika", "loppuaika"]
        for field in required_fields:
            if field not in request.form:
                print("Error: fieldi puuttuu")
                return Response("Error, kyseinen fieldi puuttuu", mimetype="text/plain"), 400

        if int(request.form["kesto"]) <= 0:
            return Response("Error, kesto ei validi", mimetype="text/plain"), 422
        
        alkuaika = request.form["alkuaika"]
        loppuaika = request.form["loppuaika"]

        if alkuaika:
            try: 
                alkuaika = datetime.strptime(alkuaika, '%y-%m-%d %H:%M:%S')
            except ValueError:
                return Response("Error, alkuaika väärässä muodossa", mimetype="text/plain"), 422  
                  
        if loppuaika: 
            try: 
                loppuaika = datetime.strptime(loppuaika, '%y-%m-%d %H:%M:%S')       
            except ValueError:
                return Response("Error, loppuaika väärässä muodossa", mimetype="text/plain"), 422
        
        if alkuaika and loppuaika and loppuaika <= alkuaika:
            return Response("Error, loppuajan oltava suurempi kuin alkuajan", mimetype="text/plain"), 422
            

        sarjalista = json.loads(request.form["sarjalista"])
        nimi = request.form["nimi"].strip().lower()

        for sarja in sarjalista:
            if sarja["nimi"].strip().lower() == nimi:
                return Response("Error, sarjan nimi on jo olemassa", mimetype="text/plain"), 422
                
        
        sarjaUusi = {
            "nimi": request.form["nimi"].strip(),
            "kesto": int(request.form["kesto"]),
            "alkuaika": alkuaika,
            "loppuaika": loppuaika,
            "id": max(sarja["id"] for sarja in sarjalista) + 1
            }
        
        sarjalista.append(sarjaUusi)
        
        return Response(json.dumps(sarjalista), mimetype=("application/json"))
    
    except (KeyError, json.JSONDecodeError):
        print("Virhe: Sarjat olivat väärässä muodossa JSON-dekoodauksen aikana.")
        return Response("Sarjat olivat väärässä muodossa", mimetype="text/plain"), 400

@app.route('/poistaJoukkue', methods = ['POST', 'GET'])
def poistaJoukkue():
    """

    muista alustaa se homma python -m flask run mutta joka päivä piti tehdä se joku komento ennen ehkä set FLASK_APP=vt1.py
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
    try:
        
        if "joukkuelista" not in request.form:
            return Response("Error, joukkuelistan lataaminen epäonnistui", mimetype="text/plain"), 422

        joukkuelista = json.loads(request.form["joukkuelista"])
        
        if "id" not in request.form:
            return Response("Error, Id:tä ei löytynyt", mimetype="text/plain")           
        
        id = int(request.form["id"])

        poistettavaJoukkue = None
        for joukkue in joukkuelista:
            try: 
                if joukkue["id"] == id:
                    poistettavaJoukkue = joukkue
                    break
            except:
                return Response("Error, id:tä ei löytynyt joukkuelistasta", mimetype="text/plain"), 422
        
        if poistettavaJoukkue is not None:
            joukkuelista.remove(poistettavaJoukkue)
        else: 
            return Response("Error, joukkueen id:tä ei löytynyt joukkuelistasta", mimetype="text/plain"), 422

        return Response(json.dumps(joukkuelista), mimetype=("application/json"))    

    except Exception as e:
        return Response(f"Error, joukkueen poistaminen epäonnistui: {str(e)}", mimetype="text/plain"), 400


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
    try:
        if "rastit" not in request.form:
            return Response("Error, rastilistan lataaminen epäonnistui", mimetype="text/plain")
        
        rastilista = json.loads(request.form["rastit"])
        rastit_listana = []

        # muutetaan rastilistan rakenne oikeaan muotoon
        for key, value in rastilista.items():
            if isinstance(value, dict) and 'koodi' in value and 'lat' in value and 'lon' in value:
                rastit_listana.append({
                    "id": key,
                    "koodi": value["koodi"],
                    "lat": value["lat"],
                    "lon": value["lon"]
            })

        try:
            jarjestetytRastit = sorted(rastit_listana, key=lambda x: (x["koodi"][0].isdigit(), x["koodi"].casefold()))
        except:
            return Response("Error, evirhe järjestäessä rastilistoja", mimetype="text/plain")
        
        return Response(json.dumps(jarjestetytRastit), mimetype="application/json")

    except (KeyError, json.JSONDecodeError):
        return Response("Error, rastien järjestäminen epäonnistui", mimetype="text/plain"), 400



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

    try:

        try:
            data = json.loads(request.form["data"])
            if not isinstance(data, dict):
                return Response("Error, data ei ole sanakirja", mimetype="text/plain"), 400
        except (json.JSONDecodeError, ValueError):
            return Response("Error, virheellinen JSON-data", mimetype="text/plain"), 400

        required_fields = ["nimi", "sarja", "leimaustavat", "jasenet"]    

        for field in required_fields:
            if field not in request.form:
                print(f"Error: {field} puuttuu")
                return Response(f"Error, {field} puuttuu", mimetype="text/plain"), 422

        nimi = request.form["nimi"].strip()
        sarja = int(request.form["sarja"])
        leimaustavat = json.loads(request.form["leimaustavat"])       
        jasenet = json.loads(request.form["jasenet"])

        for joukkue in data["joukkueet"]:
            joukkue_nimi = joukkue["nimi"].strip()
    
            if not nimi.casefold():
                return Response("Error, joukkueen nimi ei voi olla tyhjä", mimetype="text/plain"), 422
            
            if nimi.isspace():
                return Response("Error, joukkueen nimi ei voi olla whitesapcea", mimetype="text/plain"), 422
    
            if joukkue_nimi.casefold() == nimi.casefold():
                return Response("Error, joukkueen nimi on jo olemassa", mimetype="text/plain"), 422

        if not leimaustavat:
            return Response("Error, leimaustapoja ei valittu", mimetype="text/plain"), 422

        if not isinstance(data, dict):
            return Response("Error, leimaustapa data ei ole sanakirja", mimetype="text/plain"), 400

        olemassaOlevatLeimaustavat = data["leimaustavat"]    

        for leimaustapa in leimaustavat:
            if leimaustapa not in olemassaOlevatLeimaustavat:
                return Response("Error, leimaustapaa ei ole olemassa", mimetype="text/plain"), 422   

        jasenet = [jasen.strip() for jasen in jasenet if jasen.strip()]
        if len(jasenet) < 2:            
            return Response("Error, jäsenien lukumäärä on alle kaksi", mimetype="text/plain"), 422

        if len(jasenet) != len(set(jasen.strip().casefold() for jasen in jasenet)):
            return Response("Error, samannimiset jasenet ei sallittu", mimetype="text/plain"), 422

        if not sarja:
            return Response("Error, sarjaa ei valittu", mimetype="text/plain"), 422

        if not isinstance(data, dict):
            return Response("Error, sarja data ei ole sanakirja", mimetype="text/plain"), 400
        

        olemassaOlevatSarjat = [sarjaId["id"] for sarjaId in data["sarjat"]]

        if sarja not in olemassaOlevatSarjat:
            return Response("Error, sarjaa ei ole olemassa", mimetype="text/plain"), 422


        uusi_joukkue = {
            "id": max(joukkue["id"] for joukkue in data["joukkueet"]) + 1,
            "nimi": nimi,
            "jasenet": jasenet, 
            "leimaustapa": [data["leimaustavat"].index(leimaustapa) for leimaustapa in leimaustavat], 
            "rastileimaukset": [], 
            "sarja": sarja, 
            "pisteet": 0, 
            "matka": 0,
            "aika": "00:00:00"
        }

        data["joukkueet"].append(uusi_joukkue)

        return Response(json.dumps(data), mimetype="application/json")
            
    except Exception as e:
        return Response(f"Error, joukkueen lisääminen epäonnistui: {str(e)}", mimetype="text/plain"), 400
    



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
    
    try:        
        rastit = json.loads(request.form["rastit"])
        
        if not isinstance(rastit, dict):
            return Response("Error, data ei ole sanakirja", mimetype="text/plain"), 400

        haluttuLahto_rasti = 'LAHTO'
        haluttuMaali_rasti = 'MAALI'
        viimeisinLahtoaika = None
        ensimmaisinMaaliaika = None
        lahtoRastinKoodi = None
        maaliRastinKoodi = None

        # etsitään rasteista lahtoa ja maalia vastaava id
        for rastinId, rasti in rastit.items():
            if rasti["koodi"] == haluttuLahto_rasti:
                lahtoRastinKoodi = str(rastinId)
            if rasti["koodi"] == haluttuMaali_rasti:
                maaliRastinKoodi = str(rastinId)

        # etsitään rastileimausten viimeisin lähtöaika ja ensimmäisin maaliintuloaika
        for leimaus in joukkue["rastileimaukset"]:
            try:
                koodi = str(leimaus["rasti"]) 
                aika = leimaus["aika"]  

                if not koodi or not aika:
                    print("Puuttuva koodi tai aika joukkueelta: ", joukkue["nimi"])
                    continue

                if koodi == lahtoRastinKoodi:
                    if viimeisinLahtoaika is None or aika > viimeisinLahtoaika:
                        viimeisinLahtoaika = aika

                elif koodi == maaliRastinKoodi:
                    if ensimmaisinMaaliaika is None or aika < ensimmaisinMaaliaika:
                        ensimmaisinMaaliaika = aika
                
            except KeyError as e:
                print(f"Virhe joukkueelta {joukkue['nimi']}: Leimauksessa {leimaus} puuttuu avain {str(e)}, ei vaadi toimia.")

        if viimeisinLahtoaika and ensimmaisinMaaliaika:
            maaliaikaObjekti = datetime.strptime(ensimmaisinMaaliaika, '%Y-%m-%d %H:%M:%S')                
            lahtoaikaObjekti = datetime.strptime(viimeisinLahtoaika, '%Y-%m-%d %H:%M:%S')  
            
            kilpailuaika = maaliaikaObjekti - lahtoaikaObjekti
            
            if kilpailuaika.total_seconds() < 0:
                joukkue["aika"] = "00:00:00"
            else:
                joukkue["aika"] = str(kilpailuaika)
        else:
            joukkue["aika"] = "00:00:00"

    except ValueError:
        return Response("Error, virheellinen aikamuoto", mimetype="text/plain")
    except Exception as e:
        return Response(f"Error, joukkueen rastiajan laskeminen epäonnistui: {str(e)}", mimetype="text/plain")
    
    
@app.route('/jarjestaJoukkueet', methods = ['POST', 'GET'])
def jarjestaJoukkueet():
    """
    ehkä haetaan for joukkue in data["joukkueet"] niin joukkue = json.loads(niin voi muokata tätä       )

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
    try:
        joukkueet_data = request.form["joukkueet"]
        
        try:
            joukkueet = json.loads(joukkueet_data)
            
            if not isinstance(joukkueet, list):
                return Response(json.dumps({"error": "joukkueet ei ole lista"}), mimetype="application/json"), 400
            
        except json.JSONDecodeError:
            return Response(json.dumps({"error": "virheellinen JSON-data"}), mimetype="application/json"), 400

        jarjestetytJoukkueet = sorted(joukkueet, key=lambda joukkue: joukkue["nimi"].strip().lower())

        for joukkue in jarjestetytJoukkueet:
            laskeAika(joukkue)
            
        return Response(json.dumps(jarjestetytJoukkueet), mimetype="application/json")

    except Exception as e:
        print("eitoimi100")
        return Response(json.dumps({"error": f"joukkueiden järjestäminen epäonnistui: {str(e)}"}), mimetype="application/json"), 400
        



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






