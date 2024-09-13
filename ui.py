import asyncio
import base64
import tempfile

import edge_tts
import streamlit as st


async def synthesize_text(text: str, voice: str) -> str:
    communicate = edge_tts.Communicate(text, voice)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
        await communicate.save(tmp_file.name)
        return tmp_file.name


def run_ui():
    st.title("Text-to-Speech with Edge TTS")

    text = st.text_area("Enter text to synthesize")

    voices = asyncio.run(edge_tts.list_voices())

    voice_options = [voice['ShortName'] for voice in voices]
    voice = st.selectbox("Select voice", voice_options)

    if st.button("Synthesize"):
        if text and voice:
            st.write("Synthesizing...")
            try:
                audio_file = asyncio.run(synthesize_text(text, voice))
                st.audio(audio_file, format='audio/mp3')
                st.success("Audio synthesized successfully")

                with open(audio_file, "rb") as file:
                    b64 = base64.b64encode(file.read()).decode()
                    href = f'<a href="data:audio/mp3;base64,{b64}" download="output.mp3">Download audio</a>'
                    st.markdown(href, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.error("Please fill in all fields")


if __name__ == "__main__":
    run_ui()
