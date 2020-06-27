from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

PATH = "./LlavesAbogados/"

def cifrarKeyRSA( nombreAbogado, message ):
    nameDocument = nombreAbogado + " receiver.pem"
    archKey = RSA.import_key( open( PATH + nameDocument ).read() )
    cipher = PKCS1_OAEP.new( archKey )
    cipherText = cipher.encrypt( message )
    return cipherText
