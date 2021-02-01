#!/usr/bin/python3.8

#########################################################################
# File Name: generator.py
# Author: Kidd Chao
# Mail: zzykid1412@gmail.com
# Created Time: Mon 31 Aug 2020 07:57:25 PM DST
#########################################################################

import json
import time
import random

total_amount = 30000 #total value you need per month
total_amount_average = total_amount/30

def select_card():

    # time.gmtime()      UTC time
    # time.localtime     Local time
    current_time = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(time.time()))
    print(current_time)

    localtime = time.localtime(time.time())
    date = localtime.tm_mday

    with open('cards.json') as obj:
        cardslist = json.load(obj)
    for card in cardslist['cards']:
        # account_period means the maxinum interest-free period
        # repayment period means how many days from today to next repayment data
        if card['repayment_date'] > card['statement_date']:
            card['account_period'] = card['repayment_date'] + 30 - card['statement_date']
            if card['statement_date'] > date:
                card['repayment_period'] = card['repayment_date'] - date
            else:
                card['repayment_period'] = card['repayment_date'] + 30 - date
        else:
            card['account_period'] = card['repayment_date'] + 60 - card['statement_date']
            if card['statement_date'] > date:
                card['repayment_period'] = card['repayment_date'] + 30 - date
            else:
                card['repayment_period'] = card['repayment_date'] + 60 - date

        if card['account_period'] == card['repayment_period']:
            card['repayment_period'] = card['repayment_period'] - 30

    # Sort card by repayment period
    sequence = sorted(cardslist['cards'], key = lambda x:x["repayment_period"])

    # Output format
    #tplt = "{0:^10}\t{1:^10}\t{2:^10}"
    tplt = "{0:{3}^10}\t{1:{3}^10}\t{2:^10}"
    print(tplt.format("       Name", "          Account period", "  Due", chr(12288)))
    for card in sequence:
        print(tplt.format(card['name'], card['account_period'], card['repayment_period'], chr(12288)))

    print("")
    print("Advice Card: " + card['name'])

    #print(sequence[0]) find first element in dictionary
    #print(sequence[-1]) find last element in dictionary


    # Generate a random card,
    for card in sequence:
        card['random_number'] = card['repayment_period'] + random.randint(0, 30)

    sequence = sorted(cardslist['cards'], key = lambda x:x["random_number"])

    #for card in sequence:
    #    print(tplt.format(card['name'], card['account_period'], card['repayment_period']))

    tplt = "{0:{2}^10}\t{1:^10}"
    print("")
    print(tplt.format("       Name", "          Random", chr(12288)))
    for card in sequence:
        print(tplt.format(card['name'], card['random_number'], chr(12288)))

    print("")
    print("Random Card: " + sequence[-1]['name'])


def select_pos():
    with open('POSs.json') as obj:
        poslist = json.load(obj)

    for pos in poslist['POSs']:
        pos['big_rate'] = pos['big_rate'] + random.randint(0, 10)

    sequence = sorted(poslist['POSs'], key = lambda x:x["big_rate"])

    print("")
    print("Advice POS: " + sequence[0]['name'])

def random_amount(amount_range):
    amount = random.randint(0, amount_range)

    # Reduce unexpected value
    if amount < 100 or amount > 1000:
        amount = random.randint(0, amount_range)

    print("")
    print("Amount: " + str(amount))

if __name__ == '__main__':
        select_card()

        select_pos()

        random_amount(2 * total_amount_average)
