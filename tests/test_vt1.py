#viikkotehtävä 1:n kokeellisia testejä
#parantele näitä tarpeen mukaan
import json

def test_vt1(client):
    response = client.get("/vt1")
    assert 200 == response.status_code, 'Sovelluksen aloitussivu ei toimi'

def test_jarjestaLeimaustavat(client):
    #kelvollinen data
    global data
    url = "/jarjestaLeimaustavat"

    leimaustavat = {"ltavat": json.dumps(data["leimaustavat"])}
    response = client.post(url, data=leimaustavat)
    #jos tulee virhekoodi, ei tarkisteta pitemmälle
    assert 200 == response.status_code, "Kaatuu heti"
    assert b'["GPS", "Lomake", "NFC", "QR"]' == response.data, 'Leimaustavat eivät ole järjestyksessä : ' + response.data.decode("UTF-8")

    leimaustavat = {"ltavat": json.dumps(["gps", "LOMAKE", " nfc", "QR"])}
    response = client.post(url, data=leimaustavat)
    assert b'["gps", "LOMAKE", " nfc", "QR"]' == response.data, "Järjestäminen ei ole caseinsensitive eikä huomioi alussa olevaa whitespacea : " + response.data.decode("UTF-8")

    #kokeillaan kaatuuko post-requestiin ilman parametreja
    response = client.post(url)
    assert 400 == response.status_code, 'Kaatuu POST-requestissa, jos leimaustapoja ei ole annettu' 

    #kokeillaan kaatuuko get-requestiin ilman parametreja
    response = client.get(url)
    assert 400 == response.status_code, 'Kaatuu GET-requestissa'


def test_jarjestaSarjat(client):
    #kelvollinen data
    global data
    sarjat = {"sarjat": json.dumps(data["sarjat"])}
    url = "/jarjestaSarjat"
    response = client.post(url, data=sarjat)
    assert 200 == response.status_code, "Kaatuu kelvollisilla parametreillakin"
    #kokeillaan kaatuuko post-requestiin ilman parametreja
    response = client.post(url)
    assert 400 == response.status_code, 'Kaatuu POST-requestissa, jos sarjoja ei ole annettu' 
    #kokeillaan kaatuuko get-requestiin ilman parametreja
    response = client.get(url)
    assert 400 == response.status_code, 'Kaatuu GET-requestissa'
    #todo: pitäisi testata oikealla data


def test_lisaaSarja(client):
    #kelvollinen data
    global data
    url = "/lisaaSarja"

    reqdata = {
        "sarjalista": json.dumps(data["sarjat"]),
        "nimi": "foobar",
        "kesto": "10",
        "alkuaika": "2023-01-01 10:30:30",
        "loppuaika": "2023-02-01 10:00:00"
    }
    response = client.post(url, data=reqdata)
#    assert 200 == response.status_code or 400 == response.status_code or 422 == response.status_code, "HTTP-koodia on väärä eli ei ole 200, 400 tai 422"
    assert response.status_code in (200, 400, 422), "Väärä http-status, pitäisi olla 200 tai 422 : " +  response.data.decode("UTF-8")
    if response.status_code == 200:
        assert len(data["sarjat"]) != len(json.loads(response.data.decode("UTF-8"))), "Lisäystä ei tehty : " + response.data.decode("UTF-8")

    reqdata = {
        "sarjalista": json.dumps(data["sarjat"]),
        "nimi": "foobar",
        "kesto": "10",
        "alkuaika": "2023-01-01 10f",
        "loppuaika": "2023-02-00:00:00"
    }
    response = client.post(url, data=reqdata)
    assert 422 == response.status_code, "Kaatuu, jos alkuaika tai loppuaika on väärää muotoa"

    reqdata = {
        "sarjalista": json.dumps(data["sarjat"]),
        "nimi": "   ",
        "kesto": "10",
        "alkuaika": "2023-01-01 10:30:00",
        "loppuaika": "2023-02-01 10:00:00"
    }
    response = client.post(url, data=reqdata)
    assert response.status_code in (200, 400, 422), "Väärä http-status, pitäisi olla 200 tai 422 : " +  response.data.decode("UTF-8")
    if response.status_code == 200:
        assert len(data["sarjat"]) == len( json.loads(response.data.decode("UTF-8"))) , "Lisäys tehtiin vaikka sarjan nimi on pelkkää whitespacea : " + response.data.decode("UTF-8")

    reqdata = {
        "sarjalista": json.dumps(data["sarjat"]),
        "nimi": "foobar",
        "kesto": "a",
        "alkuaika": "2023-01-01 10:30:00",
        "loppuaika": "2023-02-01 10:00:00"
    }
    response = client.post(url, data=reqdata)
    assert 422 == response.status_code, "Kaatuu, jos kesto ei olekkaan numero"

    reqdata = {
        "sarjalista": json.dumps(data["sarjat"]),
        "nimi": "foobar",
        "kesto": "10",
        "alkuaika": "2023-03-01 10:30:00",
        "loppuaika": "2023-02-01 10:00:00"
    }
    response = client.post(url, data=reqdata)
    assert response.status_code in (200, 400, 422), "Väärä http-status, pitäisi olla 200 tai 422 : " +  response.data.decode("UTF-8")
    if response.status_code == 200:
        assert len(data["sarjat"]) == len( json.loads(response.data.decode("UTF-8"))) , "Lisäys tehtiin vaikka alkuaika on loppuajan jälkeen : " + response.data.decode("UTF-8")


    reqdata = {
        "sarjalista": json.dumps(data["sarjat"]),
        "nimi": "2H",
        "kesto": "10",
        "alkuaika": "2023-01-01 10:30:00",
        "loppuaika": "2023-02-01 10:00:00"
    }
    response = client.post(url, data=reqdata)
    assert response.status_code in (200, 400, 422), "Väärä http-status, pitäisi olla 200 tai 422 : " +  response.data.decode("UTF-8")
    if response.status_code == 200:
        assert len(data["sarjat"]) == len( json.loads(response.data.decode("UTF-8"))) , "Lisäys tehtiin vaikka samanniminen sarja löytyy : 2H"

    reqdata = {
        "sarjalista": json.dumps(data["sarjat"]),
        "nimi": "foofoo",
        "kesto": "-5",
        "alkuaika": "2023-01-01 10:30:00",
        "loppuaika": "2023-02-01 10:00:00"
    }
    response = client.post(url, data=reqdata)
    assert response.status_code in (200, 400, 422), "Väärä http-status, pitäisi olla 200 tai 422 : " +  response.data.decode("UTF-8")
    if response.status_code == 200:
        assert len(data["sarjat"]) == len( json.loads(response.data.decode("UTF-8"))) , "Lisäys tehtiin vaikka kesto on negatiivinen luku : -5"

    reqdata = {
        "sarjalista": json.dumps(data["sarjat"]),
        "nimi": "foofoo",
        "kesto": "0",
        "alkuaika": "2023-01-01 10:30:00",
        "loppuaika": "2023-02-01 10:00:00"
    }
    response = client.post(url, data=reqdata)
    assert response.status_code in (200, 400, 422), "Väärä http-status, pitäisi olla 200 tai 422 : " +  response.data.decode("UTF-8")
    if response.status_code == 200:
        assert len(data["sarjat"]) == len( json.loads(response.data.decode("UTF-8"))) , "Lisäys tehtiin vaikka kesto on nolla"


    #lisätään useampi
    reqdata = {
        "sarjalista": json.dumps(data["sarjat"]),
        "nimi": "foofoo",
        "kesto": "1",
        "alkuaika": "2023-01-01 10:30:00",
        "loppuaika": "2023-02-01 10:00:00"
    }
    response = client.post(url, data=reqdata)
    sarjat = response.data.decode("UTF-8")
    reqdata = {
        "sarjalista": sarjat,
        "nimi": "foofoo1",
        "kesto": "1",
        "alkuaika": "2023-01-01 10:30:00",
        "loppuaika": "2023-02-01 10:00:00"
    }
    response = client.post(url, data=reqdata)
    sarjat = response.data.decode("UTF-8")
    reqdata = {
        "sarjalista": sarjat,
        "nimi": "foofoo2",
        "kesto": "1",
        "alkuaika": "2023-01-01 10:30:00",
        "loppuaika": "2023-02-01 10:00:00"
    }
    response = client.post(url, data=reqdata)
    return
    sarjat = json.loads(response.data.decode("UTF-8"))
    idt = set()
    for s in sarjat:
#       try:
          idt.add(s["id"])
#       except KeyError:
    assert len(idt) == len( sarjat ) , "Sarjoilla ei ole kaikilla uniikki id"

    #kokeillaan kaatuuko post-requestiin ilman parametreja
    response = client.post(url)
    assert 400 == response.status_code, 'Kaatuu tyhjällä POST-requestilla. Pitäisi palauttaa 400 ja virheilmo' 
    #kokeillaan kaatuuko get-requestiin ilman parametreja
    response = client.get(url)
    assert 400 == response.status_code, 'Kaatuu GET-requestissa. Pitäisi palauttaa 400 ja virheilmo'

    #todo:
    #uniikki id
    #onko kesto nollaa suurempi kokonaisluku


def test_jarjestaRastit(client):
    #kelvollinen data
    global data
    url = "/jarjestaRastit"

    reqdata = {
        "rastit": json.dumps(data["rastit"])
    }
    response = client.post(url, data=reqdata)
    assert 200 == response.status_code, 'Kaatuu heti'
    rastit = json.loads(response.data.decode("UTF-8"))
    assert rastit[0]["koodi"][0].isnumeric() == False, "Rastit eivät ole oikeassa järjestyksessä. Ensimmäisen rastin koodi alkaa numerolla : " + rastit[0]["koodi"]
    assert rastit[len(rastit)-1]["koodi"][0].isnumeric(), "Rastit eivät ole oikeassa järjestyksessä. Viimeisen rastin koodi ei ala numerolla : " + rastit[len(rastit)-1]["koodi"]

def test_lisaaJoukkue(client):
    #kelvollinen data
    global data
    url = "/lisaaJoukkue"

    reqdata = {
        "data": json.dumps(data),
        "nimi": "   ",
        "leimaustavat": json.dumps(["GPS", "NFC"]),
        "sarja": 12345679,
        "jasenet": json.dumps(["foo","bar"])
    }
    response = client.post(url, data=reqdata)

