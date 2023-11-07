import requests
from pprint import pprint
import json
from datetime import datetime
import time


class Bot:
    def __init__(self):
        self.currencies = []

        self.url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

        self.params = {
            'start': '1',
            'limit': '5000',
            'convert': 'USD'
        }

        self.headers = {
            'Accept': 'application/json',
            'X-CMC_PRO_API_KEY': 'aed024a2-9415-4591-b8ba-9426781496a1'
        }

        self.count = 0

        self.fileList = []

        self.criptoResult = []

    #Caricamento dati dal sito Coinmarket
    def fetchCurrenciesData(self):
        r = requests.get(url=self.url, headers=self.headers, params=self.params).json()
        self.currencies = r['data']
        return r['data']

    # Conta le cryptovalute
    def criptoCount(self):
        for x in self.currencies:
            self.count = self.count + 1
        return self.count

    # Criptovaluta con volume maggiore
    def criptoMaxVolume24(self):
        result = []
        maxVol = 0
        for maxV in self.currencies:
            if maxV['quote']['USD']['volume_24h'] > maxVol:
                maxVol = maxV['quote']['USD']['volume_24h']
                result = maxV
        return result

    #Prime dieci criptovalute per pecentuale di crescita 24h
    def criptoFirstTen(self):
        firstTen = []

        for i in range(10):
            firstTen.append(self.currencies[i])

        for x in range(10):
            for currency in self.currencies:
                if x == 0:
                    if firstTen[x]['quote']['USD']['percent_change_24h'] \
                            < currency['quote']['USD']['percent_change_24h']:
                        firstTen[x] = currency
                elif firstTen[x]['quote']['USD']['percent_change_24h'] < \
                        currency['quote']['USD']['percent_change_24h'] \
                        and firstTen[x - 1]['quote']['USD']['percent_change_24h'] \
                        > currency['quote']['USD']['percent_change_24h']:
                    firstTen[x] = currency

        return firstTen

    #Peggiori 10 criptovalute per incremento percentuale 24h
    def criptoWorstTen(self):
        worstTen = []

        for i in range(10):
            worstTen.append(self.currencies[i])

        for x in range(10):
            for currency in self.currencies:
                if x == 0:
                    if worstTen[x]['quote']['USD']['percent_change_24h'] > currency['quote']['USD'][
                        'percent_change_24h']:
                        worstTen[x] = currency
                elif worstTen[x]['quote']['USD']['percent_change_24h'] > \
                        currency['quote']['USD']['percent_change_24h'] and worstTen[x - 1]['quote']['USD'][
                    'percent_change_24h'] \
                        < currency['quote']['USD']['percent_change_24h']:
                    worstTen[x] = currency

        return worstTen

    #prime 20 criptovalute per incremento volume 24h
    def criptofirstTwenty_marketCap(self):
        firstTwenty = []

        for i in range(20):
            firstTwenty.append(self.currencies[i])

        for x in range(20):
            for currency in self.currencies:
                if x == 0:
                    if firstTwenty[x]['quote']['USD']['market_cap'] < currency['quote']['USD']['market_cap']:
                        firstTwenty[x] = currency
                elif firstTwenty[x]['quote']['USD']['market_cap'] < currency['quote']['USD']['market_cap'] \
                        and firstTwenty[x - 1]['quote']['USD']['market_cap'] > currency['quote']['USD']['market_cap']:
                    firstTwenty[x] = currency

        return firstTwenty

    #criptovalute con magior volume 24h
    def criptoMaxVolumePrice(self):
        firstMaxVolume = []
        for currency in self.currencies:
            if currency['quote']['USD']['volume_24h'] > 76000000:
                firstMaxVolume.append(currency)

        return firstMaxVolume

    #Salvataggio dati elaborati in file
    def saveCriptoFile(self):
        data = datetime.now()
        fileName = data.strftime('%Y-%m-%d.json')
        with open(fileName, 'w') as outFile:
            json.dump(self.criptoResult, outFile)
        self.fileList.append(fileName)


impactBot = Bot()

