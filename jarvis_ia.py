"""
J.A.R.V.I.S. - Just A Rather Very Intelligent System
Assistente Pessoal de IA com Automação, Memória e Voz
Baseado no documento Guia_JARVIS_IA-3.docx
"""

import os
import sqlite3
import datetime
import threading
import re
from typing import Optional, Dict, List
from dataclasses import dataclass

# Dependências opcionais
try:
    import speech_recognition as sr
    import pyttsx3
    VOZ_OK = True
except ImportError:
    VOZ_OK = False
    print("[!] Voz não disponível: pip install SpeechRecognition pyttsx3")

try:
    import numpy as np
    from sentence_transformers import SentenceTransformer
    EMBEDDINGS_OK = True
except ImportError:
    EMBEDDINGS_OK = False
    print("[!] Embeddings não disponíveis: pip install sentence-transformers")

try:
    import tkinter as tk
    from tkinter import scrolledtext
    GUI_OK = True
except ImportError:
    GUI_OK = False


@dataclass
class Interacao:
    id: Optional[int]
    timestamp: str
    tipo_entrada: str
    comando: str
    intencao: str
    resposta: str
    acao_executada: Optional[str]
    feedback: Optional[str]


# ============================================================
# 1. SISTEMA DE MEMÓRIA (SQLite + RAG)
# ============================================================

class SistemaMemoria:
    def __init__(self, db_path="jarvis_memoria.db"):
        self.db_path = db_path
        self.modelo = None
        if EMBEDDINGS_OK:
            try:
                self.modelo = SentenceTransformer("all-MiniLM-L6-v2")
                print("[OK] Embeddings carregados")
            except Exception as e:
                print(f"[!] Erro embeddings: {e}")
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS interacoes (
            id INTEGER PRIMARY KEY, timestamp TEXT, tipo_entrada TEXT,
            comando TEXT, intencao TEXT, resposta TEXT,
            acao_executada TEXT, embedding BLOB)""")
        c.execute("""CREATE TABLE IF NOT EXISTS preferencias (
            chave TEXT PRIMARY KEY, valor TEXT, categoria TEXT)""")
        conn.commit()
        conn.close()
        print("[OK] Banco de dados pronto")

    def salvar_interacao(self, interacao: Interacao):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        emb = None
        if self.modelo and interacao.comando:
            try:
                emb = self.modelo.encode(interacao.comando).tobytes()
            except:
                pass
        c.execute("INSERT INTO interacoes VALUES (NULL,?,?,?,?,?,?,?,?)",
                 (interacao.timestamp, interacao.tipo_entrada, interacao.comando,
                  interacao.intencao, interacao.resposta, interacao.acao_executada, None, emb))
        conn.commit()
        conn.close()

    def buscar_similares(self, texto: str, limite=3):
        if not self.modelo:
            return []
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT comando, resposta, embedding FROM interacoes WHERE embedding IS NOT NULL")
        rows = c.fetchall()
        conn.close()
        if not rows:
            return []
        query_emb = self.modelo.encode(texto)
        resultados = []
        for row in rows:
            emb = np.frombuffer(row[2], dtype=np.float32)
            sim = np.dot(query_emb, emb) / (np.linalg.norm(query_emb) * np.linalg.norm(emb))
            resultados.append((sim, row))
        resultados.sort(reverse=True, key=lambda x: x[0])
        return [{"comando": r[0], "resposta": r[1], "sim": float(s)} 
                for s, r in resultados[:limite]]

    def salvar_pref(self, chave: str, valor: str, cat="geral"):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO preferencias VALUES (?,?,?)", (chave, valor, cat))
        conn.commit()
        conn.close()


# ============================================================
# 2. CÉREBRO (Processamento de Linguagem)
# ============================================================

class Cerebro:
    INTENCOES = {
        "abrir": ["abrir", "executar", "iniciar", "rodar", "launch"],
        "fechar": ["fechar", "encerrar", "parar", "finalizar", "matar"],
        "pesquisar": ["pesquisar", "buscar", "procurar", "google", "search"],
        "lembrete": ["lembrete", "lembrar", "avisar", "anotar", "notificar"],
        "clima": ["clima", "tempo", "previsão", "temperatura", "weather"],
        "hora": ["hora", "horas", "horário", "que horas", "time"],
        "data": ["data", "dia", "hoje", "que dia", "date"],
        "calcular": ["calcular", "quanto é", "soma", "subtrair", "multiplicar", "dividir"],
        "conversar": ["oi", "olá", "ola", "tudo bem", "bom dia", "boa tarde", "boa noite"],
        "ajuda": ["ajuda", "help", "comandos", "o que você faz", "funcionalidades"]
    }

    def __init__(self, memoria: SistemaMemoria):
        self.memoria = memoria

    def identificar(self, texto: str):
        texto_lower = texto.lower()
        for intencao, palavras in self.INTENCOES.items():
            if any(p in texto_lower for p in palavras):
                params = self._extrair_params(intencao, texto)
                return (intencao, 0.8, params)
        similares = self.memoria.buscar_similares(texto)
        if similares and similares[0]["sim"] > 0.7:
            return ("memoria", 0.6, {"ref": similares[0]})
        return ("desconhecido", 0.3, {})

    def _extrair_params(self, intencao, texto):
        params = {}
        if intencao == "abrir":
            apps = ["chrome", "navegador", "firefox", "calculadora", "editor", 
                   "terminal", "explorer", "spotify", "vscode", "bloco de notas"]
            for app in apps:
                if app in texto.lower():
                    params["app"] = app
                    break
            if "app" not in params:
                palavras = texto.split()
                if len(palavras) > 1:
                    params["app"] = palavras[-1]
        elif intencao in ["pesquisar", "lembrete"]:
            params["termo"] = texto
        return params

    def responder(self, intencao: str, params: dict):
        agora = datetime.datetime.now()
        respostas = {
            "abrir": f"Abrindo {params.get('app', 'aplicativo')}...",
            "fechar": f"Fechando {params.get('app', 'aplicativo')}...",
            "pesquisar": f"Pesquisando: {params.get('termo', '')}",
            "lembrete": "Lembrete registrado com sucesso!",
            "clima": "Consultando previsão do tempo...",
            "hora": f"Agora são {agora.strftime('%H:%M')}",
            "data": f"Hoje é {agora.strftime('%d/%m/%Y')}",
            "calcular": "Calculando...",
            "conversar": "Olá! Como posso ajudar você hoje?",
            "ajuda": """Posso ajudar com:
• Abrir aplicativos (chrome, calculadora, editor, etc.)
• Pesquisar na web
• Criar lembretes
• Calcular expressões
• Informar hora e data
• Consultar clima""",
            "desconhecido": "Não entendi completamente. Pode reformular?",
            "memoria": f"Baseado em nossa conversa anterior: {params.get('ref', {}).get('resposta', '')}"
        }
        return respostas.get(intencao, "Processando sua solicitação...")

    def processar(self, texto: str):
        intencao, conf, params = self.identificar(texto)
        resposta = self.responder(intencao, params)
        requer_acao = intencao not in ["conversar", "hora", "data", "ajuda", "desconhecido", "memoria"]
        return {"intencao": intencao, "conf": conf, "params": params,
                "resposta": resposta, "requer_acao": requer_acao}


# ============================================================
# 3. EXECUTOR DE AÇÕES
# ============================================================

class Executor:
    def __init__(self, cerebro: Cerebro, memoria: SistemaMemoria):
        self.cerebro = cerebro
        self.memoria = memoria

    def executar(self, intencao: str, params: dict):
        try:
            if intencao == "abrir":
                return self._abrir(params)
            elif intencao == "fechar":
                return self._fechar(params)
            elif intencao == "pesquisar":
                return self._pesquisar(params)
            elif intencao == "lembrete":
                return self._lembrete(params)
            elif intencao == "calcular":
                return self._calcular(params)
            elif intencao == "clima":
                return self._clima(params)
            else:
                return (False, "Ação não implementada", {})
        except Exception as e:
            return (False, f"Erro: {str(e)}", {})

    def _abrir(self, params):
        app = params.get("app", "")
        mapa = {
            "chrome": "start chrome" if os.name == "nt" else "google-chrome",
            "navegador": "start chrome" if os.name == "nt" else "google-chrome",
            "firefox": "start firefox" if os.name == "nt" else "firefox",
            "calculadora": "calc" if os.name == "nt" else "gnome-calculator",
            "editor": "notepad" if os.name == "nt" else "gedit",
            "terminal": "cmd" if os.name == "nt" else "gnome-terminal",
            "explorer": "explorer" if os.name == "nt" else "nautilus",
            "spotify": "spotify"
        }
        cmd = mapa.get(app, app)
        if os.name == "nt":
            os.system(f"start {cmd}")
        else:
            os.system(f"{cmd} &")
        return (True, f"Aplicativo {app} iniciado", {})

    def _fechar(self, params):
        app = params.get("app", "")
        if os.name == "nt":
            os.system(f"taskkill /IM {app}.exe /F")
        else:
            os.system(f"pkill -f {app}")
        return (True, f"Aplicativo {app} encerrado", {})

    def _pesquisar(self, params):
        import urllib.parse
        termo = params.get("termo", "")
        url = f"https://www.google.com/search?q={urllib.parse.quote(termo)}"
        if os.name == "nt":
            os.system(f"start chrome {url}")
        else:
            os.system(f"google-chrome {url} &")
        return (True, f"Pesquisando por: {termo}", {"url": url})

    def _lembrete(self, params):
        conteudo = params.get("termo", "")
        with open("lembretes.txt", "a", encoding="utf-8") as f:
            f.write(f"[{datetime.datetime.now()}] {conteudo}\n")
        return (True, "Lembrete salvo em lembretes.txt", {})

    def _calcular(self, params):
        texto = params.get("termo", "")
        match = re.search(r"(\d+\s*[+\-*/]\s*\d+)", texto)
        if match:
            try:
                expr = match.group(1).replace("x", "*").replace("X", "*")
                resultado = eval(expr)
                return (True, f"O resultado é {resultado}", {"resultado": resultado})
            except:
                pass
        return (False, "Não consegui entender o cálculo", {})

    def _clima(self, params):
        # Integrar com OpenWeatherMap API para dados reais
        return (True, "Previsão do tempo: 25°C, ensolarado. (Integrar com API)", {})


# ============================================================
# 4. INTERFACE DE VOZ
# ============================================================

class InterfaceVoz:
    def __init__(self):
        if not VOZ_OK:
            raise Exception("Voz não disponível")
        self.rec = sr.Recognizer()
        self.mic = sr.Microphone()
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 150)
        self.engine.setProperty("volume", 0.9)
        vozes = self.engine.getProperty("voices")
        for v in vozes:
            if "portuguese" in v.name.lower() or "brazil" in v.name.lower():
                self.engine.setProperty("voice", v.id)
                break
        with self.mic as source:
            print("[OK] Calibrando microfone...")
            self.rec.adjust_for_ambient_noise(source, duration=2)

    def ouvir(self) -> Optional[str]:
        with self.mic as source:
            print("🎤 Ouvindo... (fale agora)")
            try:
                audio = self.rec.listen(source, timeout=5, phrase_time_limit=5)
                print("🔄 Processando...")
                texto = self.rec.recognize_google(audio, language="pt-BR")
                print(f"✅ Reconhecido: {texto}")
                return texto
            except sr.WaitTimeoutError:
                print("⏱️ Tempo esgotado")
                return None
            except sr.UnknownValueError:
                print("❌ Não entendi o que foi dito")
                return None
            except Exception as e:
                print(f"❌ Erro: {e}")
                return None

    def falar(self, texto: str):
        print(f"🔊 JARVIS: {texto}")
        self.engine.say(texto)
        self.engine.runAndWait()


# ============================================================
# 5. INTERFACE GRÁFICA
# ============================================================

class JarvisGUI:
    def __init__(self, jarvis):
        self.jarvis = jarvis
        self.root = tk.Tk()
        self.root.title("J.A.R.V.I.S.")
        self.root.geometry("800x600")
        self.root.configure(bg="#0a0e27")
        self._setup()

    def _setup(self):
        # Header
        header = tk.Label(self.root, text="J.A.R.V.I.S.", font=("Consolas", 24, "bold"),
                       bg="#0a0e27", fg="#00d4ff")
        header.pack(pady=10)

        sub = tk.Label(self.root, text="Just A Rather Very Intelligent System",
                      font=("Consolas", 10), bg="#0a0e27", fg="#64748b")
        sub.pack()

        # Área de chat
        self.chat = scrolledtext.ScrolledText(
            self.root, wrap=tk.WORD, width=90, height=25,
            bg="#0f172a", fg="#e2e8f0", font=("Consolas", 11),
            insertbackground="#e2e8f0", padx=10, pady=10)
        self.chat.pack(padx=20, pady=20)
        self.chat.insert(tk.END, "🤖 Sistema inicializado. Aguardando comandos...\n\n")
        self.chat.config(state=tk.DISABLED)

        # Frame de entrada
        frame = tk.Frame(self.root, bg="#0a0e27")
        frame.pack(fill=tk.X, padx=20, pady=10)

        self.entrada = tk.Entry(
            frame, width=60, font=("Consolas", 12),
            bg="#1e293b", fg="#e2e8f0", insertbackground="#e2e8f0",
            relief=tk.FLAT)
        self.entrada.pack(side=tk.LEFT, padx=5)
        self.entrada.bind("<Return>", self._enviar)

        btn_enviar = tk.Button(
            frame, text="➤ Enviar", command=self._enviar,
            bg="#00d4ff", fg="#0a0e27", font=("Consolas", 10, "bold"),
            relief=tk.FLAT, padx=15, pady=5)
        btn_enviar.pack(side=tk.LEFT, padx=5)

        if self.jarvis.voz_ativa:
            btn_voz = tk.Button(
                frame, text="🎤", command=self._voz,
                bg="#7c3aed", fg="white", font=("Consolas", 10),
                relief=tk.FLAT, padx=10, pady=5)
            btn_voz.pack(side=tk.LEFT, padx=5)

        self.status = tk.Label(
            self.root, text="● Sistema Online",
            font=("Consolas", 9), bg="#0a0e27", fg="#10b981", anchor=tk.W)
        self.status.pack(fill=tk.X, padx=20, pady=5)

    def _add_msg(self, remetente, msg):
        self.chat.config(state=tk.NORMAL)
        prefixo = "👤 Você: " if remetente == "user" else "🤖 JARVIS: "
        self.chat.insert(tk.END, f"{prefixo}{msg}\n\n")
        self.chat.see(tk.END)
        self.chat.config(state=tk.DISABLED)

    def _enviar(self, event=None):
        cmd = self.entrada.get().strip()
        if cmd:
            self._add_msg("user", cmd)
            self.entrada.delete(0, tk.END)
            threading.Thread(target=self._processar, args=(cmd,)).start()

    def _processar(self, cmd):
        resp = self.jarvis.processar(cmd, "texto")
        self.root.after(0, lambda: self._add_msg("jarvis", resp["resposta"]))

    def _voz(self):
        self._add_msg("jarvis", "🎤 Ouvindo...")
        threading.Thread(target=self._processar_voz).start()

    def _processar_voz(self):
        cmd = self.jarvis.voz.ouvir()
        if cmd:
            self.root.after(0, lambda: self._add_msg("user", cmd))
            resp = self.jarvis.processar(cmd, "voz")
            self.root.after(0, lambda: self._add_msg("jarvis", resp["resposta"]))
        else:
            self.root.after(0, lambda: self._add_msg("jarvis", "Não entendi. Pode repetir?"))

    def run(self):
        self.root.mainloop()


# ============================================================
# 6. NÚCLEO CENTRAL
# ============================================================

class JarvisCore:
    def __init__(self):
        print("=" * 60)
        print("🤖 INICIALIZANDO J.A.R.V.I.S.")
        print("=" * 60)

        self.memoria = SistemaMemoria()
        self.cerebro = Cerebro(self.memoria)
        self.executor = Executor(self.cerebro, self.memoria)

        try:
            self.voz = InterfaceVoz()
            self.voz_ativa = True
            print("[OK] Interface de voz ativa")
        except Exception as e:
            self.voz = None
            self.voz_ativa = False
            print(f"[!] Voz desativada: {e}")

        print("[OK] Todos os sistemas operacionais")
        print("=" * 60)

    def processar(self, comando: str, tipo: str = "texto"):
        resultado = self.cerebro.processar(comando)
        acao = None
        if resultado["requer_acao"]:
            ok, msg, _ = self.executor.executar(resultado["intencao"], resultado["params"])
            if ok:
                acao = resultado["intencao"]
                resultado["resposta"] = msg

        interacao = Interacao(
            id=None,
            timestamp=datetime.datetime.now().isoformat(),
            tipo_entrada=tipo,
            comando=comando,
            intencao=resultado["intencao"],
            resposta=resultado["resposta"],
            acao_executada=acao,
            feedback=None)
        self.memoria.salvar_interacao(interacao)

        return resultado

    def modo_texto(self):
        print("\n" + "=" * 60)
        print("⌨️  MODO TEXTO ATIVADO")
        print("=" * 60)
        print("Digite 'sair' para encerrar\n")

        while True:
            try:
                cmd = input("👤 Você: ").strip()
                if cmd.lower() in ["sair", "exit", "tchau", "desligar"]:
                    print("\n🤖 JARVIS: Encerrando sistemas. Até logo!")
                    break
                if not cmd:
                    continue

                resp = self.processar(cmd, "texto")
                print(f"🤖 JARVIS: {resp['resposta']}")
                print()

            except KeyboardInterrupt:
                print("\n🤖 JARVIS: Sistema interrompido. Até logo!")
                break
            except Exception as e:
                print(f"❌ Erro: {e}")

    def modo_voz(self):
        if not self.voz_ativa:
            print("[!] Módulo de voz não disponível")
            return

        print("\n" + "=" * 60)
        print("🎤 MODO VOZ ATIVADO")
        print("=" * 60)
        print("Diga 'sair' ou 'desligar' para encerrar\n")

        self.voz.falar("Modo de conversação por voz ativado. Estou ouvindo.")

        while True:
            cmd = self.voz.ouvir()
            if not cmd:
                continue

            if any(p in cmd.lower() for p in ["sair", "desligar", "tchau", "adeus"]):
                self.voz.falar("Desligando sistemas. Até logo, senhor.")
                break

            resp = self.processar(cmd, "voz")
            self.voz.falar(resp["resposta"])


# ============================================================
# 7. PONTO DE ENTRADA
# ============================================================

def main():
    jarvis = JarvisCore()

    print("\nEscolha o modo de operação:")
    print("1. ⌨️  Texto (digitação)")
    print("2. 🎤 Voz" + (" (indisponível)" if not jarvis.voz_ativa else ""))
    if GUI_OK:
        print("3. 🖥️  Interface Gráfica")

    opcao = input("\nOpção (1/2/3): ").strip()

    if opcao == "1":
        jarvis.modo_texto()
    elif opcao == "2" and jarvis.voz_ativa:
        jarvis.modo_voz()
    elif opcao == "3" and GUI_OK:
        app = JarvisGUI(jarvis)
        app.run()
    else:
        print("Opção inválida ou indisponível. Usando modo texto.")
        jarvis.modo_texto()


if __name__ == "__main__":
    main()