#    assert 422 == response.status_code or 200 == response.status_code, 'lisaaJoukkue kaatuu heti : ' + response.data.decode("UTF-8")
    assert response.status_code in (200, 400, 422), "Väärä http-status, pitäisi olla 200 tai 422 : " +  response.data.decode("UTF-8")
    if response.status_code == 200:
        assert len(data["joukkueet"]) == len( json.loads(response.data.decode("UTF-8"))["joukkueet"]) , "Lisäys tehdään vaikka joukkueen nimi on pelkkää whitespacea"


    reqdata = {
        "data": json.dumps(data),
        "nimi": "testijoukkue",
        "leimaustavat": json.dumps(["GPS", "NFC"]),
        "sarja": 12345679,
        "jasenet": json.dumps(["foo","bar"])
    }
    response = client.post(url, data=reqdata)
    assert response.status_code in (200, 400, 422), "Väärä http-status, pitäisi olla 200 tai 422 : " +  response.data.decode("UTF-8")
    if response.status_code == 200:
        assert len(data["joukkueet"]) != len( json.loads(response.data.decode("UTF-8"))["joukkueet"]) , "Joukkueen lisäystä ei tehty : " + str( len(data["joukkueet"])) + " joukkuetta vs " + str(len(json.loads(response.data.decode("UTF-8"))["joukkueet"])) + " joukkuetta"

    reqdata = {
        "data": json.dumps(data),
        "nimi": "testijoukkue",
        "leimaustavat": "foo",
        "sarja": "a",
        "jasenet": "ei toimi"
    }
    response = client.post(url, data=reqdata)
    assert 400 == response.status_code, 'lisaaJoukkue kaatuu, jos parametrit ovat väärää muotoa ' + response.data.decode("UTF-8")


def test_jarjestaJoukkueet(client):
    #kelvollinen data
    global data
    url = "/jarjestaJoukkueet"
    pass

def test_laskeAika(client):
    #kelvollinen data
    global data
    url = "/jarjestaJoukkueet"
    sortorder = [
               {"key": "sarja", "order": 1, "numeric": False},
              {"key": "nimi", "order": 1, "numeric": False},
                               {"key": "matka", "order": -1, "numeric": True},
                                       {"key": "aika", "order": 1, "numeric": False},
                                               {"key": "pisteet", "order": -1, "numeric": True}
                                                      ]
    reqdata = {
        "joukkueet": json.dumps(data["joukkueet"]),
        "mainsort": json.dumps("nimi"),
        "sortorder": json.dumps(sortorder),
        "leimaustavat": json.dumps(data["leimaustavat"]),
        "rastit": json.dumps(data["rastit"]),
        "sarjat": json.dumps(data["sarjat"])
    }
    response = client.post(url, data=reqdata)
    assert 200 == response.status_code    , 'jarjestaJoukkueet kaatuu heti' + response.data.decode("UTF-8")
    assert "05:01:05" in response.data.decode("UTF-8"), "Sopupelin aika on väärä " + response.data.decode("UTF-8")
    assert '"pisteet":59' in response.data.decode("UTF-8").replace(" ", ""), "Sopupelin pisteet ovat väärin " + response.data.decode("UTF-8")
    assert '"pisteet":273' in response.data.decode("UTF-8").replace(" ", ""), "Onnenonkijoiden pisteet ovat väärin " + response.data.decode("UTF-8")
    assert '"matka":13' in response.data.decode("UTF-8").replace(" ", ""), "Sopupelin matka on väärä " + response.data.decode("UTF-8")



