"""
memory.py - Memória do JARVIS
Salva e recupera dados com SQLite local.
"""

import os

from db import cursor
from utils import agora_str

# Caminho do banco (funciona no Android via Termux/Kivy)
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "jarvis.db")


def inicializar():
    """Cria as tabelas se não existirem."""
    with cursor(DB_PATH, commit=True) as c:
        c.execute("""
            CREATE TABLE IF NOT EXISTS historico (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entrada TEXT,
                resposta TEXT,
                data TEXT
            )
        """)

        c.execute("""
            CREATE TABLE IF NOT EXISTS dados (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chave TEXT UNIQUE,
                valor TEXT,
                data TEXT
            )
        """)


def salvar_historico(entrada, resposta):
    """Salva uma conversa no histórico."""
    with cursor(DB_PATH, commit=True) as c:
        c.execute(
            "INSERT INTO historico (entrada, resposta, data) VALUES (?, ?, ?)",
            (entrada, resposta, agora_str())
        )


def salvar_dado(chave, valor):
    """Salva ou atualiza um dado pelo nome."""
    agora = agora_str()
    with cursor(DB_PATH, commit=True) as c:
        c.execute(
            "INSERT INTO dados (chave, valor, data) VALUES (?, ?, ?) "
            "ON CONFLICT(chave) DO UPDATE SET valor=?, data=?",
            (chave, valor, agora, valor, agora)
        )


def buscar_dado(chave):
    """Busca um dado salvo pela chave."""
    with cursor(DB_PATH) as c:
        c.execute("SELECT valor FROM dados WHERE chave=?", (chave.lower(),))
        resultado = c.fetchone()
    return resultado[0] if resultado else None


def listar_dados():
    """Retorna todos os dados salvos."""
    with cursor(DB_PATH) as c:
        c.execute("SELECT chave, valor FROM dados ORDER BY chave")
        return c.fetchall()


def buscar_historico(limite=5):
    """Retorna as últimas N conversas."""
    with cursor(DB_PATH) as c:
        c.execute(
            "SELECT entrada, resposta, data FROM historico "
            "ORDER BY id DESC LIMIT ?", (limite,)
        )
        return c.fetchall()
