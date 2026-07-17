import os
import time
import uuid

def generate_uuidv7() -> uuid.UUID:
    ms = int(time.time() * 1000)
    high = ms << 16
    rand_bytes = os.urandom(10)
    
    high |= (rand_bytes[0] & 0x0F) | 0x7000 
    low = ((rand_bytes[1] & 0x3F) | 0x80) << 56
    for i in range(2, 10):
        low |= rand_bytes[i] << (8 * (9 - i))
        
    return uuid.UUID(int=(high << 64) | low)
