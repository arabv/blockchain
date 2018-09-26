from flask import Flask, jsonify, request
import blockchain
from uuid import uuid4

#instance our node
app=Flask(__name__)

#generate a globally unique address for this node
node_identifier=str(uuid4()).replace('-','')

#instance the Blockchain

blockchain=blockchain.Blockchain()

#/mine endpoint
@app.route('/mine', methods=["GET"])
def mine():
    #let's run PoW algorithm to receive the next proof
    last_block=blockchain.last_block
    last_proof=last_block["proof"]
    proof=blockchain.proof_of_work(last_block)

    #we are receiving a reward for finding the proof
    #the sender is '0' to signify that this node has mined a new coin
    blockchain.new_transaction(
        sender='0',
        recipient=node_identifier,
        amount=1
    )

    #forge a new block by adding it to the chain
    previous_hash=blockchain.hash(last_block)
    block=blockchain.new_block(proof, previous_hash)

    response={
        "message":"new block forged",
        "index":block["index"],
        "transactions":block["transactions"],
        "proof":block["proof"],
        "previous_hash":block["previous_hash"],
    }
    return jsonify(response), 200

@app.route('/transactions/new', methods=["POST"])
def new_transaction():
    values=request.get_json()

    #check that the posted data are in the POST'ed data
    required=["sender", "recipient", "amount"]

    if not all(k in values for k in required):
        return "missing values", 404

    #create a new transaction
    index=blockchain.new_transaction(values["sender"], values["recipient"], values["amount"])

    response={"message":f"transation will be added to block{index}"}
    return jsonify(response), 201


@app.route('/nodes/register', methods=["POST"])
def register_nodes():
    values=request.get_json()

    nodes=values.get('nodes')

    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(nodes)

    response={
        "message":"new nodes has been added",
        "total_nodes": list(blockchain.nodes)
    }
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced=blockchain.resolve_conflict()

    if replaced:
        response={
            "message":"our chain was replaced",
            "new_chain":blockchain.chain
        }
    else:
        response={
        "message":"our chain is authoritative",
        "chain":blockchain.chain
        }
    return jsonify(response), 200
