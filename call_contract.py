from web3 import Web3
import os

pk = os.environ.get("HASH_MASH")

abi = [{"inputs": [
        {
            "internalType": "string",
            "name": "newMessage",
            "type": "string"
        }
        ],
        "name": "writeMessage",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
        },
       {
    "inputs": [],
    "name": "readMessage",
    "outputs": [
        {
            "internalType": "string",
            "name": "",
            "type": "string"
        }
    ],
    "stateMutability": "view",
    "type": "function"}]


contract_address = "0xAE3C20700f5D5F17BD4e5BaA3ce2fF220A15854D"
# some_address = "0xd203Cb30344DCdDEff030dCadef5674b5E5431ae"

w3 = Web3(Web3.HTTPProvider("https://saturn-rpc.swanchain.io"))

interactor = w3.eth.account.from_key(pk)
nonce = w3.eth.get_transaction_count(interactor.address)

MessageContract = w3.eth.contract(address=contract_address, abi=abi)

tx = MessageContract.functions.writeMessage("Yohai!").build_transaction({"chainId": 2024,
                                                                         "gas": 70000,
                                                                         "maxFeePerGas": w3.to_wei(2, "gwei"),
                                                                         "maxPriorityFeePerGas": w3.to_wei(1, "gwei"),
                                                                         "nonce": nonce})

signed_tx = w3.eth.account.sign_transaction(tx, pk)
tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)


print(f'Transaction Hash: {tx_hash.hex()}')
