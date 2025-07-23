# 🗣️ Voice English Tutor Assistant

Este projeto é um **assistente de voz local** que ajuda você a melhorar sua conversação em inglês. Ele utiliza **reconhecimento de fala (Vosk)**, **síntese de voz (TTS)** e um **modelo de linguagem local (Ollama)** para criar uma experiência fluida de conversação totalmente offline (ou quase).



## ✨ Funcionalidades

- 🎙️ Reconhecimento de fala com [Vosk](https://alphacephei.com/vosk/)
- 🧠 Geração de respostas com [Ollama](https://ollama.com/)
- 🗣️ Resposta por voz com o [TTS (Text-to-Speech)](https://github.com/coqui-ai/TTS)
- 🔁 Interação contínua em loop de conversação
- 💡 Ideal para praticar inglês de forma simples e eficaz


## 📋 Pré-requisitos

Antes de rodar o projeto, instale os seguintes componentes no seu sistema:


### 1. Python 3.8 ou superior

> Verifique com `python --version`


### 2. Dependências do sistema

Certifique-se de ter instalados os seguintes pacotes no seu sistema (exemplo para Ubuntu/Debian):

```bash
sudo apt update
sudo apt install python3-pip python3-dev libasound-dev ffmpeg


### 3. Ambiente virtual (opcional, mas recomendado)

python3 -m venv venv
source venv/bin/activate


## Downloads necessários

### 1. Baixe o modelo de reconhecimento de fala (Vosk)

Acesse o link:

👉 https://alphacephei.com/vosk/models

Baixe o modelo English - vosk-model-en-us-0.22 (ou o mais recente)
Extraia-o em um diretório e atualize o caminho no seu código se necessário, por padrão no código a pasta está na raiz do código.


### 2. Instale o Ollama

Você precisará do Ollama para rodar um modelo de linguagem local (como gemma3).

Acesse:
👉 https://ollama.com/download

Após a instalação, rode no terminal:

ollama run gemma:2b


### Como rodar o assistente

Com tudo instalado, execute:

python seu_arquivo.py

Fale algo em inglês. O assistente irá transcrever, gerar uma resposta e responder com áudio.
Comandos especiais

    Diga "exit", "quit" ou "stop" para encerrar o assistente.


### Personalização

Para usar outro modelo TTS, troque o valor de model_name na linha:

TTS(model_name="tts_models/en/ljspeech/glow-tts")


### Possíveis erros comuns

Ollama não responde
Verifique se está rodando com o modelo carregado (ollama run gemma:2b).

Erro ao sintetizar áudio
Verifique se o modelo TTS foi carregado corretamente e se ffmpeg está instalado.

Sem áudio ou microfone
Teste seu microfone com arecord ou outra ferramenta para confirmar que está funcionando.
