from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

PATH_PUBLIC_KEY = "media/LlavesPublicas/"

def generarFirmaDigital( clavePrivadaRSA, message ):
    key = RSA.importKey( clavePrivadaRSA )
    resultHash = SHA256.new( message )
    signature = pkcs1_15.new( key ).sign( resultHash )
    return signature

def verificarFirma( nombreAbogado, message, signature ):
    key = RSA.import_key( open( PATH_PUBLIC_KEY + nombreAbogado + " receiver.pem").read()  )
    resultHash = SHA256.new(message)
    try:
        pkcs1_15.new(key).verify( resultHash, signature )
        return True
    except( ValueError, TypeError ):
        return False