#inizio ciclo
while(1):
    impactBot.fetchCurrenciesData()

    # Conta il numero delle cryptovalute
    print('\nOggi ci sono in tutto {} criptovalute'.format(impactBot.criptoCount()))

    # Criptovaluta con volume maggiore
    criptoMax = impactBot.criptoMaxVolume24()

    # le prime 10 e le ultime 10 criptovalute
    criptoFirst = impactBot.criptoFirstTen()
    firstTen = {}
    id = 0
    for first in criptoFirst:
        coinId = 'coin_' + str(id)
        firstCoin = {
            'name': first['name'],
            'symbol': first['symbol'],
            'percent_change_24h': first['quote']['USD']['percent_change_24h']
        }
        firstID = {
            coinId: firstCoin
        }
        firstTen.update(firstID)
        id = id + 1

    # le ultime 10 criptovalute
    criptoWorst = impactBot.criptoWorstTen()
    firstWorst = {}
    id = 0
    for worst in criptoWorst:
        coinId = 'coin_' + str(id)
        worstCoin = {
            'name': worst['name'],
            'symbol': worst['symbol'],
            'percent_change_24h': worst['quote']['USD']['percent_change_24h']
        }
        worstID = {
            coinId: worstCoin
        }
        firstWorst.update(worstID)
        id = id + 1

    # il prezzo delle prime venti criptovalute ordinate per Capitale di mercato
    criptoTwenty = impactBot.criptofirstTwenty_marketCap()
    priceTwenty = 0
    pricePrecDay=0

    firstTwenty = {}
    id = 0
    for ftwenty in criptoTwenty:
        priceTwenty = priceTwenty + ftwenty['quote']['USD']['price']
        #calcolo prezzo giorno precedente
        tempPrecDay = (ftwenty['quote']['USD']['price'] * ftwenty['quote']['USD']['percent_change_24h'])/100
        pricePrecDay = pricePrecDay + tempPrecDay
        coinId = 'coin_' + str(id)
        first = {
            'name': ftwenty['name'],
            'symbol': ftwenty['symbol'],
            'price': ftwenty['quote']['USD']['price']
        }
        firstID = {
            coinId: first
        }
        firstTwenty.update(firstID)
        id = id + 1

    # la quantità di denaro necessario per acquistare criptovalute con volume maggiore di 76.000.000$
    criptoMaxVolume = impactBot.criptoMaxVolumePrice()
    priceVolume = 0
    firstVolume = {}
    id = 0
    for maxVolume in criptoMaxVolume:
        priceVolume = priceVolume + maxVolume['quote']['USD']['price']
        coinId = 'coin_id' + str(id)
        first = {
            'name': maxVolume['name'],
            'symbol': maxVolume['symbol'],
            'price': maxVolume['quote']['USD']['price']
        }
        firstID = {coinId: first}
        firstVolume.update(firstID)
        id = id + 1

    # calcola la percentuale
    gainPercent = 0
    gain = 0
    gainPercent = 100 * ((pricePrecDay)/(priceTwenty-pricePrecDay))

    # inserisce i risultati nel file
    result = {
        'criptoMax': {
            'description': 'Criptovaluta con volume maggiore nelle ultime 24 ore',
            'name': criptoMax['name'],
            'symbol': criptoMax['symbol'],
            'volume24h': criptoMax['quote']['USD']['volume_24h']
        },
        'criptoFirst': {
            'description': 'Le migliori 10 criptovalute per percentuale di crescita nelle ultime 24h',
            'valute': firstTen
        },
        'criptoWorst': {
            'description': 'Le peggiori 10 criptovalute per percentuale di crescita nelle ultime 24 ore',
            'valute': firstWorst
        },
        'criptoCap': {
            'description': 'Prezzi di acquisto delle prime 20 criptovalute ordinate per capitalizzazzione nelle ultime 24 ore',
            'valute': firstTwenty,
            'totalPrice': priceTwenty
        },
        'criptoVol': {
            'description': 'Prezzi di acquisto delle criptovalute con volume nelle ultime 24 ore superiore a 76.000.000$',
            'valute': firstVolume,
            'totalPrice': priceVolume
        },
        'monetaryGain': {
            'description': 'Guadagno rispetto al precedente giorno, se avessi acquistato 1 unità delle prime 20 criptovalute',
            'amount': pricePrecDay,
            'percentAmount': gainPercent
        }
    }

    impactBot.criptoResult = result
    impactBot.saveCriptoFile()

    # Stampa a schermo dei valori
    print('\n')
    print(result['criptoMax']['description'])
    print('Nome: {}'.format(result['criptoMax']['name']))
    print('Simbolo: {}'.format(result['criptoMax']['symbol']))

    print('\n')
    print(result['criptoFirst']['description'])
    x = 1
    for valute in result['criptoFirst']['valute']:
        coinId = 'coin_' + str(x-1)
        print('{:02d} - {} {} {:.4f}%'.format(x, result['criptoFirst']['valute'][valute]['name'],\
                                      result['criptoFirst']['valute'][valute]['symbol'],\
                                      result['criptoFirst']['valute'][valute]['percent_change_24h']))
        x = x + 1

    print('\n')
    print(result['criptoWorst']['description'])
    x = 1
    for valute in result['criptoWorst']['valute']:
        print('{:02d} - {} {} {:.4f}%'.format(x, result['criptoWorst']['valute'][valute]['name'],\
                                      result['criptoWorst']['valute'][valute]['symbol'],\
                                      result['criptoWorst']['valute'][valute]['percent_change_24h']))
        x = x + 1

    print('\n')
    print(result['criptoCap']['description'])
    x = 1
    for valute in result['criptoCap']['valute']:
        print('{:02d} - {} {} {:.4f}$'.format(x, result['criptoCap']['valute'][valute]['name'], \
                                      result['criptoCap']['valute'][valute]['symbol'],\
                                      result['criptoCap']['valute'][valute]['price']))
        x = x + 1

    print('\n')
    print(result['criptoVol']['description'])
    x = 1
    for valute in result['criptoVol']['valute']:
        print('{:02d} - {} {} {:.4f}$'.format(x, result['criptoVol']['valute'][valute]['name'], \
                                      result['criptoVol']['valute'][valute]['symbol'],\
                                      result['criptoVol']['valute'][valute]['price']))
        x = x + 1

    print('\n')
    print(result['monetaryGain']['description'])
    print('Oggi hai guadagnato/perso {:.4f}$, lo {:.4f}% rispetto a ieri'.format(result['monetaryGain']['amount'],\
                                                                  result['monetaryGain']['percentAmount']))
    seconds = 59
    minuts = 59
    hours = 23
    print('\n')
    print('tempo mancante al prossimo aggiornamento:')
    while(1):
        print('\r{:02d}:{:02d}:{:02d}'.format(hours, minuts, seconds), end='')
        time.sleep(1)
        seconds = seconds - 1
        if seconds == 0:
            if minuts > 0:
                minuts = minuts - 1
                seconds = 59
            if minuts == 0:
                if hours > 0:
                    hours = hours - 1
                    minuts = 59
                elif seconds <= 0 and minuts <= 0:
                    break






