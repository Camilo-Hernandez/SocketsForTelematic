#!bin/python3
from socketserver import StreamRequestHandler, BaseRequestHandler
import string

def shift_n_letters(text, n):
    """Emplea encriptación Cesar: Desplaza cada caracter de un texto, n cantidad de letras

    Args:
        text (str): texto a encriptar
        n (int): factor de desplazamiento

    Returns:
        str: texto encriptado
    """
    # alphabet "abcdefghijklmnopqrstuvwxyz"
    intab = string.ascii_lowercase
    # alphabet shifted by n positions
    outtab = intab[n % 26:] + intab[:n % 26]
    # translation made b/w patterns
    trantab = str.maketrans(intab, outtab)
    # text is shifted to right
    return text.translate(trantab)