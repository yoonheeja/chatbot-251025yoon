import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("💬 응답하라 ESG")
st.write(
    "이 앱은 OpenAI의 GPT-3.5 모델을 사용한 esg에 대해 응답하는 간단한 챗봇입니다. "
    "사용하려면 OpenAI API 키가 필요하며, [여기서](https://platform.openai.com/account/api-keys) 받을 수 있습니다. "
    "또한 [튜토리얼](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps)을 따라 단계별로 만드는 방법을 배울 수 있습니다."
)


# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    # ✅ 이 아래부터는 모두 4칸 들여쓰기!
    client = OpenAI(api_key=openai_api_key)

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "당신은 전문적인 ESG 컨설턴트입니다. 사용자의 질문에 ESG 전문가의 관점에서 답변하세요."}
        ]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("esg에 대해서 무엇이든 물어보세요"):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages,
            stream=True,
        )

        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
