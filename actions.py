"""
actions.py - Ações do JARVIS
Executa cada comando e retorna a resposta.
"""

from datetime import datetime
import math
import re
import memory


def hora():
    return "Agora sao: " + datetime.now().strftime("%H:%M:%S")


def data():
    dias = ["Segunda","Terca","Quarta","Quinta","Sexta","Sabado","Domingo"]
    meses = ["","Jan","Fev","Mar","Abr","Mai","Jun",
             "Jul","Ago","Set","Out","Nov","Dez"]
    agora = datetime.now()
    dia_sem = dias[agora.weekday()]
    return "{}, {} de {} de {}".format(
        dia_sem, agora.day, meses[agora.month], agora.year
    )


def calcular(expressao):
    """Avalia expressao matematica simples de forma segura."""
    # Remove palavras, mantém só os numeros e operadores
    expr = expressao.lower()
    for p in ["calcular","calcule","quanto","e","eh","=","?"]:
        expr = expr.replace(p, " ")

    # Substitui vírgula por ponto
    expr = expr.replace(",", ".").strip()

    if not expr:
        return "Diga o que calcular. Ex: calcular 10+5"

    # Valida: só números, operadores e parênteses
    if not re.match(r'^[\d\s\+\-\*\/\.\(\)\%\^]+$', expr):
        return "Expressao invalida. Use: calcular 10+5"

    try:
        expr = expr.replace("^", "**")
        resultado = eval(expr, {"__builtins__": {}}, {})
        # Formata resultado
        if isinstance(resultado, float) and resultado == int(resultado):
            resultado = int(resultado)
        return "{} = {}".format(expr.strip(), resultado)
    except ZeroDivisionError:
        return "Erro: divisao por zero!"
    except Exception:
        return "Nao consegui calcular. Ex: calcular 10+5"


def salvar(texto):
    """
    Salva um dado. Formatos:
      salvar nome Joao
      salvar telefone 99999
    """
    partes = texto.strip().split(" ", 1)
    if len(partes) < 2:
        return "Use: salvar [chave] [valor]\nEx: salvar nome Joao"
    chave = partes[0].lower()
    valor = partes[1]
    memory.salvar_dado(chave, valor)
    return "Salvo: {} = {}".format(chave, valor)


def lembrar(chave):
    """Busca um dado salvo."""
    chave = chave.strip().lower()
    if not chave:
        return "Use: lembrar [chave]\nEx: lembrar nome"
    valor = memory.buscar_dado(chave)
    if valor:
        return "{}: {}".format(chave, valor)
    return "Nao encontrei '{}'. Use 'listar' para ver o que esta salvo.".format(chave)


def listar():
    """Lista todos os dados salvos."""
    dados = memory.listar_dados()
    if not dados:
        return "Nenhum dado salvo ainda."
    linhas = ["Dados salvos:"]
    for chave, valor in dados:
        linhas.append("  {} = {}".format(chave, valor))
    return "\n".join(linhas)


def historico():
    """Mostra o historico de conversas."""
    hist = memory.buscar_historico(5)
    if not hist:
        return "Historico vazio."
    linhas = ["Ultimas conversas:"]
    for entrada, resposta, dt in reversed(hist):
        linhas.append("[{}] Voce: {}".format(dt, entrada))
        linhas.append("      JARVIS: {}".format(resposta[:60]))
    return "\n".join(linhas)


def ajuda():
    return (
        "Comandos disponiveis:\n"
        "  hora\n"
        "  data\n"
        "  calcular 10+5\n"
        "  salvar nome Joao\n"
        "  lembrar nome\n"
        "  listar\n"
        "  historico\n"
        "  ajuda"
    )
