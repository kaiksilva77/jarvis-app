"""
db.py - Utilitario de acesso ao SQLite
Centraliza a abertura, commit e fechamento de conexoes,
evitando repetir esse padrao em cada funcao da memoria.
"""

import sqlite3
from contextlib import contextmanager


@contextmanager
def cursor(db_path, commit=False):
    """
    Context manager que abre uma conexao SQLite, entrega o cursor
    e garante commit (opcional) e fechamento ao final.

    Uso:
        with cursor(DB_PATH, commit=True) as c:
            c.execute(...)
    """
    conn = sqlite3.connect(db_path)
    try:
        c = conn.cursor()
        yield c
        if commit:
            conn.commit()
    finally:
        conn.close()
