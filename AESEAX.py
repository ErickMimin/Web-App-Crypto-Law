from base64 import b64encode
from base64 import b64decode
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.SecretSharing import Shamir
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import telegram
import base64
from datetime import datetime

from gestionAbogados.codigoAparte.almacenaBase import almacenaAbogado, almacenaRelacion, obtenObjectCaso
from RSAKeys import cifrarKeyRSA

KeySizeByte = 16

def encryptAES( plainText ):
    key = get_random_bytes( KeySizeByte )
    cipher = AES.new( key, AES.MODE_EAX )
    cipherText, tag = cipher.encrypt_and_digest( plainText )
    return cipher.nonce, key, tag, cipherText

def decryptAES( IV, key, tag, cipherText ):
    cipher = AES.new(key, AES.MODE_EAX, nonce = IV)
    plainText = cipher.decrypt( cipherText )
    try:
        cipher.verify(tag)
        return plainText, True
    except ValueError:
        return plainText, False

def separateKey( key, valorN, valorK, nombreCaso, nameUserList, chatID, nombreArchivo ):
    shares = Shamir.split( valorK, valorN, key )
    users = []
    cont = 0 
    objectCaso = obtenObjectCaso( nombreCaso, nombreArchivo )

    for idx, share in shares:
        print( share )
        nombreAbogado = nameUserList[cont]
        idAbogado =  chatID[cont]
        RSAKeyCaso = cifrarKeyRSA( nombreAbogado, share )
        msg = "Hola abogado %s \n El ID de tu llave es: %d \n Tu llave es: %s \n \nPor favor no la compartas, la necesitaras para tener acceso a los archivos del caso '%s' \n Debes ingresar únicamente lo que esta entre comillas simples" % ( nombreAbogado, idx, base64.b64encode(RSAKeyCaso), nombreCaso )
        bot = telegram.Bot( token = '1225575856:AAElaHpfpWVkS_1B1w5lnW187un80SRkRS4' )
        bot.send_message( chat_id = idAbogado, text = msg )
        users.append( nameUserList[cont] )
        cont = cont + 1

        objectAbogado = almacenaAbogado( nombreAbogado, idAbogado )
        almacenaRelacion( objectCaso, objectAbogado )

    return users
    
def juntarLlaves( numeroAES, clavePrivadasAES, clavePrivadasRSA ): 
    combine = []
    for idx, parteKey, clavePrivada in zip( numeroAES, clavePrivadasAES, clavePrivadasRSA ):
        keyRSA = RSA.importKey( clavePrivada )
        cipherRSA = PKCS1_OAEP.new( keyRSA ) 
        share = cipherRSA.decrypt( base64.b64decode( parteKey ) )
        combine.append( ( int(idx), share) )
    key = Shamir.combine( combine )
    return key

def modificarAES( key, plainText, nombreAbogado, firmaDigital ):
    formatoFecha = '%b %d %Y %I:%M%p'
    dateTime = datetime.now()
    datetimeStr = dateTime.strftime( formatoFecha ) 
    cipher = AES.new( key, AES.MODE_EAX )
    cipherText, tag = cipher.encrypt_and_digest( plainText + b'\n\n'+ b'Ultima modificacion: ' + nombreAbogado.encode() + 
                                                b' ' + datetimeStr.encode() + b'\n\n' + base64.b32encode( firmaDigital ) )
    return cipher.nonce, tag, cipherText
