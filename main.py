import hashlib
import json
import time
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

class Blockchain:
    def __init__(self):
        self.chain: List[dict] = []
        self.current_transactions: List[dict] = []
        self.new_block(previous_hash="1", proof=100)

    def new_block(self, proof: int, previous_hash: str = None) -> dict:
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]) if self.chain else "1",
        }
        self.current_transactions = []
        self.chain.append(block)
        return block

    def new_transaction(self, sender: str, recipient: str, amount: int) -> int:
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        return self.last_block['index'] + 1

    @staticmethod
    def hash(block: dict) -> str:
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self) -> dict:
        return self.chain[-1]

    def proof_of_work(self, last_proof: int) -> int:
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof: int, proof: int) -> bool:
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:2] == "00"

    def valid_chain(self, chain: List[dict]) -> bool:
        last_block = chain[0]
        current_index = 1
        while current_index < len(chain):
            block = chain[current_index]
            if block['previous_hash'] != self.hash(last_block):
                return False
            if not self.valid_proof(last_block['proof'], block['proof']):
                return False
            last_block = block
            current_index += 1
        return True

app = FastAPI(title="Mini-Blockchain API")
blockchain = Blockchain()

class TransactionRequest(BaseModel):
    sender: str
    recipient: str
    amount: int

@app.get("/chain")
def get_chain():
    return {"chain": blockchain.chain, "length": len(blockchain.chain)}

@app.post("/transactions/new")
def new_transaction(transaction: TransactionRequest):
    index = blockchain.new_transaction(transaction.sender, transaction.recipient, transaction.amount)
    return {"message": f"Транзакция будет в блоке № {index}"}

@app.get("/mine")
def mine():
    last_block = blockchain.last_block
    proof = blockchain.proof_of_work(last_block['proof'])
    blockchain.new_transaction(sender="0", recipient="miner", amount=1)
    block = blockchain.new_block(proof)
    return {"message": "Блок смайнен!", "block": block}

@app.get("/valid")
def validate_chain():
    return {"valid": blockchain.valid_chain(blockchain.chain)}