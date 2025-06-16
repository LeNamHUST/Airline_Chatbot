import streamlit as st
import pandas as pd
from langchain.prompts import PromptTemplate
from langchain_community.llms import LlamaCpp
from langchain_core.runnables import RunnableSequence
from openai import OpenAI
from chain.booking_chain import handle_intent
from utils.utils import *

OPENAI_API_KEY = ""
client = OpenAI(api_key=OPENAI_API_KEY)
messages = [{"role": "system", "content": "You are a intelligent assistant."}]

with open("prompt/extract_prompt.txt", "r", encoding="utf-8") as f:
    question = f.read()


st.set_page_config(page_title="Trợ lý đặt vé máy bay ✈")

st.title("Trợ lý đặt vé máy bay ✈")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "👋 Chào bạn! Mình có thể giúp gì cho bạn về vé máy bay?"}
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Nhập nội dung ...")

if user_input:
    st.session_state.messages.append({"role":"user", "content":user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Đang xử lý..."):

            try:
                question = question + f"""
                    Phân tích câu sau:
                    "{user_input}"
                    Trả về định dạng:
                    Intent: <intent>
                    Entities:
                      - <entity>: <value>
                    """
                if question:
                    messages.append(
                        {"role": "user", "content": question},
                    )
                    chat = client.chat.completions.create(
                        model="gpt-4o",
                        messages=messages,
                        temperature=0.0,
                        top_p=0.1
                    )
                # chain = prompt | llm
                print('chat:', chat)
                output = chat.choices[0].message.content
                print('===> DEBUG: output:', output)

                # st.write("### Kết quả từ LLM:")
                # st.code(output)

                # Xử lý kết quả trả về từ mô hình
                intent, entities = parse_output(output)

                message, flight_df = handle_intent(intent, entities)

                if flight_df is not None and not flight_df.empty:
                    st.session_state["flight_df"] = flight_df
                    st.session_state["show_flights"] = True
                else:
                    st.markdown(message)
                    st.session_state.messages.append({"role": "assistant", "content": message})

            except Exception as e:
                st.error(f"Đã xảy ra lỗi: {e}")
                import traceback
                st.code(traceback.format_exc())

if st.session_state.get("show_flights", False):
    df = st.session_state["flight_df"]
    st.markdown("#### Có các chuyến bay sau:")

    options = [
        f"{row['flight_id']} - {row['datetime']} - {row['cost']:,} VND"
        for idx, row in df.iterrows()
    ]
    selected = st.selectbox("Chọn chuyến bay:", options, key="selected_flight")
    st.session_state["selected_id"] = selected.split(" - ")[0]

    if st.button("✈ Xác nhận chuyến bay"):
        sid = st.session_state.get("selected_id", None)
        if sid:
            chosen_flight = df[df["flight_id"] == sid]
            if not chosen_flight.empty:
                flight = chosen_flight.iloc[0]
                confirm_message = (
                    f"✅ Bạn đã chọn chuyến bay: {flight['flight_id']} từ {flight['from_city']} "
                    f"đến {flight['to_city']} lúc {flight['datetime']} với giá {flight['cost']:,} VND"
                )
                st.success(confirm_message)
                st.session_state["chosen_flight"] = flight.to_dict()
                st.session_state.messages.append({"role": "assistant", "content": confirm_message})
                # Sau khi xác nhận xong, ẩn giao diện chọn chuyến bay
                st.session_state["show_flights"] = False
            else:
                st.warning("Không tìm thấy chuyến bay đã chọn.")

