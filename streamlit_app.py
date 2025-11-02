import os
import json
from dotenv import load_dotenv, find_dotenv
from pathlib import Path
import streamlit as st

from validating_ideas import AppIdeaValidator, create_app_validator, execute_validation


def ensure_env_loaded() -> None:
    dotenv_path = find_dotenv(usecwd=True) or str(Path(__file__).resolve().parent.joinpath(".env"))
    load_dotenv(dotenv_path, override=True)
    if not os.getenv("OPENROUTER_API_KEY"):
        st.error(f"OPENROUTER_API_KEY não encontrada. Verifique seu .env em: {dotenv_path}")


def main():
    st.set_page_config(page_title="Validador de Ideias de App", page_icon="💡", layout="centered")
    st.title("💡 Validador de Ideias de Aplicativo")

    ensure_env_loaded()

    with st.form("idea_form"):
        idea = st.text_area(
            "Descreva a ideia do seu aplicativo",
            value="Um aplicativo de produtividade para sessões de trabalho focadas",
            height=120,
        )
        session_id = idea.lower().replace(" ", "-")[:64]
        submitted = st.form_submit_button("Validar ideia")

    if submitted:
        if not idea.strip():
            st.warning("Por favor, descreva a ideia do seu aplicativo.")
            return

        with st.spinner("Analisando sua ideia e gerando relatório..."):
            try:
                validator: AppIdeaValidator = create_app_validator(session_id)
                result = validator.run(app_idea=idea)
            except Exception as e:
                st.error(f"Erro ao executar validação: {e}")
                return

        if result and getattr(result, "content", None):
            st.markdown("### 📄 Relatório")
            st.markdown(result.content)
            if st.download_button("Baixar relatório (.md)", data=result.content, file_name=f"relatorio_{session_id}.md", mime="text/markdown"):
                pass
        else:
            st.info("Nenhum conteúdo retornado pelo validador.")


if __name__ == "__main__":
    main()


