
# importing libraries
import json
import datetime
from flask import Flask, jsonify
import hashlib

# auto added library by the program; don't know why this exists
from werkzeug.wrappers import response

# setting up the Blockchain
class Blockchain:

  # initialization
  def __init__(self) -> None:
    self.chain = []

    # create the initial block; aka the genesis block
    self.create_block(proof = 1, previous_hash = '0') 

  # create block and append to chain through this function
  def create_block(self, proof, previous_hash):
    block = {
      'index': len(self.chain) + 1,
      'timestamp': str(datetime.datetime.now()),
      'proof': proof,
      'previous_hash': previous_hash
    }
    self.chain.append(block)
    return block
  
  # get last block of the chain
  def get_previous_block(self):
    return self.chain[-1]
  
  # the proof of work algorithm
  # proof of work is basically the NONCE of a block
  def proof_of_work(self, previous_proof):
    new_proof = 1
    check_proof = False
    while check_proof is False:

      # hash_operation is basically encoding the algorithm with the proof
      hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()

      # verifying condition - you can change the number of zeros; the more the number, harder to get the proof of work
      if hash_operation[:4] == '0000':
        check_proof = True
      else:
        new_proof += 1

    return new_proof

  # get the 64 letters long hash for a block
  def hash(self, block):
    encoded_block = json.dumps(block, sort_keys = True).encode()
    return hashlib.sha256(encoded_block).hexdigest()
  
  # function to check if the whole chain is valid or not!
  def is_chain_valid(self, chain):
    # starting with the genesis block
    previous_block = chain[0]
    block_index = 1

    # I know the first thought would be why to use the while loop than using the for loop which will be convenient 
    # because we cannot gurantee the order of the chain; it may or may not be block index wised

    while block_index < len(chain):
      block = chain[block_index]
      if block['previous_hash'] != self.hash(previous_block):
        return False
      
      previous_proof = previous_block['proof']
      proof = block['proof']
      hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
      if hash_operation[:4] != '0000':
        return False

      previous_block = block
      block_index += 1

    return True
  
# initalizing the Flask [server]
app = Flask(__name__)

# get the Blockchain
blockchain = Blockchain()

# GET request 'mine_block' to mine a block
@app.route('/mine_block', methods = ['GET'])
def mine_block():
  previous_block = blockchain.get_previous_block()
  previous_proof = previous_block['proof']
  proof = blockchain.proof_of_work(previous_proof)
  previous_hash = blockchain.hash(previous_block)
  block = blockchain.create_block(proof, previous_hash)

  response = {
    'message': 'Congratulations you have mined the block successfully!',
    'index': block['index'],
    'timestamp': block['timestamp'],
    'proof': block['proof'],
    'previous_hash': block['previous_hash']
  }

  return jsonify(response), 200


# GET request 'get_chain' to return the complete chain
@app.route('/get_chain', methods = ['GET'])
def get_chain():
  response = {
    'length': len(blockchain.chain),
    'chain': blockchain.chain
  }

  return jsonify(response), 200


# GET request 'is_valid' to check the chain's validity
@app.route('/is_valid', methods = ['GET'])
def is_valid():
  valid = blockchain.is_chain_valid(blockchain.chain)
  if valid is True:
    response = {
      'message': 'Blockchain is Valid',
      'Validity': valid
    }
  else:
    response = {
      'message': 'Blockchain is invalid',
      'Validity': valid
    }
  return jsonify(response), 200

# finally run the app [server]
app.run(host = '0.0.0.0', port = 5000)