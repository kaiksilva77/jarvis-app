"""
main.py - Interface principal do JARVIS
Integra a interface Kivy com o cerebro e a memoria.
"""

import os

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp, sp

import memory
import brain


# ─────────────────────────────────────────
#  WIDGETS DE MENSAGEM
# ─────────────────────────────────────────

class MensagemUsuario(BoxLayout):
    """Balao de mensagem do usuario."""

    def __init__(self, texto, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.size_hint_y = None

        # Prefixo visual
        self.texto = "[b]Voce:[/b]  " + texto

        # Ajusta altura depois do render
        Clock.schedule_once(self._ajustar, 0)

    def _ajustar(self, dt):
        self.height = self.minimum_height + dp(8)


class MensagemJarvis(BoxLayout):
    """Balao de mensagem do JARVIS."""

    def __init__(self, texto, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.size_hint_y = None

        self.texto = "[b]JARVIS:[/b]  " + texto

        Clock.schedule_once(self._ajustar, 0)

    def _ajustar(self, dt):
        self.height = self.minimum_height + dp(8)


# ─────────────────────────────────────────
#  TELA PRINCIPAL
# ─────────────────────────────────────────

class TelaPrincipal(BoxLayout):
    """
    Layout principal carregado pelo .kv.
    Gerencia o envio e exibicao de mensagens.
    """

    def enviar(self):
        """Chamado quando usuario pressiona Enviar ou tecla Enter."""
        campo = self.ids.campo_texto
        texto = campo.text.strip()
        if not texto:
            return

        # Limpa o campo
        campo.text = ""

        # Exibe mensagem do usuario
        self._adicionar_mensagem(texto, tipo="usuario")

        # Processa e exibe resposta (pequeno delay para feedback visual)
        Clock.schedule_once(lambda dt: self._responder(texto), 0.05)

    def _responder(self, texto):
        """Chama o cerebro e exibe a resposta."""
        try:
            resposta = brain.processar(texto)
        except Exception as e:
            resposta = "Erro interno: {}".format(str(e))

        # Salva no historico
        memory.salvar_historico(texto, resposta)

        # Exibe resposta
        self._adicionar_mensagem(resposta, tipo="jarvis")

    def _adicionar_mensagem(self, texto, tipo="usuario"):
        """Adiciona widget de mensagem ao chat e rola para baixo."""
        chat = self.ids.chat_box

        if tipo == "usuario":
            widget = MensagemUsuario(texto=texto)
        else:
            widget = MensagemJarvis(texto=texto)

        chat.add_widget(widget)

        # Rola para o final
        Clock.schedule_once(lambda dt: self._rolar(), 0.1)

    def _rolar(self):
        """Rola o ScrollView para a ultima mensagem."""
        self.ids.scroll.scroll_y = 0

    def boas_vindas(self):
        """Exibe mensagem inicial."""
        from actions import ajuda
        msg = (
            "Ola! Sou o JARVIS.\n"
            "Funcionando 100%% offline.\n\n"
            + ajuda()
        )
        self._adicionar_mensagem(msg, tipo="jarvis")


# ─────────────────────────────────────────
#  APLICATIVO
# ─────────────────────────────────────────

class JarvisApp(App):

    def build(self):
        # Inicializa banco de dados
        memory.inicializar()

        # Configura cor de fundo da janela
        Window.clearcolor = (0.05, 0.07, 0.12, 1)

        # Cria e retorna a tela principal
        tela = TelaPrincipal()

        # Boas-vindas apos render
        Clock.schedule_once(lambda dt: tela.boas_vindas(), 0.4)

        return tela

    def on_pause(self):
        """Permite pausar sem fechar no Android."""
        return True

    def on_resume(self):
        pass


if __name__ == "__main__":
    JarvisApp().run()
