import streamlit as st
from streamlit.delta_generator import DeltaGenerator


# Source: https://arnaudmiribel.github.io/streamlit-extras/extras/bottom_container/#summary
def bottom() -> DeltaGenerator:
    """
    Insert a multi-element container that sticks to the bottom of the app.

    Note that this can only be in the main body of the app, and not in
    other parts e.g. st.sidebar
    """
    if hasattr(st, "_bottom"):
        return st._bottom
    else:
        raise Exception(
            "The bottom container is not supported in this Streamlit version."
        )