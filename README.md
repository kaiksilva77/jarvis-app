# JARVIS - Assistente Virtual Offline
## Compilado direto no celular via Termux

---

## ESTRUTURA

```
jarvis_app/
 ├── main.py          Interface Kivy + integração
 ├── brain.py         Interpretação de comandos
 ├── memory.py        Banco de dados SQLite
 ├── actions.py       Funções de resposta
 ├── jarvis.kv        Layout visual
 └── buildozer.spec   Configuração do APK
```

---

## COMANDOS DO APP

```
hora                    → Hora atual
data                    → Data de hoje
calcular 10+5           → Resultado: 15
salvar nome Joao        → Salva "nome = Joao"
lembrar nome            → Mostra o valor salvo
listar                  → Lista tudo que salvou
historico               → Ultimas conversas
ajuda                   → Mostra esta lista
```

---

## COMPILAR NO CELULAR (TERMUX)

### PASSO 1 — Instalar o Termux
Baixe pelo F-Droid (recomendado) ou Play Store:
https://f-droid.org/packages/com.termux/

---

### PASSO 2 — Instalar dependências no Termux

```bash
pkg update && pkg upgrade -y

pkg install -y python git clang make \
    openjdk-17 wget unzip zip \
    libffi openssl

pip install --upgrade pip
pip install cython buildozer
```

---

### PASSO 3 — Permissões de storage

```bash
termux-setup-storage
```
Aparecerá um popup: toque em PERMITIR.

---

### PASSO 4 — Criar o projeto

```bash
cd ~
mkdir jarvis_app
cd jarvis_app
```

---

### PASSO 5 — Criar os arquivos

Cole o conteúdo de cada arquivo:

```bash
# Crie cada arquivo com:
nano main.py
nano brain.py
nano memory.py
nano actions.py
nano jarvis.kv
nano buildozer.spec
```

Para salvar no nano: Ctrl+X → Y → Enter

---

### PASSO 6 — Compilar o APK

```bash
cd ~/jarvis_app
buildozer -v android debug
```

ATENÇÃO: A primeira compilação baixa ~2GB de dependências
(NDK, SDK) e pode demorar 30-60 minutos.

---

### PASSO 7 — Instalar o APK

O APK é gerado em:
```
~/jarvis_app/bin/jarvis-1.0-arm64-v8a-debug.apk
```

Copie para o armazenamento e instale:
```bash
cp bin/*.apk /sdcard/Download/
```

Depois abra o gerenciador de arquivos, vá em Downloads e instale.

---

## TESTAR SEM COMPILAR (Pydroid 3)

Para testar o código antes de gerar APK:

1. Instale o Pydroid 3 pela Play Store
2. Instale o plugin Kivy dentro do Pydroid
3. Abra o main.py e rode

ATENCAO: Pydroid NAO gera APK, serve so para testes.

---

## SOLUCAO DE PROBLEMAS

**Erro de permissão**
```bash
termux-setup-storage
```

**Buildozer não encontrado**
```bash
pip install buildozer --upgrade
export PATH=$PATH:~/.local/bin
```

**Falta de memória RAM**
→ Feche outros apps antes de compilar

**Erro de NDK**
```bash
buildozer android clean
buildozer -v android debug
```

---

## EXPANDIR O JARVIS

Para adicionar novos comandos:

1. Em brain.py: adicione a detecção
```python
if "meu_comando" in t:
    return actions.minha_funcao(texto)
```

2. Em actions.py: adicione a função
```python
def minha_funcao(texto):
    return "Resposta aqui"
```

---

JARVIS v1.0 - 100% offline - Python + Kivy
