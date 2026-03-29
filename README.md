🤖 J.A.R.V.I.S. - Assistente Pessoal de IA
Just A Rather Very Intelligent System
Assistente pessoal inteligente com automação, memória persistente e interação por voz, inspirado no sistema do Homem de Ferro.

Interface JARVIS
📋 Arquitetura do Sistema
Baseada no documento Guia_JARVIS_IA-3.docx:
🧠 Cérebro (LLM): Processamento de linguagem natural e identificação de intenções
💾 Memória: SQLite + Embeddings vetoriais para RAG (Retrieval-Augmented Generation)
⚡ Ações: Execução de comandos no sistema operacional
🎙️ Interface: Voz (STT/TTS) e Gráfica (Tkinter)
🚀 Funcionalidades
✅ Implementadas
☒ Processamento de Linguagem: Identifica intenções (abrir, pesquisar, calcular, etc.)
☒ Memória Persistente: SQLite com histórico de conversas
☒ RAG (Retrieval-Augmented Generation): Busca semântica em interações anteriores
☒ Execução de Ações:
Abrir/fechar aplicativos
Pesquisar no Google
Criar lembretes
Calcular expressões matemáticas
Informar hora/data
☒ Interface de Voz: Reconhecimento de fala (Google Speech) e Síntese (pyttsx3)
☒ Interface Gráfica: Design futurista estilo JARVIS
☒ Aprendizado Contínuo: Armazena preferências e padrões do usuário
🔄 Em Desenvolvimento
☐ Integração com APIs externas (Clima, Notícias)
☐ Automações avançadas (rotinas programáveis)
☐ Confirmação para ações críticas (segurança)
☐ Suporte a mais idiomas
📦 Instalação
1. Clone ou baixe o arquivo
# O arquivo jarvis_ia.py contém todo o sistema
2. Instale as dependências opcionais conforme necessário
Para interface de voz:
pip install SpeechRecognition pyttsx3 PyAudio
Para memória vetorial (RAG):
pip install sentence-transformers numpy
Todas as dependências:
pip install -r requirements.txt
3. Execute
python jarvis_ia.py
🎮 Modos de Operação
1. Modo Texto (⌨️)
Interface via terminal
Digite comandos e receba respostas textuais
Comando sair para encerrar
2. Modo Voz (🎤)
Interação por áudio
Reconhecimento de fala em português (pt-BR)
Respostas faladas pelo sistema
Requer microfone
3. Interface Gráfica (🖥️)
Design escuro futurista
Área de chat com histórico
Botão de microfone para entrada de voz
Requer tkinter (incluso no Python)
📝 Comandos Suportados
Comando
Exemplo
Descrição
Abrir
“Abrir chrome”
Abre aplicativos
Fechar
“Fechar spotify”
Encerra aplicativos
Pesquisar
“Pesquisar Python tutorial”
Busca no Google
Lembrete
“Lembrete reunião às 15h”
Salva lembrete
Calcular
“Quanto é 25 * 4”
Calcula expressões
Hora/Data
“Que horas são?”
Informa horário
Clima
“Como está o tempo?”
Previsão do tempo
Ajuda
“O que você faz?”
Lista comandos

🏗️ Estrutura do Código
jarvis_ia.py
├── SistemaMemoria      # Persistência SQLite + RAG
├── Cerebro            # NLP e identificação de intenções
├── Executor           # Ações no sistema operacional
├── InterfaceVoz       # STT (Speech-to-Text) e TTS
├── JarvisGUI          # Interface Tkinter
└── JarvisCore         # Integração central
🔒 Segurança
Ações críticas (excluir, formatar) requerem confirmação
Dados sensíveis armazenados localmente
Sem envio de dados para servidores externos (exceto Google Speech API quando usando voz)
🛠️ Personalização
Adicionar novas intenções
Edite o dicionário INTENCOES na classe Cerebro:
INTENCOES = {
    "sua_intencao": ["palavra-chave1", "palavra-chave2"],
    # ...
}
Adicionar novas ações
Implemente um novo método na classe Executor:
def _sua_acao(self, params):
    # Sua lógica aqui
    return (True, "Mensagem de sucesso", {})
📊 Banco de Dados
O sistema cria automaticamente jarvis_memoria.db com as tabelas: - interacoes: Histórico completo de comandos e respostas - preferencias: Preferências do usuário - rotinas: Padrões de uso (futuro)
🌟 Roadmap
☐ Integração com LLMs externos (OpenAI, Anthropic)
☐ Suporte a plugins/extensões
☐ Versão web (Flask/FastAPI)
☐ App mobile (Kivy/React Native)
☐ Integração com smart home
📄 Licença
Projeto educacional baseado no documento Guia_JARVIS_IA-3.docx.

Nota: Este é um projeto funcional e escalável. Sinta-se à vontade para contribuir e expandir as funcionalidades!
