from web3 import Web3


class TestnetTx:
    def __init__(self, rpc_url: str, chain_id: int, private_key: str) -> None:
        self.w3 = Web3(Web3.HTTPProvider(endpoint_uri=rpc_url))
        self.chain_id = chain_id
        self.private_key = private_key
        self.sender = self.w3.eth.account.from_key(
            private_key=self.private_key)

    def sign_and_send(self, addr_to: str, amount: float | int, unit: str = "ether") -> str | None:
        """
        Perform a simple signed transfer from one wallet to another.

        :param addr_to: receiver's address.
        :param amount: amount to be sent.
        :param unit: name of a token being sent. "ether" if not specified otherwise.

        :return: transaction hash on success, None otherwise.
        """
        tx = {
            "from": self.sender.address,
            "to": addr_to,
            "value": self.w3.to_wei(number=amount, unit=unit),
            "nonce": self.w3.eth.get_transaction_count(self.sender.address),
            "gas": 200000,
            "maxFeePerGas": self.w3.to_wei(2, "gwei"),
            "maxPriorityFeePerGas": self.w3.to_wei(1, "gwei"),
            "chainId": self.chain_id
        }
        signed_tx = self.w3.eth.account.sign_transaction(tx, self.private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        receipt = self.w3.eth.wait_for_transaction_receipt(transaction_hash=tx_hash, timeout=360)
        if receipt.get("status") == 1:
            return tx_hash.hex()
        return None

    def call_contract_method(self, contract_addr: str, abi: list, method_name: str, params: list = None) -> str | None:
        """
        Interact with a Solidity Smart Contract deployed on chain.

        :param contract_addr: contract's address.
        :param abi: contract's ABI.
        :param method_name: name of a method/function of a contract that's being called.
        :param params: list of parameters to pass the called function. 

        :return: transaction hash on success, None otherwise.
        """

        tx = {
            "from": self.sender.address,
            "nonce": self.w3.eth.get_transaction_count(self.sender.address),
            "gas": 200000,
            "maxFeePerGas": self.w3.to_wei(2, "gwei"),
            "maxPriorityFeePerGas": self.w3.to_wei(1, "gwei"),
            "chainId": self.chain_id
        }
        Contract = self.w3.eth.contract(address=contract_addr, abi=abi)

        if params:
            contract_method = Contract.functions[method_name](params)
        else:
            contract_method = Contract.functions[method_name]()

        built_tx = contract_method.build_transaction(tx)
        signed_tx = self.w3.eth.account.sign_transaction(built_tx, self.private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        receipt = self.w3.eth.wait_for_transaction_receipt(transaction_hash=tx_hash, timeout=360)
        if receipt.get("status") == 1:
            return tx_hash.hex()
        return None

    def check_balance(self, unit: str = "ether") -> int | float:
        """
        Get balance of current account.

        :param unit: desired balance unit. "ether" if not specified otherwise.

        :return: balance in ETH.
        """
        balance = self.w3.eth.get_balance(account=self.sender.address)
        return self.w3.from_wei(number=balance, unit=unit)
