import random
import hashlib
from fastecdsa.curve import secp256k1
from fastecdsa.point import Point

def private_key_gen():         #generate private key "by tossing coin 256 times" (yes it should be by some kind of crypto library ;d)
    key=[]
    for i in range (0,256):
        j=random.randint(0,1)
        key.append(j)
    key=''.join(str(each) for each in key)
    key=hex(int(key,2))
    return key
'''
def btc_address(public_key):
    val=hashlib.sha256()
    val.update(public_key.x)
    return val
'''

gx=0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798   #secp256k1 constant
gy=0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8

g=Point(gx,gy,curve=secp256k1)

assert(gx==g.x)
assert(gy==g.y)

private_key=private_key_gen()
public_key=int(private_key,16)*g    #gen public key by multiplying 'g', 'private_key' times over finite field
#print(hex(public_key.x))
public_key=str(hex(public_key.x))[2:]+str(hex(public_key.y))[2:]
public_key='04'+public_key[2:]
public_key=
#print(hex(public_key.x))
#print(hex(public_key.y))

#address=btc_address(public_key)
#print(address)
