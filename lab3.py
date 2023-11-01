from web3 import Web3

infura = "https://sepolia.infura.io/v3/e33d2935bbc84dc3a469b8220444da6d"
w3 = Web3(Web3.HTTPProvider(infura))
print(w3.is_connected())
acc1 = "0x2376e5d54089aacC6B884B6c7C80552Ef27fEfE1"
private_key = "9b1b5eff3652cc44b81f0abae335893f6c6b014f49ff19a234939798ae16d68c"

contract_address = "0x90268C542A261Db2D5294a52D7E0F363799cF343"

contract_abi = [{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"user","type":"address"},{"indexed":False,"internalType":"uint256","name":"newValue","type":"uint256"}],"name":"DataUpdated","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":True,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"inputs":[],"name":"data","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getData","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_newValue","type":"uint256"}],"name":"setData","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"}]

my_contract = w3.eth.contract(address=contract_address, abi=contract_abi)
nonce = w3.eth.get_transaction_count(acc1)

new_data_value = 42  
new_owner_address = "0x2D80E648E8dbd545620b95F9029e4a7Ac3A7849d"  
gas_price = w3.to_wei('20', 'gwei')
transaction_data = my_contract.functions.setData(new_data_value).build_transaction({
    'gas': 200000,  
    'gasPrice': gas_price, 
    'nonce': w3.eth.get_transaction_count(acc1),
})

signed_transaction_data = w3.eth.account.sign_transaction(transaction_data, private_key)

tx_hash_data = w3.eth.send_raw_transaction(signed_transaction_data.rawTransaction)
print(f"setData Transaction Hash: {tx_hash_data.hex()}")

transaction_ownership = my_contract.functions.transferOwnership(new_owner_address).build_transaction({
    'gas': 200000, 
    'gasPrice': gas_price, 
    'nonce': w3.eth.get_transaction_count(acc1) + 1, 
})

signed_transaction_ownership = w3.eth.account.sign_transaction(transaction_ownership, private_key)
tx_hash_ownership = w3.eth.send_raw_transaction(signed_transaction_ownership.rawTransaction)
print(f"transferOwnership Transaction Hash: {tx_hash_ownership.hex()}")

def get_contract_events():
    events = my_contract.events.DataUpdated().get_logs(fromBlock='latest')
    return events

def subscribe_to_data_updated_events():
    event_filter = my_contract.events.DataUpdated().create_filter(fromBlock='latest')
    for event in event_filter.get_all_entries():
        print(f"DataUpdated Event: {event}")

def subscribe_to_ownership_transferred_events():
    event_filter = my_contract.events.OwnershipTransferred().create_filter(fromBlock='latest')
    for event in event_filter.get_all_entries():
        print(f"OwnershipTransferred Event: {event}")

events_data_updated = get_contract_events()
print(f'DataUpdated Events: {events_data_updated}')
subscribe_to_data_updated_events()

events_ownership_transferred = my_contract.events.OwnershipTransferred().get_logs(fromBlock='latest')
print(f'OwnershipTransferred Events: {events_ownership_transferred}')
subscribe_to_ownership_transferred_events()
