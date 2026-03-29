"""
brain.py - Cerebro do JARVIS
Interpreta o texto do usuario e decide qual acao executar.
"""

import actions


def processar(texto):
    """
    Recebe o texto do usuario, detecta o comando
    e retorna a resposta do JARVIS.
    """
    texto = texto.strip()
    if not texto:
        return "Diga algo! Digite 'ajuda' para ver os comandos."

    t = texto.lower()

    # ── Saudacao
    if any(w in t for w in ["oi", "ola", "ola", "hello", "bom dia",
                              "boa tarde", "boa noite", "ei", "hey"]):
        return "Ola! Sou o JARVIS. Digite 'ajuda' para ver o que posso fazer."

    # ── Ajuda
    if any(w in t for w in ["ajuda", "help", "comandos", "menu"]):
        return actions.ajuda()

    # ── Hora
    if "hora" in t:
        return actions.hora()

    # ── Data
    if any(w in t for w in ["data", "dia", "hoje"]):
        return actions.data()

    # ── Calcular
    if any(w in t for w in ["calcular", "calcule", "quanto"]):
        # Remove a palavra de comando, passa o resto
        expr = t
        for p in ["calcular", "calcule", "quanto e", "quanto eh", "quanto"]:
            expr = expr.replace(p, "")
        return actions.calcular(expr)

    # ── Expressao matematica direta (ex: "10+5")
    import re
    if re.search(r'\d+\s*[\+\-\*\/]\s*\d+', t):
        return actions.calcular(t)

    # ── Salvar
    if t.startswith("salvar "):
        return actions.salvar(texto[7:])  # Remove "salvar "

    # ── Lembrar / buscar
    if t.startswith("lembrar "):
        return actions.lembrar(texto[8:])  # Remove "lembrar "
    if t.startswith("buscar "):
        return actions.lembrar(texto[7:])

    # ── Listar
    if any(w in t for w in ["listar", "lista", "mostrar tudo", "o que salvei"]):
        return actions.listar()

    # ── Historico
    if any(w in t for w in ["historico", "historico", "conversas"]):
        return actions.historico()

    # ── Agradecimento
    if any(w in t for w in ["obrigado", "obrigada", "valeu", "thanks"]):
        return "De nada! Estou aqui quando precisar."

    # ── Fallback
    return (
        "Nao entendi '{}'\n"
        "Digite 'ajuda' para ver os comandos.".format(texto)
    )
