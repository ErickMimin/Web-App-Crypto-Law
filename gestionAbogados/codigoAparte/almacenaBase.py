from gestionAbogados.models import Casos, Abogado, Relacion
from django.core.exceptions import ObjectDoesNotExist

def almacenaCaso( caso, nombreArchivo, cantidadK, boolCifrado ):
    caso = Casos( nombreCaso = caso, archivoCaso = nombreArchivo, numK = cantidadK, cifrado = boolCifrado ) 
    caso.save()

def almacenaAbogado( nombreAbog, idAbogado ):
    try:
        abogadoGuadar = Abogado.objects.get( idTelegram = idAbogado )
    except ObjectDoesNotExist:
        abogadoGuadar = Abogado( idTelegram = int( idAbogado ), nombreAbogado = nombreAbog )
        abogadoGuadar.save()
    #abogadoGuadar = Abogado( idTelegram = int( idAbogado ), nombreAbogado = nombreAbog )
    #if not Abogado.objects.filter( idTelegram = idAbogado ).exists():
    #    abogadoGuadar.save()
    return abogadoGuadar

def obtenObjectCaso( caso, nombreArchivo ):
    instanceCasos = Casos.objects.get( nombreCaso = caso, archivoCaso = nombreArchivo )
    return instanceCasos


def almacenaRelacion( objectCaso, objectAbogado ):
    relacion = Relacion( idCaso = objectCaso, idTelegram = objectAbogado )
    relacion.save()
