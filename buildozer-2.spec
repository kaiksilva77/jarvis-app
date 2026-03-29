[app]

# ── Identidade do app ──
title = JARVIS
package.name = jarvis
package.domain = br.jarvis.app

# ── Arquivos do projeto ──
source.dir = .
source.include_exts = py,kv,db

# ── Versão ──
version = 1.0

# ── Dependências ──
# Mínimo necessário para rodar offline no Android
requirements = python3==3.11.0,kivy==2.3.0,sqlite3

# ── Orientação e tela ──
orientation = portrait
fullscreen = 0

# ── Ponto de entrada ──
# main.py é detectado automaticamente

# ── Android ──
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 33
android.ndk_api = 21
android.arch = arm64-v8a

# Armazena banco de dados no storage privado do app
android.private_storage = True

# Cor do splash screen (combina com o tema escuro)
presplash.color = #0A0E1A

# ── Buildozer ──
[buildozer]
log_level = 2
warn_on_root = 1
