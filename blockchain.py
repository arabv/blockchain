#!/usr/bin/env python3
import hashlib
import json
from time import time
from uuid import uuid4


class Blockchain(object):
    def __init__(self):
        self.chain=[]
        self.pending_transactions=[]

        #creating genesis block
        self.new_block(previous_hash='1', proof=100)

    def new_block(self, proof, previous_hash=None):
        '''
        creates new blocks and adds it to the chain
        :param proof: <int> the proof given by PoW algorithm
        :param previous_hash: (oprional) <str> hash of the previous block
        :return: <dict> new block
        '''

        block={
        "index" :len(self.chain)+1,
        "timestamp" :time(),
        "transactions"  :self.pending_transactions,
        "proof" :proof,
        "previous_hash" :previous_hash or self.hash(self.chain[-1])
        }

        #reset the current list of transactions
        self.pending_transactions=[]
        self.chain.append(block)
        return block

    def new_transaction(self):
        #adds new transation to the list of transactions
        pass

    @staticmethod
    def hash(block):
        '''
        creates a SHA256 hash of a block
        :param block:   <dict> blocks
        :return: <str>
        '''

        #we must make sure that the dictionary is ordered or we will have inconsistent hashes
        block_string=json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()


    @property
    def last_block(self):
        #returns the last block in the chain
        self.chain[-1]

    def new_transaction(self, sender recipient, amount):
        '''
        Creates a new transation to go into the next mined block
        :param sender:  <str> address of the sender
        :param recipient:   <str> address of the recipient
        :param amount:  <int> amount
        :return: <int> the index of the block that will hold this transaction
        '''
        self.pending_transactions.append({
        "sender":sender,
        "recipient":recipient,
        "amount":amount
        })
        return self.last_block["index"]+1