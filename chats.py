import time
from typing import Literal

import streamlit as st
from PIL import Image
from io import BytesIO

import requests

# Define the class for chat history instances
class ChatHistoryInstance:
    def __init__(self, type_of: Literal["Image", "Text", "Error"], author: Literal["User", "AI"], message: str = "", image_url: str = ""):
        self.type_of = type_of
        self.author = author
        self.message = message
        self.image_url = image_url
        self.streamed = False


# Function to render chat history
def render_chat_history():
    def stream_data(data: str):
        for word in data.split(" "):
            yield word + " "
            time.sleep(0.05)

    for idx, chat_item in enumerate(st.session_state.chat_history):
        if chat_item.type_of == "Text":
            if chat_item.author == "User":
                message = st.chat_message("user")
                message.write(f"{chat_item.message}")
            else:
                message = st.chat_message("assistant")
                col1, col2 = message.columns([0.7, 0.3], gap="large")
                if idx == len(st.session_state.chat_history) - 1 and not chat_item.streamed:
                    # Last AI Message
                    col1.write("**AI Responded**: ")
                    col2.download_button(label="Download", data=chat_item.message, file_name=f"ai-response-{idx}.txt")

                    message.write_stream(
                        stream_data(f"{chat_item.message}")
                    )
                    chat_item.streamed = True
                else:
                    col1.write("**AI Responded**: ")
                    col2.download_button(label="Download", data=chat_item.message,
                                         file_name=f"ai-response-{idx}.txt")
                    message.write(f"{chat_item.message}")
        elif chat_item.type_of == "Image":
            message = st.chat_message("assistant")
            col1, col2 = message.columns([0.7, 0.3], gap="large")
            col1.write(f"**AI Generated an image**:")

            # Download the image from the URL and convert it to bytes
            image_data = requests.get(chat_item.image_url).content
            image = Image.open(BytesIO(image_data))

            # Create a BytesIO buffer to store the image as bytes
            buffer = BytesIO()
            image.save(buffer, format="PNG")  # Save as PNG
            buffer.seek(0)  # Rewind the buffer

            col2.download_button(
                label="Download",
                data=buffer,
                file_name=f"{chat_item.message}.png",
                mime="image/png",
            )
            # SHow the image
            message.image(chat_item.image_url, caption=chat_item.message)
        elif chat_item.type_of == "Error":
            message = st.chat_message("assistant")
            message.error(chat_item.message, icon="ℹ️")


# Function to add a new chat instance
def add_chat_instance(type_of: str, author: str, message: str = "", image_url: str = ""):
    new_chat = ChatHistoryInstance(type_of=type_of, author=author, message=message, image_url=image_url)
    st.session_state.chat_history.append(new_chat)
