"""
memory.py - Memória do JARVIS
Salva e recupera dados com SQLite local.
"""

import sqlite3
import os
from contextlib import closing
from datetime import datetime

# Caminho do banco (funciona no Android via Termux/Kivy)
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "jarvis.db")


def inicializar():
    """Cria as tabelas se não existirem."""
    with closing(sqlite3.connect(DB_PATH)) as conn:
        with conn:
            c = conn.cursor()

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
    agora = datetime.now().strftime("%d/%m/%Y %H:%M")
    with closing(sqlite3.connect(DB_PATH)) as conn:
        with conn:
            conn.execute(
                "INSERT INTO historico (entrada, resposta, data) VALUES (?, ?, ?)",
                (entrada, resposta, agora)
            )


def salvar_dado(chave, valor):
    """Salva ou atualiza um dado pelo nome."""
    agora = datetime.now().strftime("%d/%m/%Y %H:%M")
    with closing(sqlite3.connect(DB_PATH)) as conn:
        with conn:
            conn.execute(
                "INSERT INTO dados (chave, valor, data) VALUES (?, ?, ?) "
                "ON CONFLICT(chave) DO UPDATE SET valor=?, data=?",
                (chave, valor, agora, valor, agora)
            )


def buscar_dado(chave):
    """Busca um dado salvo pela chave."""
    with closing(sqlite3.connect(DB_PATH)) as conn:
        c = conn.cursor()
        c.execute("SELECT valor FROM dados WHERE chave=?", (chave.lower(),))
        resultado = c.fetchone()
    return resultado[0] if resultado else None


def listar_dados():
    """Retorna todos os dados salvos."""
    with closing(sqlite3.connect(DB_PATH)) as conn:
        c = conn.cursor()
        c.execute("SELECT chave, valor FROM dados ORDER BY chave")
        resultado = c.fetchall()
    return resultado


def buscar_historico(limite=5):
    """Retorna as últimas N conversas."""
    with closing(sqlite3.connect(DB_PATH)) as conn:
        c = conn.cursor()
        c.execute(
            "SELECT entrada, resposta, data FROM historico "
            "ORDER BY id DESC LIMIT ?", (limite,)
        )
        resultado = c.fetchall()
    return resultado
