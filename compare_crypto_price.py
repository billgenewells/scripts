#!/usr/bin/python2.7
"""shebang for bash run"""

import requests
import datetime
import boto3

"""
Script:        compare_bitcoin_price.py
Author:        Bill Wells
Function:    Get bitcoin price and compare to yesterday, determine if 20% or greater difference
Revisions:
"""

SNSCLIENT = boto3.client('sns', region_name='us-west-2')
BTCPERCENT = float("0.10")
ETHPERCENT= float("0.20")

def cryptocompare(btcpercent, ethpercent):
    """
    Documentation for the function
    """

    #yesterday = datetime.date.today()
   # timestamp = yesterday.strftime("%s")

    #coinsnow = requests.get\
    #            ('https://min-api.cryptocompare.com/data/pricemulti?fsyms=ETH,BTC&tsyms=USD')
    #btcyes = requests.get('https://min-api.cryptocompare.com/data/pricehistorical?fsym=BTC&tsyms=USD&ts=' + timestamp)
    #btcyes = requests.get('https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC&tsyms=USD')
    #ethyes = requests.get('https://min-api.cryptocompare.com/data/pricemultifull?fsyms=ETH&tsyms=USD')
    #if coinsnow is None or btcyes is None or ethyes is None:
    #    return "Did not get web data"
     #   exit()

    btc = requests.get('https://api.gdax.com/products/BTC-USD/stats')
    eth = requests.get('https://api.gdax.com/products/ETH-USD/stats')

    btccbopenrate = float(btc.json()['open'])
    btccbnowate = float(btc.json()['last'])
    ethcbopenrate = float(eth.json()['open'])
    ethcbnowate = float(eth.json()['last'])
    #yesterday = datetime.date.today()
    #timestamp = yesterday.strftime("%s")

    #btcnowrate = coinsnow.json()['BTC']['USD']
    #ethnowrate = coinsnow.json()['ETH']['USD']

    #btcyesrate = btcyes.json()['RAW']['BTC']['USD']['HIGH24HOUR']
    #ethyesrate = ethyes.json()['RAW']['ETH']['USD']['HIGH24HOUR']

    #print btcyesrate
    #print ethyesrate
    print btccbopenrate
    print ethcbopenrate

    btcdiff = btccbopenrate - btccbnowate
    ethdiff = ethcbopenrate - ethcbnowate
    #btcdiff = btcyesrate - btcnowrate
    #ethdiff = ethyesrate - ethnowrate

    btcdifference = btcdiff/btccbopenrate
    ethdifference = ethdiff/ethcbopenrate
    #btcdifference = btcdiff/btcyesrate
    #ethdifference = ethdiff/ethyesrate

    btcmess = 'Bitcoin is currently $%s, %s%% difference' % (btccbnowate, round(btcdifference*100, 2))
    ethmess = 'Ethereum is currently $%s, %s%% difference' % (ethcbnowate, round(ethdifference*100, 2))

    print btcmess
    print ethmess

    if btcdifference >= btcpercent:
        SNSCLIENT.publish(
            TargetArn='arn:aws:sns:us-west-2:762287401378:compare_bitcoin_price',
            Message=btcmess
        )
#    if btcnowrate > 2700:
#        SNSCLIENT.publish(
#            TargetArn='arn:aws:sns:us-west-2:762287401378:compare_bitcoin_price',
#            Message="Bitcoin is greater than 2700"
#        )
    if ethdifference >= ethpercent:
        print "sending ETH SMS"
        SNSCLIENT.publish(
            TargetArn='arn:aws:sns:us-west-2:762287401378:compare_bitcoin_price',
            Message=ethmess
        )

    return "Completed"

print cryptocompare(BTCPERCENT, ETHPERCENT)
