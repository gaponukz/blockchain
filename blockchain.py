import hashlib
import json
import time
from typing import List, Dict, IO

Block = Dict[str, str]

class Blockchain(object):
    def __init__(self):
        self.chain: List[Block] = []
        self.last_block: Block = None
        self.last_index: int = 0
        self.valid: bool = True
        self.filename: str = "data.json"
    
    def add_block(self, block: Block) -> None:
        block["hash"] = "0" if not self.last_block else \
            self.get_hash(json.dumps(self.last_block, sort_keys=True))
        
        block['index'] = self.last_index
        block['timestamp'] = time.time()

        self.last_block = block
        self.last_index += 1

        self.chain.append(block)
        self.write_data()
    
    def write_data(self) -> None:
        with open(self.filename, "w", encoding="utf-8") as out:
            json.dump(self.chain, out, indent=4)
    
    def get_hash(self, string: str) -> str:
        return hashlib.sha256(string.encode()).hexdigest()

    def is_valid(self, source: IO = None) -> List[bool, Block]:
        if source: chain = json.load(source)
        else: chain = self.chain

        for block_index in range(1, len(chain)):
            last = chain[block_index-1]
            current = chain[block_index]

            if not self.get_hash(json.dumps(last, sort_keys=True)) == current['hash']:
                return False, last
            
        return True, current