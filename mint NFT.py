import random
import time
from web3 import Web3

delay = (30, 90)     # delay between wallets
gwei = (127, 129)   # choice(min_gwei, max_gwei) / 10 amount

eth_rpc = 'https://ethereum.blockpi.network/v1/rpc/public'
web3 = Web3(Web3.HTTPProvider(eth_rpc))


def read_file(filename):
    result = []
    with open(filename, 'r') as file:
        for tmp in file.readlines():
            result.append(tmp.replace('\n', ''))

    return result


def write_to_file(filename, text):
    with open(filename, 'a') as file:
        file.write(f'{text}\n')


def mint_nft(private):
    address = web3.eth.account.privateKeyToAccount(private).address

    tx = {
        'from': address,
        'to': web3.toChecksumAddress('0x932261f9Fc8DA46C4a22e31B45c4De60623848bF'),
        'value': 0,  # Set value if needed
        'nonce': web3.eth.getTransactionCount(address),
        'data': '0x1249c58b0021fb3f',
        'chainId': 1
    }

    tx['gas'] = web3.eth.estimateGas(tx)
    tx['maxPriorityFeePerGas'] = web3.toWei(0.1, 'gwei')
    tx['maxFeePerGas'] = web3.toWei(random.randint(*gwei)/10, 'gwei')
    try:
        tx_create = web3.eth.account.sign_transaction(tx, private)
        tx_hash = web3.eth.sendRawTransaction(tx_create.rawTransaction)
        write_to_file('hashes.txt', tx_hash.hex())
        print(f"Transaction hash: {tx_hash.hex()}")
    except Exception as e:
        print(e)
        write_to_file('ERRORS.txt', f'{private};{e}')


def main():
    privates = read_file('privates.txt')
    random.shuffle(privates)

    for private in privates:
        mint_nft(private)
        time.sleep(random.randint(*delay))


if __name__ == '__main__':
    main()
