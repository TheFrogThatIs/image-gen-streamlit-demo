# Simple GenAI Demo - 🖼️Image & 💬Text

A simple Streamlit demo that uses [Hive.ai](https://docs.thehive.ai/docs/getting-started) for Image Generation, 
and [Anthropic](https://console.anthropic.com/) for Text Generation, in a unified chat interface. 

The user is prompted for API keys for both of these platforms to use the respective generative feature.

### Public URL
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://image-gen-demo.streamlit.app/)

### Obtaining API Keys
#### Hive.ai
1. [Sign up for Hive.ai account](https://portal.thehive.ai/signup)
2. Within your Organization, Create New Project
   1. Project Type: _Hive Models_
   2. Choose "_Image Generation - ..._" Model (i.e. SDXL, Flux Schnell Enhanced)
   3. Name Project
3. On Project Dashboard > Click _API Keys_
   1. Copy the Key, Paste into Streamlit App

#### Anthropic
1. [Sign up for Anthropic account](https://console.anthropic.com/login)
2. [Create New API Key](https://console.anthropic.com/settings/keys)
3. Store Key Securely, Paste into the Streamlit App

### How to run it on your own machine

1. Install the requirements

```shell
pip install -r requirements.txt
```

2. Run the app

```shell
streamlit run streamlit_app.py
```
or...
```shell
python -m streamlit run streamlit_app.py
```