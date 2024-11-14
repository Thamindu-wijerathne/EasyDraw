import streamlit as st
from PIL import Image
import time
def mainIU():
    # Set page configuration
    st.set_page_config(page_title="Creativity at Your Fingertips", layout="wide")

    # Header
    st.markdown("""
        <div style="text-align: center;">
            <h1>Creativity at Your Fingertips<br> Unlocking Imagination with Every Gesture</h1>
        </div>
    """, unsafe_allow_html=True)

    # Middle Section
    col1, col2 = st.columns(2)

    # Block-1 (input cam and output pic)
    with col1:
        st.markdown('<div style="text-align: center;"><div class="card-1"></div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div style="text-align: center;"><div class="card-1"></div></div>', unsafe_allow_html=True)

    # Block-2 (Instructions)
    st.markdown("""
        <div class="block-2">
            <p>
            <b>Instructions:</b>
            <ul>
                <li>Index Finger : Use to draw lines</li>
                <li>Index Finger + Middle Finger : To idle and move fingers across display</li>
                <li>Index Finger + Middle Finger + Ring Finger : Delete the drawing</li>
                <li>All Fingers : To post picture</li>
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Footer
    st.markdown("<div class='footer'></div>", unsafe_allow_html=True)



    # Custom CSS for styling
    st.markdown("""
        <style>
        * {
            font-family: 'Ubuntu', sans-serif;
            background-color: #000000;
            color : white;
        }
        h1 {
            text-align: center;
        }
        li {
            margin-bottom: 10px;
        }
        .block-1 {
            display: flex;
            gap: 20px;
            margin: 20px 0;
            justify-content: center;
            align-items: center;
        }
        .card-1 {
            background-color: #444444;
            padding: 20px;
            border-radius: 8px;
        }
        </style>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    mainIU()