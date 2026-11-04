from main import Blockchain

def test_blockchain_init():
    bc = Blockchain()
    assert len(bc.chain) == 1

def test_add_transaction():
    bc = Blockchain()
    bc.new_transaction("A", "B", 100)
    assert len(bc.current_transactions) == 1

def test_pow():
    bc = Blockchain()
    proof = bc.proof_of_work(bc.last_block['proof'])
    assert bc.valid_proof(bc.last_block['proof'], proof) is True

def test_mine():
    bc = Blockchain()
    proof = bc.proof_of_work(bc.last_block['proof'])
    block = bc.new_block(proof)
    assert block['index'] == 2

def test_valid():
    bc = Blockchain()
    assert bc.valid_chain(bc.chain) is True
