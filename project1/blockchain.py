#!/usr/bin/env python3
import hashlib
import json
from time import time
from uuid import uuid4
from urllib.parse import urlparse
import requests
import api

class Blockchain(object):
    def __init__(self):
        self.nodes=set()
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

    def new_transaction(self, sender, recipient, amount):
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
            "amount":amount,
            })
            return self.last_block["index"]+1

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
        return self.chain[-1]

    def proof_of_work(self, last_block):
        '''
        simple PoW algorithm
        -find a number 'p*' such that hash of 'pp*' contains leading 4 zeroes where p is previous p*
        -'p' is the previous proof and the 'p*' is the new proof
        :param last_block: <int>
        :return: <int>
        '''
        last_proof=last_block['proof']
        last_hash=self.hash(last_block)

        proof=0
        while self.valid_proof(last_proof, proof) is False:
            proof+=1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        '''
        Validate the proof: does hash (last_proof, proof) contains leading 4 zeroes?

        :param last_proof: <int> previous proof
        :param proof: <int> current proof
        :return: <bool> true if correct, false if not
        '''

        guess=f'{last_proof}{proof}'.encode()
        guess_hash=hashlib.sha256(guess).hexdigest()
        return guess_hash[:4]=="0000"

    def register_node(self, address):
        '''
        add a new node to the list of nodes
        :param address: address of the node; eg. 'http://192.168.0.5:5000'
        '''
        parsed_url=urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def valid_chain(self, chain):
        '''
        determine if a given blockchain is valid
        :param chain: a blockchain
        :return: true if valid false if not
        '''

        last_block=chain[0]
        current_index=1

        while current_index < len(chain):
            block=chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n-------\n")
            #check that the hash of the block is correct
            if block['previous_hash']!=self.hash(last_block):
                return False

            #check that the PoW is correct
            if not self.valid_proof(last_block['proof'], block['proof']):
                return False

            last_block=block
            current_index+=1

            return True

    def resolve_conflict(self):
            '''
            this is our consensus algorithm, it resolves colnflicts by replacing
            our chain with the longest one in the network
            :return: true if our chain was replaced false if not
            '''
            neighbours=self.nodes
            new_chain=None
            #we're looking for chains longer than ours
            max_length=len(self.chain)
            #grab and verify the chains from all the nodes in the network
            for node in neighbours:
                response=requests.get(f'http://{node}/chain')
                if response.status_code==200:
                    length=response.json()['length']
                    chain=response.json()['chain']
                    #check if the length is longer and if chain is valid
                    if length>max_length and self.valid_chain(chain):
                        max_length=length
                        new_chain=chain

            #replace our chain if we found longer than ours and valid
            if new_chain:
                self.chain=new_chain
                return True
            return False

if __name__=="__main__":
    from argparse import ArgumentParser
    parser=ArgumentParser()
    parser.add_argument("-p", "--port", default=5000, type=int, help="port to listen to")
    args=parser.parse_args()
    port=args.port

    api.app.run(host="0.0.0.0", port=port)
