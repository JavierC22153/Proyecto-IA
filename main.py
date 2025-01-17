from backend.cores import run_llm
import streamlit as st
from streamlit_chat import message

st.header("LangChain - Documentation Helper Bot")

# Input para el prompt
prompt = st.text_input("Prompt", placeholder="Enter your prompt here")

# Inicializar el estado de la sesión si es necesario
if "chat_answers_history" not in st.session_state:
    st.session_state["chat_answers_history"] = []
if "user_prompt_history" not in st.session_state:
    st.session_state["user_prompt_history"] = []
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []


# Crear cadena de fuentes desde URLs
def create_sources_string(source_urls: set[str]) -> str:
    if not source_urls:
        return ""
    sources_list = list(source_urls)
    sources_list.sort()
    sources_string = "Sources:\n"
    for i, source in enumerate(sources_list):
        sources_string += f"{i + 1}. {source}\n"
    return sources_string


# Si se introduce un prompt
if prompt:
    with st.spinner("Generating response..."):
        generated_response = run_llm(
            query=prompt,
            chat_history=st.session_state["chat_history"]
        )
        # Obtener las fuentes desde los metadatos de los documentos
        sources = set([doc.metadata["source"] for doc in generated_response["source"]])
        formatted_response = f"{generated_response['result']}\n\n{create_sources_string(sources)}"

        # Actualizar historial de la sesión
        st.session_state["user_prompt_history"].append(prompt)
        st.session_state["chat_answers_history"].append(formatted_response)
        st.session_state["chat_history"].append(("human", prompt))
        st.session_state["chat_history"].append(("ai", generated_response["result"]))

# Mostrar el historial de mensajes en el chat
if st.session_state["chat_answers_history"]:
    for i, (generated_response, user_query) in enumerate(
            zip(st.session_state["chat_answers_history"], st.session_state["user_prompt_history"])):
        message(user_query, is_user=True, key=f"user_{i}")  # Asignar un key único para cada mensaje del usuario
        message(generated_response, key=f"ai_{i}")  # Asignar un key único para cada mensaje generado