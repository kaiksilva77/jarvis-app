"""
utils.py - Funcoes utilitarias compartilhadas do JARVIS
Reune pequenos helpers usados por mais de um modulo.
"""

from datetime import datetime


def agora_str():
    """Timestamp padrao usado no banco (dd/mm/aaaa hh:mm)."""
    return datetime.now().strftime("%d/%m/%Y %H:%M")


def remover_palavras(texto, palavras, sub=" "):
    """
    Remove uma lista de palavras/tokens de um texto.
    Usado para tirar as palavras de comando antes de processar o resto.
    """
    for p in palavras:
        texto = texto.replace(p, sub)
    return texto
