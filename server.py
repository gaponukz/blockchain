from blockchain import Blockchain
from typing import Callable, IO
import colorama
import time

def database_checker(function: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        while True:
            time.sleep(1)
            with open(kwargs['filename'], "r", encoding='utf-8') as out:
                function(out)
    
    return wrapper

blockchain = Blockchain()

blockchain.add_block({
    "from": "Ada",
    "to": "Me",
    "coin": "btc",
    "amount": 10
})

blockchain.add_block({
    "from": "Me",
    "to": "Ada",
    "coin": "btc",
    "amount": 5
})

blockchain.add_block({
    "from": "Mom",
    "to": "Ded",
    "coin": "btc",
    "amount": 100
})

colorama.init()

@database_checker
def secure(io_file: IO):
    if not (block := blockchain.is_valid(io_file))[0]:
        print(colorama.Fore.RED + f"Error in block {block[1]['index']}")
    
    else:
        print(colorama.Fore.GREEN  + f"Ok")

secure(filename=blockchain.filename)