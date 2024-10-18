from typing import List

import streamlit as st
from anthropic import Anthropic

import hive_ai_wrapper
from helpers import bottom
from chats import ChatHistoryInstance, render_chat_history, add_chat_instance

message_context_length = 10

# Define session state variables to store history
if "chat_history" not in st.session_state:
    st.session_state.chat_history: List[ChatHistoryInstance] = []  # To store chat prompts and responses


# ----------------------------- Page Content -------------------------------------
image_gen = "🖼️ Image Generation"
text_gen = "💬 Text Generation"


st.title(":rainbow[Generative AI Demo - Image/Text]")
st.link_button("By TheFrogThatIs", "https://github.com/TheFrogThatIs", icon="🐸")


with st.container(border=True):
    anthropic_api_key = st.text_input(
        "[Anthropic API Key](https://console.anthropic.com/)",
        type="password",
        help="Anthropic Key is Required for Text Generation"
    )
    hiveai_api_key = st.text_input(
        "[Hive.ai API Key](https://docs.thehive.ai/docs/getting-started)",
        type="password",
        help="Hive.ai Key is Required for Image Generation."
    )

# Create an OpenAI client.
anthropic_client = Anthropic(api_key=anthropic_api_key)


with bottom():
    selected_method = st.selectbox(
        "Choose the method for generating the response:",
        [image_gen, text_gen],
    )

    chat_disabled = (selected_method == image_gen and not hiveai_api_key) or (selected_method == text_gen and not anthropic_api_key)
    prompt = st.chat_input(
        f"{selected_method}: What do you want to create today?" if selected_method == image_gen
        else f"{selected_method}: Let's chat! Send me a message",
        disabled=chat_disabled,
    )
    if selected_method == image_gen and not hiveai_api_key:
        st.error('Hive.ai Key is Required for Image Generation.', icon="ℹ️")
    if selected_method == text_gen and not anthropic_api_key:
        st.error('Anthropic Key is Required for Text Generation', icon="ℹ️")


# Chat Container
with st.container(border=True):
    if prompt:
        # Add user prompt to chat history
        add_chat_instance(type_of="Text", author="User", message=prompt)

        # ----------------------------- Image Generation -------------------------------------
        if selected_method == image_gen:
            # Call the image generation API
            image_response = {}
            try:
                image_response = hive_ai_wrapper.generate_image_response(prompt, hiveai_key=hiveai_api_key, images_count=1)
                image_url = image_response["status"][0]["response"]["output"][0]["images"][0]["url"]  # Not ideal, but fine for this

                # Add generated image to chat history
                add_chat_instance(type_of="Image", author="AI", message=prompt, image_url=image_url)
            except Exception as e:
                if "message" in image_response:
                    add_chat_instance(type_of="Error", author="AI", message=image_response["message"])
                else:
                    add_chat_instance(type_of="Error", author="AI", message="This Request to AI has Failed. Please Check API Key/s.")

        # ----------------------------- Text Generation -------------------------------------
        elif selected_method == text_gen:
            # Generate a response using the Anthropic API.
            # https://docs.anthropic.com/en/api/client-sdks#python
            message_history = [{
                "role": "user" if m.author == "User" else "assistant",
                "content": m.message if m.type_of == "Text" else f"AI Generated an Image of: {m.message}",
            } for m in st.session_state.chat_history[-message_context_length:]]

            try:
                chat_completion = anthropic_client.messages.create(
                    model="claude-3-haiku-20240307",
                    max_tokens=1024,
                    messages=message_history,
                )
                response = chat_completion.content[0].text

                # Add generated image to chat history
                add_chat_instance(type_of="Text", author="AI", message=response)
            except Exception as e:
                add_chat_instance(type_of="Error", author="AI", message="This Request to AI has Failed. Please Check API Key/s.")

    # Render the chat history (if exists)
    if len(st.session_state.chat_history) > 0:
        st.write("## Chat History:")

    render_chat_history()