#testiversio datasta
data = {
  "rastit": {
    "9": {
      "koodi": "JE3", "lat": "62.109962", "lon": "25.669574"
    },
    "10": {
      "koodi": "JI70", "lat": "62.149572", "lon": "25.590916"
    },
    "11": {
      "koodi": "FP58", "lat": "62.109962", "lon": "25.704639"
    },
    "12": {
      "koodi": "32VE", "lat": "62.156431", "lon": "25.628636"
    },
    "4554615953555456": {
      "lon": "25.542413", "koodi": "66", "lat": "62.120776"
    },
    "4613241183404032": {
      "lon": "25.496872", "koodi": "6D", "lat": "62.156532"
    },
    "4642982221316096": {
      "lon": "25.714338", "koodi": "91", "lat": "62.112172"
    },
    "4669246617419776": {
      "lon": "25.544984", "koodi": "48", "lat": "62.099795"
    },
    "4685962630135808": {
      "lon": "25.737019", "koodi": "31", "lat": "62.133029"
    },
    "4741461794881536": {
      "lon": "25.518665", "koodi": "85", "lat": "62.110562"
    },
    "4750123938611200": {
      "lon": "25.615203", "koodi": "69", "lat": "62.115047"
    },
    "4763145205710848": {
      "lon": "25.729848", "koodi": "99", "lat": "62.088183"
    },
    "4771528579219456": {
      "lon": "25.644512", "koodi": "60", "lat": "62.111830"
    },
    "4794764486508544": {
      "lon": "25.618079", "koodi": "63", "lat": "62.148123"
    },
    "4810425279447040": {
      "lon": "25.605762", "koodi": "70", "lat": "62.134681"
    },
    "4821274903707648": {
      "lon": "25.666688", "koodi": "LAHTO", "lat": "62.130280"
    },
    "4828368713285632": {
      "lon": "25.635950", "koodi": "90", "lat": "62.103930"
    },
    "4854848931495936": {
      "lon": "25.573049", "koodi": "34", "lat": "62.122986"
    },
    "4875454842404864": {
      "lon": "25.628228", "koodi": "37", "lat": "62.119060"
    },
    "4894820447289344": {
      "lon": "25.652877", "koodi": "5C", "lat": "62.089674"
    },
    "4913030705971200": {
      "lon": "25.626533", "koodi": "44", "lat": "62.129767"
    },
    "4928404407189504": {
      "lon": "25.695688", "koodi": "79", "lat": "62.086189"
    },
    "4967437606846464": {
      "lon": "25.597278", "koodi": "82", "lat": "62.127323"
    },
    "4985069521338368": {
      "lon": "25.628236", "koodi": "64", "lat": "62.095187"
    },
    "5064464005070848": {
      "lon": "25.509358", "koodi": "6F", "lat": "62.141243"
    },
    "5076239463219200": {
      "lon": "25.668097", "koodi": "41", "lat": "62.136462"
    },
    "5091900256157696": {
      "lon": "25.540227", "koodi": "40", "lat": "62.153864"
    },
    "5102749880418304": {
      "lon": "25.673997", "koodi": "5A", "lat": "62.102194"
    },
    "5176191136825344": {
      "lon": "25.493141", "koodi": "92", "lat": "62.144852"
    },
    "5179900512174080": {
      "lon": "25.718561", "koodi": "5B", "lat": "62.118784"
    },
    "5209879383900160": {
      "lon": "25.678314", "koodi": "49", "lat": "62.121247"
    },
    "5232196570841088": {
      "lon": "25.553191", "koodi": "78", "lat": "62.111294"
    },
    "5248912583557120": {
      "lon": "25.691051", "koodi": "56", "lat": "62.098636"
    },
    "5266544498049024": {
      "lon": "25.733259", "koodi": "42", "lat": "62.078212"
    },
    "5313972748156928": {
      "lon": "25.535011", "koodi": "67", "lat": "62.139918"
    },
    "5334478532640768": {
      "lon": "25.562520", "koodi": "7C", "lat": "62.138397"
    },
    "5357714439929856": {
      "lon": "25.680401", "koodi": "96", "lat": "62.091567"
    },
    "5373190012403712": {
      "lon": "25.498431", "koodi": "53", "lat": "62.132320"
    },
    "5373375232868352": {
      "lon": "25.577610", "koodi": "95", "lat": "62.132964"
    },
    "5417798884917248": {
      "lon": "25.590916", "koodi": "76", "lat": "62.142319"
    },
    "5445149236658176": {
      "lon": "25.507110", "koodi": "46", "lat": "62.151460"
    },
    "5466832647487488": {
      "lon": "25.704639", "koodi": "58", "lat": "62.126591"
    },
    "5475980659392512": {
      "lon": "25.665822", "koodi": "83", "lat": "62.147298"
    },
    "5528034857713664": {
      "lon": "25.558017", "koodi": "51", "lat": "62.125561"
    },
    "5548019474759680": {
      "lon": "25.671071", "koodi": "97", "lat": "62.087827"
    },
    "5557775895625728": {
      "lon": "25.563169", "koodi": "5E", "lat": "62.147942"
    },
    "5627413958492160": {
      "lon": "25.649234", "koodi": "94", "lat": "62.124222"
    },
    "5665699833839616": {
      "lon": "25.586932", "koodi": "47", "lat": "62.100104"
    },
    "5680515860398080": {
      "lon": "25.528730", "koodi": "74", "lat": "62.153364"
    },
    "5720036136189952": {
      "lon": "25.522034", "koodi": "73", "lat": "62.099512"
    },
    "5739141090246656": {
      "lon": "25.750133", "koodi": "7B", "lat": "62.126639"
    },
    "5795146524262400": {
      "lon": "25.718473", "koodi": "6A", "lat": "62.141674"
    },
    "5811862536978432": {
      "lon": "25.613440", "koodi": "43", "lat": "62.107914"
    },
    "5844366849474560": {
      "lon": "25.716227", "koodi": "71", "lat": "62.093545"
    },
    "5876023845453824": {
      "lon": "25.565572", "koodi": "77", "lat": "62.101185"
    },
    "5876922701578240": {
      "lon": "25.560594", "koodi": "33", "lat": "62.153435"
    },
    "5897428486062080": {
      "lon": "25.647515", "koodi": "6E", "lat": "62.094680"
    },
    "5920664393351168": {
      "lon": "25.728135", "koodi": "80", "lat": "62.100413"
    },
    "5936325186289664": {
      "lon": "25.540316", "koodi": "7E", "lat": "62.131251"
    },
    "5980748838338560": {
      "lon": "25.597308", "koodi": "68", "lat": "62.149572"
    },
    "6001354749247488": {
      "lon": "25.682473", "koodi": "7A", "lat": "62.134123"
    },
    "6020720354131968": {
      "lon": "25.728800", "koodi": "89", "lat": "62.109962"
    },
    "6029782600908800": {
      "lon": "25.569589", "koodi": "45", "lat": "62.115924"
    },
    "6038930612813824": {
      "lon": "25.523811", "koodi": "57", "lat": "62.135094"
    },
    "6090984811134976": {
      "lon": "25.513792", "koodi": "38", "lat": "62.147825"
    },
    "6110969428180992": {
      "lon": "25.668757", "koodi": "81", "lat": "62.113906"
    },
    "6120725849047040": {
      "lon": "25.628636", "koodi": "50", "lat": "62.141654"
    },
    "6190363911913472": {
      "lon": "25.686679", "koodi": "7D", "lat": "62.081466"
    },
    "6202139370061824": {
      "lon": "25.589347", "koodi": "54", "lat": "62.108717"
    },
    "6214128637050880": {
      "lon": "25.645642", "koodi": "72", "lat": "62.146315"
    },
    "6217800163000320": {
      "lon": "25.732937", "koodi": "62", "lat": "62.095246"
    },
    "6228649787260928": {
      "lon": "25.576022", "koodi": "86", "lat": "62.149229"
    },
    "6235743596838912": {
      "lon": "25.531059", "koodi": "5D", "lat": "62.123662"
    },
    "6305800419016704": {
      "lon": "25.526039", "koodi": "88", "lat": "62.142258"
    },
    "6320405589524480": {
      "lon": "25.694017", "koodi": "32", "lat": "62.144101"
    },
    "6335779290742784": {
      "lon": "25.496020", "koodi": "6B", "lat": "62.125632"
    },
    "6358096477683712": {
      "lon": "25.669574", "koodi": "MAALI", "lat": "62.131769"
    },
    "6374812490399744": {
      "lon": "25.743788", "koodi": "65", "lat": "62.115241"
    },
    "6392444404891648": {
      "lon": "25.606234", "koodi": "55", "lat": "62.093203"
    },
    "6439872654999552": {
      "lon": "25.694911", "koodi": "75", "lat": "62.117266"
    },
    "6460378439483392": {
      "lon": "25.519131", "koodi": "93", "lat": "62.156431"
    },
    "6471838888624128": {
      "lon": "25.531926", "koodi": "61", "lat": "62.147942"
    },
    "6498833966039040": {
      "lon": "25.724837", "koodi": "36", "lat": "62.128162"
    },
    "6529450237755392": {
      "lon": "25.524245", "koodi": "39", "lat": "62.118778"
    },
    "6571049143500800": {
      "lon": "25.503483", "koodi": "59", "lat": "62.115914"
    },
    "6579711287230464": {
      "lon": "25.648821", "koodi": "35", "lat": "62.140919"
    },
    "6592732554330112": {
      "lon": "25.661916", "koodi": "84", "lat": "62.094023"
    },
    "6601115927838720": {
      "lon": "25.599044", "koodi": "52", "lat": "62.120424"
    },
    "6601880566235136": {
      "lon": "25.650436", "koodi": "98", "lat": "62.131207"
    },
    "6653934764556288": {
      "lon": "25.674748", "koodi": "5F", "lat": "62.127514"
    },
    "6683675802468352": {
      "lon": "25.687644", "koodi": "6C", "lat": "62.107580"
    }
  },
  "nimi": "Jäärogaining", "loppuaika": "2017-03-18 20:00:00", "kesto": 
  8, "alkuaika": "2017-03-18 09:00:00", "sarjat": [
    {
      "nimi": "4h", "kesto": 4, "loppuaika": None, "alkuaika": None, 
      "id": 12345678
    },
    {
      "nimi": "2h", "kesto": 2, "loppuaika": None, "alkuaika": None, 
      "id": 12345679
    },
    {
      "nimi": "8h", "kesto": 8, "loppuaika": None, "alkuaika": None, 
      "id": 12345680
    }
  ], "leimaustavat": [
    "QR", "GPS", "NFC", "Lomake" ], "joukkueet": [ {
      "nimi": "Onnenonkijat", "jasenet": [
        "Raimo Laine", "Pekka Paununen", "Antero Paununen" ], "pisteet": 
      0, "matka": 0, "aika": "00:00:00", "id": 470736, 
      "rastileimaukset": [
        {
          "aika": "2017-03-18 16:13:32", "rasti": "6202139370061824"
        },
        {
          "aika": "2017-03-18 15:20:17", "rasti": "6335779290742784"
        },
        {
          "aika": "2017-03-18 14:31:50", "rasti": "6090984811134976"
        },
        {
          "aika": "2017-03-18 12:11:15", "rasti": 6601880566235136
        },
        {
          "aika": "2017-03-18 18:32:27", "rasti": "6374812490399744"
        },
        {
          "aika": "2017-03-18 18:49:05", "rasti": "4685962630135808"
        },
        {
          "aika": "2017-03-18 12:33:51", "rasti": "4810425279447040"
        },
        {
          "aika": "2017-03-18 19:24:23", "rasti": "6001354749247488"
        },
        {
          "aika": "2017-03-18 16:40:19", "rasti": "5627413958492160"
        },
        {
          "aika": "2017-03-18 15:11:48", "rasti": "5373190012403712"
        },
        {
          "aika": "2017-03-18 15:44:27", "rasti": "4554615953555456"
        },
        {
          "aika": "2017-03-18 18:25:52", "rasti": "6020720354131968"
        },
        {
          "aika": "2017-03-18 13:11:37", "rasti": "4854848931495936"
        },
        {
          "aika": "2017-03-18 14:21:36", "rasti": "6460378439483392"
        },
        {
          "aika": "2017-03-18 16:58:02", "rasti": "4771528579219456"
        },
        {
          "aika": "2017-03-18 12:33:39", "rasti": "4810425279447040"
        },
        {
          "aika": "2017-03-18 13:47:11", "rasti": "5313972748156928"
        },
        {
          "aika": "2017-03-18 15:36:43", "rasti": "6235743596838912"
        },
        {
          "aika": "2017-03-18 18:09:59", "rasti": "5844366849474560"
        },
        {
          "aika": "2017-03-18 17:31:13", "rasti": "5102749880418304"
        },
        {
          "aika": "2017-03-18 15:36:40", "rasti": "6235743596838912"
        },
        {
          "aika": "2017-03-18 16:40:25", "rasti": "5627413958492160"
        },
        {
          "aika": "2017-03-18 15:20:35", "rasti": "6335779290742784"
        },
        {
          "aika": "2017-03-18 16:13:31", "rasti": "6202139370061824"
        },
        {
          "aika": "2017-03-18 18:49:01", "rasti": "4685962630135808"
        },
        {
          "aika": "2017-03-18 18:32:23", "rasti": "6374812490399744"
        },
        {
          "aika": "2017-03-18 14:28:02", "rasti": "5445149236658176"
        },
        {
          "aika": "2017-03-18 16:27:35", "rasti": "4875454842404864"
        },
        {
          "aika": "2017-03-18 12:49:06", "rasti": "4967437606846464"
        },
        {
          "aika": "2017-03-18 13:52:26", "rasti": "6305800419016704"
        },
        {
          "aika": "2017-03-18 18:41:38", "rasti": "5739141090246656"
        },
        {
          "aika": "2017-03-18 13:52:48", "rasti": "6305800419016704"
        },
        {
          "aika": "2017-03-18 14:21:38", "rasti": "6460378439483392"
        },
        {
          "aika": "2017-03-18 14:53:39", "rasti": "5176191136825344"
        },
        {
          "aika": "2017-03-18 17:40:42", "rasti": "5248912583557120"
        },
        {
          "aika": "2017-03-18 18:59:25", "rasti": "5795146524262400"
        },
        {
          "aika": "2017-03-18 19:49:07", "rasti": "5076239463219200"
        },
        {
          "aika": "2017-03-18 18:18:29", "rasti": "5920664393351168"
        },
        {
          "aika": "2017-03-18 18:02:34", "rasti": "4763145205710848"
        },
        {
          "aika": "2017-03-18 11:56:54", "rasti": 4821274903707648
        },
        {
          "aika": "2017-03-18 12:23:54", "rasti": "4913030705971200"
        },
        {
          "aika": "2017-03-18 18:59:27", "rasti": "5795146524262400"
        },
        {
          "aika": "2017-03-18 12:00:00", "rasti": 4821274903707648
        },
        {
          "aika": "2017-03-18 13:11:34", "rasti": "4854848931495936"
        },
        {
          "aika": "2017-03-18 18:42:05", "rasti": "5739141090246656"
        },
        {
          "aika": "2017-03-18 19:12:18", "rasti": "5466832647487488"
        },
        {
          "aika": "2017-03-18 16:22:36", "rasti": "4750123938611200"
        },
        {
          "aika": "2017-03-18 17:50:21", "rasti": "4928404407189504"
        },
        {
          "aika": "2017-03-18 14:37:34", "rasti": "5064464005070848"
        },
        {
          "aika": "2017-03-18 14:00:45", "rasti": "6471838888624128"
        },
        {
          "aika": "2017-03-18 14:37:40", "rasti": "5064464005070848"
        },
        {
          "aika": "2017-03-18 13:24:51", "rasti": "5528034857713664"
        },
        {
          "aika": "2017-03-18 14:31:53", "rasti": "6090984811134976"
        },
        {
          "aika": "2017-03-18 18:10:02", "rasti": "5844366849474560"
        },
        {
          "aika": "2017-03-18 14:05:53", "rasti": "5091900256157696"
        },
        {
          "aika": "2017-03-18 18:25:55", "rasti": "6020720354131968"
        },
        {
          "aika": "2017-03-18 16:22:30", "rasti": "4750123938611200"
        },
        {
          "aika": "2017-03-18 15:11:40", "rasti": "5373190012403712"
        },
        {
          "aika": "2017-03-18 15:11:49", "rasti": "5373190012403712"
        },
        {
          "aika": "2017-03-18 14:13:26", "rasti": "5680515860398080"
        },
        {
          "aika": "2017-03-18 18:18:16", "rasti": "5920664393351168"
        },
        {
          "aika": "2017-03-18 17:50:36", "rasti": "4928404407189504"
        },
        {
          "aika": "2017-03-18 13:46:59", "rasti": "5313972748156928"
        },
        {
          "aika": "2017-03-18 16:58:08", "rasti": "4771528579219456"
        },
        {
          "aika": "2017-03-18 18:02:37", "rasti": "4763145205710848"
        },
        {
          "aika": "2017-03-18 16:00:08", "rasti": "5232196570841088"
        },
        {
          "aika": "2017-03-18 19:35:11", "rasti": "6653934764556288"
        },
        {
          "aika": "2017-03-18 12:23:57", "rasti": "4913030705971200"
        },
        {
          "aika": "2017-03-18 19:52:32", "rasti": "6358096477683712"
        },
        {
          "aika": "2017-03-18 16:27:35", "rasti": "4875454842404864"
        },
        {
          "aika": "2017-03-18 14:00:25", "rasti": "6471838888624128"
        },
        {
          "aika": "2017-03-18 14:05:52", "rasti": "5091900256157696"
        },
        {
          "aika": "2017-03-18 19:12:10", "rasti": "5466832647487488"
        },
        {
          "aika": "2017-03-18 17:40:56", "rasti": "5248912583557120"
        },
        {
          "aika": "2017-03-18 13:41:35", "rasti": "5936325186289664"
        },
        {
          "aika": "2017-03-18 16:00:23", "rasti": "5232196570841088"
        },
        {
          "aika": "2017-03-18 17:31:00", "rasti": "5102749880418304"
        },
        {
          "aika": "2017-03-18 17:09:41", "rasti": "4828368713285632"
        },
        {
          "aika": "2017-03-18 13:02:51", "rasti": "5373375232868352"
        },
        {
          "aika": "2017-03-18 13:02:38", "rasti": "5373375232868352"
        },
        {
          "aika": "2017-03-18 15:44:09", "rasti": "4554615953555456"
        },
        {
          "aika": "2017-03-18 12:49:24", "rasti": "4967437606846464"
        },
        {
          "aika": "2017-03-18 12:11:14", "rasti": 6601880566235136
        },
        {
          "aika": "2017-03-18 14:27:59", "rasti": "5445149236658176"
        }
      ], "leimaustapa": [
        2 ], "sarja": 12345680
    },
    {
      "nimi": "hullut fillaristit", "jasenet": [
        "Hannele Saari", "Paula Kujala" ], "pisteet": 0, "matka": 0, 
      "aika": "00:00:00", "id": 342249, "rastileimaukset": [
        {
          "aika": "2017-03-18 14:17:29", "rasti": "4763145205710848"
        },
        {
          "aika": "2017-03-18 14:40:52", "rasti": "5248912583557120"
        },
        {
          "aika": "2017-03-18 14:02:47", "rasti": "5920664393351168"
        },
        {
          "aika": "2017-03-18 13:14:05", "rasti": "6001354749247488"
        },
        {
          "aika": "2017-03-18 14:27:23", "rasti": "4928404407189504"
        },
        {
          "aika": "2017-03-18 13:53:30", "rasti": "6020720354131968"
        },
        {
          "aika": "2017-03-18 13:06:42", "rasti": "4821274903707648"
        },
        {
          "aika": "2017-03-18 14:11:59", "rasti": "5844366849474560"
        },
        {
          "aika": "2017-03-18 13:36:38", "rasti": "6498833966039040"
        },
        {
          "aika": "2017-03-18 13:47:56", "rasti": "6374812490399744"
        },
        {
          "aika": "2017-03-18 15:19:30", "rasti": "6358096477683712"
        },
        {
          "aika": "2017-03-18 13:25:31", "rasti": "5466832647487488"
        },
        {
          "aika": "2017-03-18 14:50:05", "rasti": "5102749880418304"
        }
      ], "leimaustapa": [
        2, 1 ], "sarja": 12345679
    },
    {
      "nimi": "Vapaat", "jasenet": [
        "Juha Vapaa", "Matti Vapaa" ], "id": 207312, "matka": 0, "aika": 
      "00:00:00", "pisteet": 0, "rastileimaukset": [
        {
          "aika": "2017-03-18 14:37:43", "rasti": 4771528579219456
        },
        {
          "aika": "2017-03-18 13:16:31", "rasti": 4967437606846464
        },
        {
          "aika": "2017-03-18 14:10:07", "rasti": 6202139370061824
        },
        {
          "aika": "2017-03-18 12:19:47", "rasti": 6601880566235136
        },
        {
          "aika": "2017-03-18 15:19:44", "rasti": 5209879383900160
        },
        {
          "aika": "2017-03-18 12:06:42", "rasti": 5076239463219200
        },
        {
          "aika": "2017-03-18 12:19:31", "rasti": 6601880566235136
        },
        {
          "aika": "2017-03-18 13:28:52", "rasti": 4810425279447040
        },
        {
          "aika": "2017-03-18 12:53:37", "rasti": 6601115927838720
        },
        {
          "aika": "2017-03-18 13:29:28", "rasti": 4810425279447040
        },
        {
          "aika": "2017-03-18 12:00:00", "rasti": 4821274903707648
        },
        {
          "aika": "2017-03-18 12:32:22", "rasti": 5627413958492160
        },
        {
          "aika": "2017-03-18 14:29:23", "rasti": 4828368713285632
        },
        {
          "aika": "2017-03-18 15:49:04", "rasti": 6653934764556288
        },
        {
          "aika": "2017-03-18 14:18:27", "rasti": 5811862536978432
        },
        {
          "aika": "2017-03-18 15:10:55", "rasti": 6439872654999552
        },
        {
          "aika": "2017-03-18 15:40:37", "rasti": 6001354749247488
        },
        {
          "aika": "2017-03-18 14:55:38", "rasti": 6110969428180992
        },
        {
          "aika": "2017-03-18 12:40:24", "rasti": 4875454842404864
        },
        {
          "aika": "2017-03-18 15:56:06", "rasti": 6358096477683712
        },
        {
          "aika": "2017-03-18 13:47:17", "rasti": 4854848931495936
        },
        {
          "aika": "2017-03-18 15:31:41", "rasti": 5466832647487488
        },
        {
          "aika": "2017-03-18 12:45:36", "rasti": 4750123938611200
        },
        {
          "aika": "2017-03-18 13:36:57", "rasti": 5373375232868352
        }
      ], "leimaustapa": [
        2, 1 ], "sarja": 12345678
    },
    {
      "nimi": "Kahden joukkue", "jasenet": [
        "Matti Humppa", "Miikka Talvinen" ], "pisteet": 0, "matka": 0, 
      "aika": "00:00:00", "id": 381916, "rastileimaukset": [
        {
          "aika": "2017-03-18 19:58:57", "rasti": "6601880566235136"
        },
        {
          "aika": "2017-03-18 20:05:38", "rasti": "6358096477683712"
        },
        {
          "aika": "2017-03-18 19:06:17", "rasti": "4967437606846464"
        },
        {
          "aika": "2017-03-18 14:21:47", "rasti": "4763145205710848"
        },
        {
          "aika": "2017-03-18 12:50:57", "rasti": "4642982221316096"
        },
        {
          "aika": "2017-03-18 16:28:04", "rasti": "4771528579219456"
        },
        {
          "aika": "2017-03-18 18:18:09", "rasti": "5091900256157696"
        },
        {
          "aika": "2017-03-18 14:01:00", "rasti": "6020720354131968"
        },
        {
          "aika": "2017-03-18 17:47:48", "rasti": "5064464005070848"
        },
        {
          "aika": "2017-03-18 13:24:48", "rasti": "6498833966039040"
        },
        {
          "aika": "2017-03-18 16:49:01", "rasti": "4750123938611200"
        },
        {
          "aika": "2017-03-18 14:10:15", "rasti": "5920664393351168"
        },
        {
          "aika": "2017-03-18 14:58:46", "rasti": "5102749880418304"
        },
        {
          "aika": "2017-03-18 17:21:37", "rasti": "4554615953555456"
        },
        {
          "aika": "2017-03-18 15:35:40", "rasti": "5548019474759680"
        },
        {
          "aika": "2017-03-18 18:21:53", "rasti": "5876922701578240"
        },
        {
          "aika": "2017-03-18 14:47:25", "rasti": "5248912583557120"
        },
        {
          "aika": "2017-03-18 14:37:44", "rasti": "4928404407189504"
        },
        {
          "aika": "2017-03-18 12:00:00", "rasti": 4821274903707648
        },
        {
          "aika": "2017-03-18 19:48:36", "rasti": "5627413958492160"
        },
        {
          "aika": "2017-03-18 17:42:42", "rasti": "6305800419016704"
        },
        {
          "aika": "2017-03-18 13:42:18", "rasti": "4685962630135808"
        },
        {
          "aika": "2017-03-18 12:20:59", "rasti": "6110969428180992"
        },
        {
          "aika": "2017-03-18 18:52:13", "rasti": "4810425279447040"
        },
        {
          "aika": "2017-03-18 14:33:39", "rasti": "6190363911913472"
        },
        {
          "aika": "2017-03-18 18:39:29", "rasti": "5373375232868352"
        },
        {
          "aika": "2017-03-18 13:24:52", "rasti": "6498833966039040"
        },
        {
          "aika": "2017-03-18 19:36:12", "rasti": "4875454842404864"
        },
        {
          "aika": "2017-03-18 13:35:28", "rasti": "5795146524262400"
        },
        {
          "aika": "2017-03-18 19:23:14", "rasti": "6202139370061824"
        },
        {
          "aika": "2017-03-18 12:04:26", "rasti": 6653934764556288
        },
        {
          "aika": "2017-03-18 15:21:55", "rasti": "5357714439929856"
        },
        {
          "aika": "2017-03-18 17:59:08", "rasti": "6460378439483392"
        },
        {
          "aika": "2017-03-18 17:54:47", "rasti": "5445149236658176"
        },
        {
          "aika": "2017-03-18 15:59:20", "rasti": "5897428486062080"
        },
        {
          "aika": "2017-03-18 16:09:36", "rasti": "4985069521338368"
        },
        {
          "aika": "2017-03-18 16:18:23", "rasti": "4828368713285632"
        },
        {
          "aika": "2017-03-18 17:37:40", "rasti": "5313972748156928"
        },
        {
          "aika": "2017-03-18 17:09:26", "rasti": "4854848931495936"
        },
        {
          "aika": "2017-03-18 12:10:27", "rasti": 5209879383900160
        },
        {
          "aika": "2017-03-18 14:17:34", "rasti": "5844366849474560"
        },
        {
          "aika": "2017-03-18 16:57:44", "rasti": "6601115927838720"
        },
        {
          "aika": "2017-03-18 12:33:52", "rasti": "6439872654999552"
        },
        {
          "aika": "2017-03-18 13:17:06", "rasti": "5179900512174080"
        },
        {
          "aika": "2017-03-18 13:54:52", "rasti": "6374812490399744"
        },
        {
          "aika": "2017-03-18 17:25:03", "rasti": "6235743596838912"
        },
        {
          "aika": "2017-03-18 13:47:48", "rasti": "5739141090246656"
        },
        {
          "aika": "2017-03-18 13:17:05", "rasti": "5179900512174080"
        },
        {
          "aika": "2017-03-18 18:12:19", "rasti": "5680515860398080"
        },
        {
          "aika": "2017-03-18 13:24:57", "rasti": "6498833966039040"
        },
        {
          "aika": "2017-03-18 18:05:58", "rasti": "6471838888624128"
        },
        {
          "aika": "2017-03-18 17:51:46", "rasti": "6090984811134976"
        }
      ], "leimaustapa": [
        2, 1, 3 ], "sarja": 12345680
    },
    {
      "nimi": "Siskokset", "jasenet": [
        "Seija Kallio", "Sanna Haavikko" ], "pisteet": 0, "matka": 0, 
      "aika": "00:00:00", "id": 491022, "rastileimaukset": [
        {
          "aika": "2017-03-18 17:34:20", "rasti": "5920664393351168"
        },
        {
          "aika": "2017-03-18 16:05:56", "rasti": "4928404407189504"
        },
        {
          "aika": "2017-03-18 17:00:09", "rasti": "4763145205710848"
        },
        {
          "aika": "2017-03-18 17:12:52", "rasti": "5844366849474560"
        },
        {
          "aika": "2017-03-18 12:14:07", "rasti": 6601880566235136
        },
        {
          "aika": "2017-03-18 19:41:04", "rasti": "6358096477683712"
        },
        {
          "aika": "2017-03-18 16:47:19", "rasti": "5266544498049024"
        },
        {
          "aika": "2017-03-18 18:53:00", "rasti": "6439872654999552"
        },
        {
          "aika": "2017-03-18 16:18:36", "rasti": "6190363911913472"
        },
        {
          "aika": "2017-03-18 13:24:22", "rasti": "4985069521338368"
        },
        {
          "aika": "2017-03-18 19:28:45", "rasti": "6653934764556288"
        },
        {
          "aika": "2017-03-18 13:48:26", "rasti": "5897428486062080"
        },
        {
          "aika": "2017-03-18 17:34:11", "rasti": "5920664393351168"
        },
        {
          "aika": "2017-03-18 18:23:56", "rasti": "4642982221316096"
        },
        {
          "aika": "2017-03-18 17:12:43", "rasti": "5844366849474560"
        },
        {
          "aika": "2017-03-18 17:00:25", "rasti": "4763145205710848"
        },
        {
          "aika": "2017-03-18 18:52:41", "rasti": "6439872654999552"
        },
        {
          "aika": "2017-03-18 18:25:02", "rasti": "4642982221316096"
        },
        {
          "aika": "2017-03-18 13:24:14", "rasti": "4985069521338368"
        },
        {
          "aika": "2017-03-18 14:51:38", "rasti": "5548019474759680"
        },
        {
          "aika": "2017-03-18 12:54:56", "rasti": "4771528579219456"
        },
        {
          "aika": "2017-03-18 19:09:12", "rasti": "5209879383900160"
        },
        {
          "aika": "2017-03-18 12:55:43", "rasti": "4771528579219456"
        },
        {
          "aika": "2017-03-18 16:05:25", "rasti": "4928404407189504"
        },
        {
          "aika": "2017-03-18 16:47:22", "rasti": "5266544498049024"
        },
        {
          "aika": "2017-03-18 15:41:20", "rasti": "5357714439929856"
        },
        {
          "aika": "2017-03-18 14:10:28", "rasti": "4894820447289344"
        },
        {
          "aika": "2017-03-18 17:52:14", "rasti": "6020720354131968"
        },
        {
          "aika": "2017-03-18 19:29:14", "rasti": "6653934764556288"
        },
        {
          "aika": "2017-03-18 12:00:00", "rasti": 4821274903707648
        },
        {
          "aika": "2017-03-18 15:41:41", "rasti": "5357714439929856"
        },
        {
          "aika": "2017-03-18 16:18:38", "rasti": "6190363911913472"
        },
        {
          "aika": "2017-03-18 13:09:57", "rasti": "4828368713285632"
        },
        {
          "aika": "2017-03-18 19:41:02", "rasti": "6358096477683712"
        },
        {
          "aika": "2017-03-18 12:27:40", "rasti": "5627413958492160"
        },
        {
          "aika": "2017-03-18 19:08:52", "rasti": "5209879383900160"
        },
        {
          "aika": "2017-03-18 13:09:39", "rasti": "4828368713285632"
        },
        {
          "aika": "2017-03-18 12:13:48", "rasti": 6601880566235136
        },
        {
          "aika": "2017-03-18 14:51:42", "rasti": "5548019474759680"
        },
       {
          "aika": "2017-03-18 17:52:18", "rasti": "6020720354131968"
        },
        {
          "aika": "2017-03-18 14:10:30", "rasti": "4894820447289344"
        },
        {
          "aika": "2017-03-18 13:48:13", "rasti": "5897428486062080"
        }
      ], "leimaustapa": [
        2, 1 ], "sarja": 12345680
    },
    {
      "nimi": "Kaakelin putsaajat ", "jasenet": [
        "Timo Ruonanen", "Mikko Kaajanen", "Jaana Kaajanen" ], 
      "pisteet": 0, "matka": 0, "aika": "00:00:00", "id": 388013, 
      "rastileimaukset": [
        {
          "aika": "2017-03-18 17:29:39", "rasti": "5557775895625728"
        },
        {
          "aika": "2017-03-18 18:10:36", "rasti": "5417798884917248"
        },
        {
          "aika": "2017-03-18 17:05:29", "rasti": "5313972748156928"
        },
        {
          "aika": "2017-03-18 16:42:05", "rasti": "5680515860398080"
        },
        {
          "aika": "2017-03-18 19:42:23", "rasti": "6653934764556288"
        },
        {
          "aika": "2017-03-18 12:08:48", "rasti": 6601880566235136
        },
        {
          "aika": "2017-03-18 12:16:30", "rasti": 5627413958492160
        },
        {
          "aika": "2017-03-18 14:14:25", "rasti": "6235743596838912"
        },
        {
          "aika": "2017-03-18 12:46:55", "rasti": "6202139370061824"
        },
        {
          "aika": "2017-03-18 14:45:00", "rasti": "6529450237755392"
        },
        {
          "aika": "2017-03-18 13:34:02", "rasti": "5876023845453824"
        },
        {
          "aika": "2017-03-18 16:04:27", "rasti": "4613241183404032"
        },
        {
          "aika": "2017-03-18 13:47:41", "rasti": "5232196570841088"
        },
        {
          "aika": "2017-03-18 12:00:00", "rasti": 4821274903707648
        },
        {
          "aika": "2017-03-18 16:47:31", "rasti": "5091900256157696"
        },
        {
          "aika": "2017-03-18 19:33:24", "rasti": "5076239463219200"
        },
        {
          "aika": "2017-03-18 14:58:58", "rasti": "6335779290742784"
        },
        {
          "aika": "2017-03-18 18:52:29", "rasti": "4967437606846464"
        },
        {
          "aika": "2017-03-18 15:13:00", "rasti": "5373190012403712"
        },
        {
          "aika": "2017-03-18 12:22:06", "rasti": "4875454842404864"
        },
        {
          "aika": "2017-03-18 14:32:32", "rasti": "4741461794881536"
        },
        {
          "aika": "2017-03-18 15:36:45", "rasti": "5064464005070848"
        },
        {
          "aika": "2017-03-18 17:18:19", "rasti": "5876922701578240"
        },
        {
          "aika": "2017-03-18 18:21:40", "rasti": "5373375232868352"
        },
        {
          "aika": "2017-03-18 19:49:28", "rasti": "6358096477683712"
        },
        {
          "aika": "2017-03-18 14:08:46", "rasti": "4554615953555456"
        },
        {
          "aika": "2017-03-18 12:58:40", "rasti": "5665699833839616"
        },
        {
          "aika": "2017-03-18 18:28:08", "rasti": "4854848931495936"
        },
        {
          "aika": "2017-03-18 16:55:14", "rasti": "6471838888624128"
        },
        {
          "aika": "2017-03-18 15:44:29", "rasti": "5445149236658176"
        },
        {
          "aika": "2017-03-18 17:48:22", "rasti": "6228649787260928"
        },
        {
          "aika": "2017-03-18 15:40:56", "rasti": "6090984811134976"
        },
        {
          "aika": "2017-03-18 12:26:59", "rasti": "4750123938611200"
        },
        {
          "aika": "2017-03-18 15:25:46", "rasti": "5176191136825344"
        },
        {
          "aika": "2017-03-18 17:00:13", "rasti": "6305800419016704"
        },
        {
          "aika": "2017-03-18 19:05:51", "rasti": "4810425279447040"
        },
        {
          "aika": "2017-03-18 16:34:35", "rasti": "6460378439483392"
        },
        {
          "aika": "2017-03-18 19:25:05", "rasti": "6579711287230464"
        },
        {
          "aika": "2017-03-18 18:39:43", "rasti": "6601115927838720"
        }
      ], "leimaustapa": [
        2, 1 ], "sarja": 12345680
    },
    {
      "nimi": "Tähdenlento", "jasenet": [
        "Virva", "Anu" ], "pisteet": 0, "matka": 0, "aika": "00:00:00", 
      "id": 152701, "rastileimaukset": [], "leimaustapa": [
        2 ], "sarja": 12345678
    },
    {
      "nimi": "Kotilot ", "jasenet": [
        "Niina Salonen", "Maija Meikäläinen", "Jaana Meikäläinen", 
      "Kaisa Konttinen" ], "pisteet": 0, "matka": 0, "aika": "00:00:00", 
      "id": 311985, "rastileimaukset": [
        {
          "aika": "2017-03-18 13:52:04", "rasti": "6358096477683712"
        },
        {
          "aika": "2017-03-18 12:46:32", "rasti": "4750123938611200"
        },
        {
          "aika": "2017-03-18 13:42:08", "rasti": "6653934764556288"
        },
        {
          "aika": "2017-03-18 12:26:45", "rasti": "5627413958492160"
        },
        {
          "aika": "2017-03-18 12:00:00", "rasti": 4821274903707648
        },
        {
          "aika": "2017-03-18 13:51:13", "rasti": "6358096477683712"
        },
        {
          "aika": "2017-03-18 13:18:15", "rasti": "4771528579219456"
        },
        {
          "aika": "2017-03-18 13:09:15", "rasti": "4828368713285632"
        },
        {
          "aika": "2017-03-18 12:26:20", "rasti": "6601880566235136"
        },
        {
          "aika": "2017-03-18 12:14:20", "rasti": 6601880566235136
        },
        {
          "aika": "2017-03-18 12:38:56", "rasti": "4875454842404864"
        },
        {
          "aika": "2017-03-18 13:18:03", "rasti": "4828368713285632"
        }
      ], "leimaustapa": [
        2, 1, 3 ], "sarja": 12345679
    },
    {
      "nimi": "Tollot", "jasenet": [
        "Tappi", "Juju" ], "pisteet": 0, "matka": 0, "aika": "00:00:00", 
      "id": 756141, "rastileimaukset": [
        {
          "aika": "2017-03-18 12:00:00", "rasti": 4821274903707648
        },
        {
          "aika": "2017-03-18 15:56:29", "rasti": "5445149236658176"
        },
        {
          "aika": "2017-03-18 15:29:21", "rasti": "5064464005070848"
        },
        {
          "aika": "2017-03-18 17:54:13", "rasti": "6601115927838720"
        },
        {
          "aika": "2017-03-18 12:16:04", "rasti": 6601880566235136
        },
        {
          "aika": "2017-03-18 16:11:31", "rasti": "5680515860398080"
        },
        {
          "aika": "2017-03-18 14:23:08", "rasti": "6235743596838912"
        },
        {
          "aika": "2017-03-18 16:02:58", "rasti": "6460378439483392"
        },
        {
          "aika": "2017-03-18 18:58:34", "rasti": "6653934764556288"
        },
        {
          "aika": "2017-03-18 12:59:51", "rasti": "6202139370061824"
        },
        {
          "aika": "2017-03-18 12:35:52", "rasti": "4875454842404864"
        },
        {
          "aika": "2017-03-18 12:40:32", "rasti": "4750123938611200"
        },
        {
          "aika": "2017-03-18 13:22:17", "rasti": "5232196570841088"
        },
        {
          "aika": "2017-03-18 15:52:57", "rasti": "6090984811134976"
        },
        {
          "aika": "2017-03-18 14:16:47", "rasti": "6529450237755392"
        },
        {
          "aika": "2017-03-18 13:59:10", "rasti": "4854848931495936"
        },
        {
          "aika": "2017-03-18 17:06:59", "rasti": "5373375232868352"
        },
        {
          "aika": "2017-03-18 14:07:04", "rasti": "4554615953555456"
        },
        {
          "aika": "2017-03-18 14:36:04", "rasti": "5373190012403712"
        },
        {
          "aika": "2017-03-18 16:47:40", "rasti": "5876922701578240"
        },
        {
          "aika": "2017-03-18 15:10:03", "rasti": "5176191136825344"
        },
        {
          "aika": "2017-03-18 15:39:01", "rasti": "5313972748156928"
        },
        {
          "aika": "2017-03-18 18:40:40", "rasti": "5076239463219200"
        },
        {
          "aika": "2017-03-18 17:16:11", "rasti": "4810425279447040"
        },
        {
          "aika": "2017-03-18 15:48:17", "rasti": "6471838888624128"
        },
        {
          "aika": "2017-03-18 19:06:49", "rasti": "6358096477683712"
        },
        {
          "aika": "2017-03-18 16:18:53", "rasti": "5091900256157696"
        },
        {
          "aika": "2017-03-18 17:31:20", "rasti": "4967437606846464"
        },
        {
          "aika": "2017-03-18 12:53:52", "rasti": "5811862536978432"
        },
        {
          "aika": "2017-03-18 15:33:45", "rasti": "6305800419016704"
        },
        {
          "aika": "2017-03-18 12:28:33", "rasti": "5627413958492160"
        }
      ], "leimaustapa": [
        2 ], "sarja": 12345680
    },
    {
      "nimi": "Mudan Ystävät", "jasenet": [
        "Kaija Kinnunen", "Teija Kinnunen" ], "pisteet": 0, "matka": 0, 
      "aika": "00:00:00", "id": 587419, "rastileimaukset": [
        {
          "aika": "2017-03-18 20:04:07", "rasti": "6358096477683712"
        },
        {
          "aika": "2017-03-18 17:25:42", "rasti": "4763145205710848"
        },
        {
          "aika": "2017-03-18 13:03:10", "rasti": "5076239463219200"
        },
        {
          "aika": "2017-03-18 16:58:43", "rasti": "5920664393351168"
        },
        {
          "aika": "2017-03-18 15:22:19", "rasti": "5795146524262400"
        },
        {
          "aika": "2017-03-18 13:01:08", "rasti": "5076239463219200"
        },
        {
          "aika": "2017-03-18 12:00:00", "rasti": 4821274903707648
        },
        {
          "aika": "2017-03-18 14:09:33", "rasti": "6579711287230464"
        },
        {
          "aika": "2017-03-18 12:18:30", "rasti": 5627413958492160
        },
        {
          "aika": "2017-03-18 16:07:44", "rasti": "5739141090246656"
        },
        {
          "aika": "2017-03-18 12:32:32", "rasti": "6601880566235136"
        },
        {
          "aika": "2017-03-18 16:29:16", "rasti": "6374812490399744"
        },
        {
          "aika": "2017-03-18 14:42:02", "rasti": "6001354749247488"
        },
        {
          "aika": "2017-03-18 16:43:11", "rasti": "6020720354131968"
        },
        {
          "aika": "2017-03-18 15:22:42", "rasti": "5795146524262400"
        },
        {
          "aika": "2017-03-18 19:23:22", "rasti": "6110969428180992"
        },
        {
          "aika": "2017-03-18 18:07:37", "rasti": "5357714439929856"
        },
        {
          "aika": "2017-03-18 13:51:27", "rasti": "6214128637050880"
        },
        {
          "aika": "2017-03-18 17:46:23", "rasti": "4928404407189504"
        },
        {
          "aika": "2017-03-18 19:54:59", "rasti": "6653934764556288"
        },
        {
          "aika": "2017-03-18 18:30:02", "rasti": "6592732554330112"
        },
        {
          "aika": "2017-03-18 15:53:29", "rasti": "4685962630135808"
        },
        {
          "aika": "2017-03-18 17:15:18", "rasti": "5844366849474560"
        },
        {
          "aika": "2017-03-18 13:22:07", "rasti": "5475980659392512"
        }
      ], "leimaustapa": [
        2, 1 ], "sarja": 12345680
    },
    {
      "nimi": "RogRog", "jasenet": [
        "Samuli Paavola", "Antti Kaakkuri", "Pekka Kosonen", "Mikko Meikäläinen" ], "pisteet": 0, "matka": 0, "aika": "00:00:00", 
      "id": 585805, "rastileimaukset": [
        {
          "aika": "2017-03-18 14:24:06", "rasti": "6305800419016704"
        },
        {
          "aika": "2017-03-18 12:35:24", "rasti": "4875454842404864"
        },
        {
          "aika": "2017-03-18 14:55:01", "rasti": "5445149236658176"
        },
        {
          "aika": "2017-03-18 13:26:54", "rasti": "4810425279447040"
        },
        {
          "aika": "2017-03-18 14:58:58", "rasti": "6090984811134976"
        },
        {
          "aika": "2017-03-18 13:36:08", "rasti": "5373375232868352"
        },
        {
          "aika": "2017-03-18 13:10:45", "rasti": "4967437606846464"
        },
        {
          "aika": "2017-03-18 14:03:16", "rasti": "5528034857713664"
        },
        {
          "aika": "2017-03-18 15:26:34", "rasti": "5176191136825344"
        },
        {
          "aika": "2017-03-18 19:59:57", "rasti": "6358096477683712"
        },
        {
          "aika": "2017-03-18 18:54:56", "rasti": "4928404407189504"
        },
        {
          "aika": "2017-03-18 19:49:13", "rasti": "5209879383900160"
        },
        {
          "aika": "2017-03-18 18:21:38", "rasti": "5548019474759680"
        },
        {
          "aika": "2017-03-18 14:39:46", "rasti": "5680515860398080"
        },
        {
          "aika": "2017-03-18 15:04:40", "rasti": "5064464005070848"
        },
        {
          "aika": "2017-03-18 12:21:41", "rasti": "5627413958492160"
        },
        {
          "aika": "2017-03-18 13:45:17", "rasti": "4854848931495936"
        },
        {
          "aika": "2017-03-18 14:33:26", "rasti": "5091900256157696"
        },
        {
          "aika": "2017-03-18 19:07:07", "rasti": "5844366849474560"
        },
        {
          "aika": "2017-03-18 16:28:56", "rasti": "5232196570841088"
        },
        {
          "aika": "2017-03-18 16:07:49", "rasti": "6235743596838912"
        },
        {
          "aika": "2017-03-18 12:40:34", "rasti": "4750123938611200"
        },
        {
          "aika": "2017-03-18 14:29:41", "rasti": "6471838888624128"
        },
        {
          "aika": "2017-03-18 14:18:55", "rasti": "5313972748156928"
        },
        {
          "aika": "2017-03-18 18:01:48", "rasti": "6592732554330112"
        },
        {
          "aika": "2017-03-18 12:11:25", "rasti": 6601880566235136
        },
        {
          "aika": "2017-03-18 16:53:26", "rasti": "6202139370061824"
        },
        {
          "aika": "2017-03-18 19:40:21", "rasti": "6439872654999552"
        },
        {
          "aika": "2017-03-18 12:00:00", "rasti": 4821274903707648
        },
        {
          "aika": "2017-03-18 14:49:41", "rasti": "6460378439483392"
        },
        {
          "aika": "2017-03-18 17:35:35", "rasti": "4828368713285632"
        },
        {
          "aika": "2017-03-18 16:45:25", "rasti": "6029782600908800"
        },
        {
          "aika": "2017-03-18 19:03:33", "rasti": "4763145205710848"
        },
        {
          "aika": "2017-03-18 14:11:59", "rasti": "5936325186289664"
        },
        {
          "aika": "2017-03-18 12:52:47", "rasti": "6601115927838720"
        },
        {
          "aika": "2017-03-18 15:56:57", "rasti": "6038930612813824"
        },
        {
          "aika": "2017-03-18 18:49:48", "rasti": "6190363911913472"
        },
        {
          "aika": "2017-03-18 17:07:07", "rasti": "5811862536978432"
        },
        {
          "aika": "2017-03-18 16:12:41", "rasti": "4554615953555456"
        }
      ], "leimaustapa": [
        2, 1 ], "sarja": 12345680
    },
    {
      "nimi": "Vara 3", "jasenet": [
        "barbar" ], "pisteet": 0, "matka": 0, "aika": "00:00:00", "id": 
      988985, "rastileimaukset": [], "leimaustapa": [
        2, 1, 3 ], "sarja": 12345680
    },
    {
      "nimi": "Susi jo syntyessään", "jasenet": [
        "Janne Pannunen", "Riku Aarnio" ], "pisteet": 0, "matka": 0, 
      "aika": "00:00:00", "id": 685328, "rastileimaukset": [
        {
          "aika": "2017-03-18 13:30:26", "rasti": "6202139370061824"
        },
        {
          "aika": "2017-03-18 12:00:00", "rasti": 4821274903707648
        },
        {
          "aika": "2017-03-18 12:13:24", "rasti": 6601880566235136
        },
        {
          "aika": "2017-03-18 12:30:52", "rasti": "5627413958492160"
        },
        {
          "aika": "2017-03-18 18:03:38", "rasti": "6460378439483392"
        },
        {
          "aika": "2017-03-18 15:18:45", "rasti": "6235743596838912"
        },
        {
          "aika": "2017-03-18 18:22:54", "rasti": "5876922701578240"
        },
        {
          "aika": "2017-03-18 12:51:57", "rasti": "5811862536978432"
        },
        {
          "aika": "2017-03-18 19:09:26", "rasti": "5373375232868352"
        },
        {
          "aika": "2017-03-18 12:44:18", "rasti": "4750123938611200"
        },
        {
          "aika": "2017-03-18 14:46:28", "rasti": "5232196570841088"
        },
        {
          "aika": "2017-03-18 18:39:14", "rasti": "6305800419016704"
        },
        {
          "aika": "2017-03-18 16:44:26", "rasti": "6529450237755392"
        },
        {
          "aika": "2017-03-18 17:27:10", "rasti": "5064464005070848"
        },
        {
          "aika": "2017-03-18 18:17:10", "rasti": "5091900256157696"
        },
        {
          "aika": "2017-03-18 19:48:47", "rasti": "6358096477683712"
        },
        {
          "aika": "2017-03-18 14:16:45", "rasti": "4854848931495936"
        },
        {
          "aika": "2017-03-18 18:11:04", "rasti": "5680515860398080"
        },
        {
          "aika": "2017-03-18 17:55:49", "rasti": "5445149236658176"
        },
        {
          "aika": "2017-03-18 16:57:40", "rasti": "5373190012403712"
        },
        {
          "aika": "2017-03-18 16:15:45", "rasti": "4669246617419776"
        },
        {
          "aika": "2017-03-18 17:16:55", "rasti": "6038930612813824"
        },
        {
          "aika": "2017-03-18 18:44:20", "rasti": "5313972748156928"
        },
        {
          "aika": "2017-03-18 19:18:20", "rasti": "4810425279447040"
        },
        {
          "aika": "2017-03-18 18:30:56", "rasti": "6471838888624128"
        },
        {
          "aika": "2017-03-18 15:13:40", "rasti": "4554615953555456"
        },
        {
          "aika": "2017-03-18 14:25:16", "rasti": "6029782600908800"
        },
        {
          "aika": "2017-03-18 17:44:46", "rasti": "6090984811134976"
        },
        {
          "aika": "2017-03-18 12:39:03", "rasti": "4875454842404864"
        },
        {
          "aika": "2017-03-18 15:46:03", "rasti": "5720036136189952"
        },
        {
          "aika": "2017-03-18 18:02:38", "rasti": "5445149236658176"
        },
        {
          "aika": "2017-03-18 18:22:25", "rasti": "5091900256157696"
        },
        {
          "aika": "2017-03-18 13:40:25", "rasti": "6601115927838720"
        },
        {
          "aika": "2017-03-18 13:09:14", "rasti": "6392444404891648"
        }
      ], "leimaustapa": [
        2, 1, 3 ], "sarja": 12345680
    },
    {
      "nimi": "Vara 1", "jasenet": [
        "foobar" ], "pisteet": 0, "matka": 0, "aika": "00:00:00", "id": 
      856937, "rastileimaukset": [], "leimaustapa": [
        2 ], "sarja": 12345680
    },
    {
      "nimi": "Vara 4", "jasenet": [
        "foofoo" ], "pisteet": 0, "matka": 0, "aika": "00:00:00", "id": 
      1037344, "rastileimaukset": [], "leimaustapa": [
        2, 1 ], "sarja": 12345680
    },
    {
      "nimi": "Rennot 1", "jasenet": [
        "Siru Kananen", "Anja Huttunen" ], "pisteet": 0, "matka": 0, 
      "aika": "00:00:00", "id": 818831, "rastileimaukset": [
        {
          "aika": "2017-03-18 16:47:45", "rasti": "6020720354131968"
        },
        {
          "aika": "2017-03-18 18:41:56", "rasti": "6653934764556288"
        },
        {
          "aika": "2017-03-18 12:14:37", "rasti": 6110969428180992
        },
        {
          "aika": "2017-03-18 15:08:20", "rasti": "4928404407189504"
        },
        {
          "aika": "2017-03-18 19:49:08", "rasti": "5076239463219200"
        },
        {
          "aika": "2017-03-18 14:42:03", "rasti": "5357714439929856"
        },
        {
          "aika": "2017-03-18 18:29:30", "rasti": "5209879383900160"
        },
        {
          "aika": "2017-03-18 18:01:23", "rasti": "4642982221316096"
        },
        {
          "aika": "2017-03-18 16:29:50", "rasti": "6217800163000320"
        },
        {
          "aika": "2017-03-18 12:49:22", "rasti": "4828368713285632"
        },
        {
          "aika": "2017-03-18 15:58:37", "rasti": "4763145205710848"
        },
        {
          "aika": "2017-03-18 16:06:19", "rasti": "5844366849474560"
        },
        {
          "aika": "2017-03-18 16:54:55", "rasti": "6374812490399744"
        },
        {
          "aika": "2017-03-18 19:53:06", "rasti": "6358096477683712"
        },
        {
          "aika": "2017-03-18 13:25:04", "rasti": "4894820447289344"
        },
        {
          "aika": "2017-03-18 17:05:04", "rasti": "5739141090246656"
        },
        {
          "aika": "2017-03-18 13:14:50", "rasti": "5897428486062080"
        },
        {
          "aika": "2017-03-18 19:34:31", "rasti": "5627413958492160"
        },
        {
          "aika": "2017-03-18 13:07:33", "rsti": "0"
        },
        {
          "aika": "2017-03-18 18:17:17", "rasti": "6439872654999552"
        },
        {
          "aika": "2017-03-18 12:56:34", "rasti": "4985069521338368"
        },
        {
          "aika": "2017-03-18 12:00:00", "rasti": 4821274903707648
        },
        {
          "aika": "2017-03-18 15:01:31", "rasti": "6190363911913472"
        },
        {
          "aika": "2017-03-18 19:25:14", "rasti": "6601880566235136"
        },
        {
          "aika": "2017-03-18 12:37:11", "rasti": "4771528579219456"
        },
        {
          "aika": "2017-03-18 16:39:54", "rasti": "5920664393351168"
        },
        {
          "aika": "2017-03-18 13:58:44", "rasti": "5548019474759680"
        }
      ], "leimaustapa": [
        2 ], "sarja": 12345680
    },
    {
      "nimi": "Rennot 2", "jasenet": [
        "Sari Maaninka", "Heikki Häkkinen", "Pia Virtanen" ], "pisteet": 
      0, "matka": 0, "aika": "00:00:00", "id": 85103, "rastileimaukset": 
      [
        {
          "aika": "2017-03-18 13:30:48", "rasti": "6592732554330112"
        },
        {
          "aika": "2017-03-18 15:28:01", "rasti": "5739141090246656"
        },
        {
          "aika": "2017-03-18 13:44:44", "rasti": "5357714439929856"
        },
        {
          "aika": "2017-03-18 13:30:43", "rasti": "6592732554330112"
        },
        {
          "aika": "2017-03-18 15:28:00", "rasti": "5739141090246656"
        },
        {
          "aika": "2017-03-18 13:15:20", "rasti": "5102749880418304"
        },
        {
          "aika": "2017-03-18 14:56:38", "rasti": "4763145205710848"
        },
        {
          "aika": "2017-03-18 16:11:57", "rasti": "6358096477683712"
        },
        {
          "aika": "2017-03-18 15:13:32", "rasti": "6020720354131968"
        },
        {
          "aika": "2017-03-18 12:37:27", "rasti": "5209879383900160"
        },
        {
          "aika": "2017-03-18 15:18:12", "rasti": "6374812490399744"
        },
        {
          "aika": "2017-03-18 14:56:59", "rasti": "4763145205710848"
        },
        {
          "aika": "2017-03-18 12:19:41", "rasti": 6653934764556288
        },
        {
          "aika": "2017-03-18 12:19:51", "rasti": 6653934764556288
        },
        {
          "aika": "2017-03-18 15:13:09", "rasti": "6020720354131968"
        },
        {
          "aika": "2017-03-18 12:37:09", "rasti": "5209879383900160"
        },
        {
          "aika": "2017-03-18 15:04:05", "rasti": "5844366849474560"
        },
        {
          "aika": "2017-03-18 14:12:44", "rasti": "5248912583557120"
        },
        {
          "aika": "2017-03-18 14:29:29", "rasti": "4928404407189504"
        },
        {
          "aika": "2017-03-18 14:51:47", "rasti": "5266544498049024"
        },
        {
          "aika": "2017-03-18 14:28:44", "rasti": "4928404407189504"
        },
        {
          "aika": "2017-03-18 12:00:00", "rasti": 4821274903707648
        },
        {
          "aika": "2017-03-18 15:03:56", "rasti": "5844366849474560"
        },
        {
          "aika": "2017-03-18 15:18:39", "rasti": "6374812490399744"
        },
        {
          "aika": "2017-03-18 14:13:29", "rasti": "5248912583557120"
        },
        {
          "aika": "2017-03-18 13:14:55", "rasti": "5102749880418304"
        },
        {
          "aika": "2017-03-18 14:37:19", "rasti": "6190363911913472"
        },
        {
          "aika": "2017-03-18 13:44:48", "rasti": "5357714439929856"
        },
        {
          "aika": "2017-03-18 14:51:25", "rasti": "5266544498049024"
        },
        {
          "aika": "2017-03-18 16:12:17", "rasti": "6358096477683712"
        },
        {
          "aika": "2017-03-18 14:37:23", "rasti": "6190363911913472"
        },
        {
          "aika": "2017-03-18 12:55:28", "rasti": "6110969428180992"
        },
        {
          "aika": "2017-03-18 14:56:41", "rasti": "4763145205710848"
        },
        {
          "aika": "2017-03-18 12:56:44", "rasti": "6110969428180992"
        }
      ], "leimaustapa": [
        2, 1, 3 ], "sarja": 12345678
    },
    {
      "nimi": "Pelättimet", "jasenet": [
        "Kari Vaara", "Katja Vaara" ], "id": 251657, "matka": 0, "aika": 
      "00:00:00", "pisteet": 0, "rastileimaukset": [
        {
          "aika": "2017-03-18 15:19:14", "rasti": "6653934764556288"
        },
        {
          "aika": "2017-03-18 12:22:22", "rasti": 5627413958492160
        },
        {
          "aika": "2017-03-18 14:19:54", "rasti": "5357714439929856"
        },
        {
          "aika": "2017-03-18 15:38:23", "rasti": "5076239463219200"
        },
        {
          "aika": "2017-03-18 14:35:00", "rasti": "5102749880418304"
        },
        {
          "aika": "2017-03-18 14:53:41", "rasti": "6110969428180992"
        },
        {
          "aika": "2017-03-18 13:18:44", "rasti": "5897428486062080"
        },
        {
          "aika": "2017-03-18 12:49:25", "rasti": "4828368713285632"
        },
        {
          "aika": "2017-03-18 13:52:29", "rasti": "5548019474759680"
        },
        {
          "aika": "2017-03-18 12:12:18", "rasti": 6601880566235136
        },
        {
          "aika": "2017-03-18 12:00:00", "rasti": 4821274903707648
        },
        {
          "aika": "2017-03-18 12:39:01", "rasti": "4771528579219456"
        },
        {
          "aika": "2017-03-18 15:27:54", "rasti": "6001354749247488"
        },
        {
          "aika": "2017-03-18 15:10:12", "rasti": "5209879383900160"
        },
        {
          "aika": "2017-03-18 12:58:58", "rasti": "4985069521338368"
        },
        {
          "aika": "2017-03-18 15:44:08", "rasti": "6358096477683712"
        },
        {
          "aika": "2017-03-18 13:36:10", "rasti": "6592732554330112"
        }
      ], "leimaustapa": [
        2, 1 ], "sarja": 12345678
    },
    {
      "nimi": "Sopupeli", "jasenet": [
        "Venla Kujala", "Antti Haukio", "Taina Pekkanen", "Janne Hautanen" ], "pisteet": 0, "matka": 0, "aika": "00:00:00", "id": 
      648569, "rastileimaukset": [
        {
          "aika": "2017-03-18 18:52:15", "rasti": "6358096477683712"
        },
        {
          "aika": "2017-03-18 17:54:05", "rasti": "4750123938611200"
        },
        {
          "aika": "2017-03-18 18:17:24", "rasti": "5627413958492160"
        },
        {
          "aika": "2017-03-18 13:50:35", "rasti": "4821274903707648"
        },
        {
          "aika": "2017-03-18 16:45:02", "rasti": "4854848931495936"
        },
        {
          "aika": "2017-03-18 18:01:17", "rasti": "4875454842404864"
        },
        {
          "aika": "2017-03-18 14:41:47", "rasti": "4913030705971200"
        },
        {
          "aika": "2017-03-18 14:09:33", "rasti": "6601880566235136"
        },
        {
          "aika": "2017-03-18 17:21:19", "rasti": "6029782600908800"
        },
        {
          "aika": "2017-03-18 18:51:40", "rasti": "6358096477683712"
        },
        {
          "aika": "2017-03-18 15:36:06", "rasti": "541779884917248"
        },
        {
          "aika": "2017-03-18 15:03:33", "rasti": "4810425279447040"
        },
        {
          "aika": "2017-03-18 17:37:40", "rasti": "6202139370061824"
        },
        {
          "aika": "2017-03-18 16:26:46", "rasti": "5373375232868352"
        },
        {
          "aika": "2017-03-18 13:03:35", "rasti": "6358096477683712"
        }
      ], "leimaustapa": [
        2, 1 ], "sarja": 12345680
    },
    {
      "nimi": "Retkellä v 13", "jasenet": [
        "Henna Venäläinen", "Katja Vitikka" ], "pisteet": 0, "matka": 0, 
      "aika": "00:00:00", "id": 24909, "rastileimaukset": [
        {
          "aika": "2017-03-18 12:58:18", "rasti": "5627413958492160"
        },
        {
          "aika": "2017-03-18 15:24:45", "rasti": "4913030705971200"
        },
        {
          "aika": "2017-03-18 16:07:47", "rasti": "6358096477683712"
        },
        {
          "aika": "2017-03-18 14:42:48", "rasti": "4967437606846464"
        },
        {
          "aika": "2017-03-18 13:45:19", "rasti": "6202139370061824"
        },
        {
          "aika": "2017-03-18 12:41:28", "rasti": "6601880566235136"
        },
        {
          "aika": "2017-03-18 15:03:12", "rasti": "4810425279447040"
        },
        {
          "aika": "2017-03-18 13:59:38", "rasti": "6601115927838720"
        },
        {
          "aika": "2017-03-18 12:25:21", "rasti": "4821274903707648"
        },
        {
          "aika": "2017-03-18 13:17:45", "rasti": "4750123938611200"
        },
        {
          "aika": "2017-03-18 15:24:48", "rasti": "4913030705971200"
        },
        {
          "aika": "2017-03-18 13:10:29", "rasti": "4875454842404864"
        }
      ], "leimaustapa": [
        2, 1 ], "sarja": 12345678
    },
    {
      "nimi": "Vara 2", "jasenet": [
        "barfoo" ], "pisteet": 0, "matka": 0, "aika": "00:00:00", "id": 
      917852, "rastileimaukset": [], "leimaustapa": [
        2 ], "sarja": 12345680
    },
    {
      "nimi": "Dynamic Duo ", "jasenet": [
        "Kutajoen Tiukunen", "Karhusolan Rentukka" ], "pisteet": 0, 
      "matka": 0, "aika": "00:00:00", "id": 357366, "rastileimaukset": [
        {
          "aika": "2017-03-18 18:37:46", "rasti": "5844366849474560"
        },
        {
          "aika": "2017-03-18 15:30:48", "rasti": "5528034857713664"
        },
        {
          "aika": "2017-03-18 16:12:01", "rasti": "4967437606846464"
        },
        {
          "aika": "2017-03-18 16:27:49", "rasti": "4810425279447040"
        },
        {
          "aika": "2017-03-18 17:46:52", "rasti": "6653934764556288"
        },
        {
          "aika": "2017-03-18 18:53:50", "rasti": "5920664393351168"
        },
        {
          "aika": "2017-03-18 19:49:45", "rasti": "6358096477683712"
        },
        {
          "aika": "2017-03-18 12:35:59", "rasti": "4875454842404864"
        },
        {
          "aika": "2017-03-18 12:00:00", "rasti": 4821274903707648
        },
        {
          "aika": "2017-03-18 13:48:17", "rasti": "5064464005070848"
        },
        {
          "aika": "2017-03-18 14:37:00", "rasti": "5876922701578240"
        },
        {
          "aika": "2017-03-18 15:05:03", "rasti": "5313972748156928"
        },
        {
          "aika": "2017-03-18 19:16:37", "rasti": "5739141090246656"
        },
        {
          "aika": "2017-03-18 14:05:21", "rasti": "5445149236658176"
        },
        {
          "aika": "2017-03-18 14:30:03", "rasti": "5091900256157696"
        },
        {
          "aika": "2017-03-18 14:57:53", "rasti": "6305800419016704"
        },
        {
          "aika": "2017-03-18 19:40:01", "rasti": "6001354749247488"
        },
        {
          "aika": "2017-03-18 14:11:30", "rasti": "6460378439483392"
        },
        {
          "aika": "2017-03-18 12:50:13", "rasti": "5811862536978432"
        },
        {
          "aika": "2017-03-18 13:41:35", "rasti": "6038930612813824"
        },
        {
          "aika": "2017-03-18 12:41:35", "rasti": "4750123938611200"
        },
        {
          "aika": "2017-03-18 12:12:46", "rasti": 6601880566235136
        },
        {
          "aika": "2017-03-18 12:58:02", "rasti": "6202139370061824"
        },
        {
          "aika": "2017-03-18 13:10:19", "rasti": "6029782600908800"
        },
        {
          "aika": "2017-03-18 19:08:46", "rasti": "6374812490399744"
        },
        {
          "aika": "2017-03-18 15:44:29", "rasti": "5373375232868352"
        },
        {
          "aika": "2017-03-18 19:03:29", "rasti": "6020720354131968"
        },
        {
          "aika": "2017-03-18 13:27:58", "rasti": "6235743596838912"
        },
        {
          "aika": "2017-03-18 17:56:49", "rasti": "5209879383900160"
        },
        {
          "aika": "2017-03-18 18:08:44", "rasti": "6439872654999552"
        },
        {
          "aika": "2017-03-18 19:22:52", "rasti": "4685962630135808"
        },
        {
          "aika": "2017-03-18 14:22:10", "rasti": "5680515860398080"
        },
        {
          "aika": "2017-03-18 13:20:08", "rasti": "4554615953555456"
        },
        {
          "aika": "2017-03-18 15:36:47", "rasti": "4854848931495936"
        },
        {
          "aika": "2017-03-18 13:56:18", "rasti": "6090984811134976"
        },
        {
          "aika": "2017-03-18 14:49:36", "rasti": "6471838888624128"
        },
        {
          "aika": "2017-03-18 18:44:32", "rasti": "4763145205710848"
        }
      ], "leimaustapa": [
        2, 1, 3 ], "sarja": 12345680
    },
    {
      "nimi": "Toipilas", "jasenet": [
        "Leena Annila", "Satu Lehtonen" ], "pisteet": 0, "matka": 0, 
      "aika": "00:00:00", "id": 539137, "rastileimaukset": [
        {
          "aika": "2017-03-18 12:15:53", "rasti": "6601880566235136"
        },
        {
          "aika": "2017-03-18 13:23:37", "rasti": "5417798884917248"
        },
        {
          "aika": "2017-03-18 19:24:03", "rasti": "6001354749247488"
        },
        {
          "aika": "2017-03-18 18:35:09", "rasti": "4763145205710848"
        },
        {
          "aika": "2017-03-18 18:49:43", "rasti": "6020720354131968"
        },
        {
          "aika": "2017-03-18 15:04:57", "rasti": "6460378439483392"
        },
        {
          "aika": "2017-03-18 17:15:09", "rasti": "5811862536978432"
        },
        {
          "aika": "2017-03-18 14:37:46", "rasti": "6305800419016704"
        },
        {
          "aika": "2017-03-18 16:07:29", "rasti": "6235743596838912"
        },
        {
          "aika": "2017-03-18 17:54:32", "rasti": "5102749880418304"
        },
        {
          "aika": "2017-03-18 13:40:38", "rasti": "4854848931495936"
        },
        {
          "aika": "2017-03-18 14:12:31", "rasti": "5936325186289664"
        },
        {
          "aika": "2017-03-18 12:02:14", "rasti": "4821274903707648"
        },
        {
          "aika": "2017-03-18 13:00:35", "rasti": "4967437606846464"
        },
        {
          "aika": "2017-03-18 15:15:40", "rasti": "6090984811134976"
        },
        {
          "aika": "2017-03-18 13:33:57", "rasti": "5373375232868352"
        },
        {
          "aika": "2017-03-18 15:22:54", "rasti": "5064464005070848"
        },
        {
          "aika": "2017-03-18 18:19:40", "rasti": "5248912583557120"
        },
        {
          "aika": "2017-03-18 15:56:30", "rasti": "6038930612813824"
        },
        {
          "aika": "2017-03-18 16:24:56", "rasti": "5232196570841088"
        },
        {
          "aika": "2017-03-18 14:56:23", "rasti": "5680515860398080"
        },
        {
          "aika": "2017-03-18 12:36:41", "rasti": "4913030705971200"
        },
        {
          "aika": "2017-03-18 17:06:41", "rasti": "4750123938611200"
        },
        {
          "aika": "2017-03-18 16:56:23", "rasti": "6601115927838720"
        },
        {
          "aika": "2017-03-18 16:11:54", "rasti": "4554615953555456"
        },
        {
          "aika": "2017-03-18 16:41:46", "rasti": "6202139370061824"
        },
        {
          "aika": "2017-03-18 18:57:02", "rasti": "6374812490399744"
        },
        {
          "aika": "2017-03-18 13:49:35", "rasti": "5528034857713664"
        },
        {
          "aika": "2017-03-18 14:45:24", "rasti": "6471838888624128"
        },
        {
          "aika": "2017-03-18 18:39:28", "rasti": "5844366849474560"
        },
        {
          "aika": "2017-03-18 17:30:36", "rasti": "4828368713285632"
        },
        {
          "aika": "2017-03-18 19:35:13", "rasti": "6358096477683712"
        },
        {
          "aika": "2017-03-18 14:50:07", "rasti": "5091900256157696"
        },
        {
          "aika": "2017-03-18 14:18:16", "rasti": "5313972748156928"
        },
        {
          "aika": "2017-03-18 12:48:00", "rasti": "4810425279447040"
        },
        {
          "aika": "2017-03-18 15:11:40", "rasti": "5445149236658176"
        }
      ], "leimaustapa": [
        2, 1, 3 ], "sarja": 12345680
    }
  ]
}
