import hashlib
import requests

import sys
import json

import blockchain


class Wallet():
    def __init__(self, user_id):
        self.user_id = user_id
        self.transactions = []
        self.balance = 0
    
    def add_transaction(self, transaction, amount):
        self.transactions.append(transaction)
        self.balance += amount

    def get_balance(self):
        return self.balance


if __name__ == '__main__':
    # What is the server address? IE `python3 miner.py https://server.com/api/`
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    wallets = {}
    r = requests.get(url=node + "/chain")
    
    try:
        data = r.json()
        chain = data['chain']
    except:
        print('Blahh, error')

    #iterate thru the chain and look for user id == sender or recipient
    for block in chain:
        for transaction in block['transactions']:
            recipient = transaction['recipient']
            sender = transaction['sender']
            
            if recipient not in wallets:
                new_wallet = Wallet(recipient)
                wallets[recipient] = new_wallet
            wallets[recipient].add_transaction(transaction, int(transaction['amount']))

            if sender not in wallets:
                new_wallet = Wallet(sender)
                wallets[sender] = new_wallet
            wallets[sender].add_transaction(transaction, -int(transaction['amount']))

    for user_id in wallets.keys():
        print(f'User: {user_id}')
        print(f'Balance: {wallets[user_id].get_balance()}')