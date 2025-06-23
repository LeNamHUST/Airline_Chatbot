import streamlit as st
from chain.booking_chain import handle_intent
from utils.vector_db import rag
from utils.utils import *
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI


api_key=''


llm = ChatOpenAI(model="gpt-4o", temperature=0.0, openai_api_key=api_key)

if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(return_messages=True)

memory = st.session_state.memory

conversation_chain = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=True
)

with open("prompt/booking_prompt.txt", "r", encoding="utf-8") as f:
    prompt_book = f.read()

with open("prompt/tax_prompt.txt", "r", encoding="utf-8") as f:
    prompt_tax = f.read()


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
    memory.chat_memory.add_user_message(user_input)
    st.session_state.messages.append({"role":"user", "content":user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Đang xử lý..."):

            try:
                prompt = prompt_book + f"""
                    Phân tích câu sau:
                    "{user_input}"
                    Trả về định dạng:
                    Intent: <intent>
                    Entities:
                      - <entity>: <value>
                    """

                output = call_llm(prompt, api_key)
                print('===> DEBUG: output:', output)

                # st.write("### Kết quả từ LLM:")
                # st.code(output)

                # Xử lý kết quả trả về từ mô hình
                intent, entities = parse_output(output)
                if "flight_infor" not in st.session_state:
                    st.session_state.flight_infor = {}
                st.session_state.flight_infor.update(entities)
                print('st.session_state.flight_infor:',st.session_state.flight_infor)
                message, flight_df = handle_intent(intent, entities)
                print('message:', message)
                if flight_df is not None and not flight_df.empty:
                    st.session_state["flight_df"] = flight_df
                    st.session_state["show_flights"] = True
                elif message == "Giá vé này chưa bao gồm thuế ạ, bạn có muốn mình tính giúp giá vé đã bao gồm thuế không ạ?":
                    st.markdown(message)
                    st.session_state.messages.append({"role": "assistant", "content": message})
                    memory.chat_memory.add_ai_message(message)
                elif message == "yes":
                    print('memory.buffer:', memory.buffer)
                    prompt = f"""Dưới đây là đoạn hội thoại giữa người dùng và trợ lý:
                                {memory.buffer}
                                Câu cuối cùng của người dùng là: có
                                Dựa vào ngữ cảnh hội thoại trước đó, hãy xác định người dùng đang đồng ý điều gì?
                                Chỉ trả lời ngắn gọn, ví dụ: tính thuế, ..."""
                    output = call_llm(prompt, api_key)
                    print('output:', output)
                    if output == "tính thuế":
                        adults = st.session_state.flight_infor.get("passenger_adult", 0)
                        children = st.session_state.flight_infor.get("passenger_child", 0)
                        cost = st.session_state.flight_infor.get("cost", 0)
                        if adults == 0 and children == 0:
                            response_bot = "Bạn có thể cung cấp số lượng vé người lớn và vé trẻ em giúp mình được không?"
                            st.markdown(response_bot)
                            st.session_state.messages.append({"role": "assistant", "content": response_bot})
                            memory.chat_memory.add_ai_message(response_bot)
                        else:
                            print('gọi đến hàm tính thuế 1')
                            fee_total = calculator_tax(int(cost), int(adults), int(children))
                            response_bot = f"Bạn đặt {adults} cho người lớn và {children} cho trẻ em, với thuế cho người lớn là 10%, thuế cho trẻ em là 5% thì tổng số tiền bạn cần thanh toán là {int(fee_total)} VND"
                            st.markdown(response_bot)
                            st.session_state.messages.append({"role": "assistant", "content": response_bot})
                            memory.chat_memory.add_ai_message(response_bot)
                elif message == "Tính thuế":
                    print('gọi đến hàm tính thuế 2')
                    adults = st.session_state.flight_infor.get("passenger_adult", 0)
                    children = st.session_state.flight_infor.get("passenger_child", 0)
                    cost = st.session_state.flight_infor.get("cost", 0)
                    fee_total = calculator_tax(int(cost), int(adults), int(children))
                    response_bot = f"Bạn đặt {adults} cho người lớn và {children} cho trẻ em, với thuế cho người lớn là 10%, thuế cho trẻ em là 5% thì tổng số tiền bạn cần thanh toán là {int(fee_total)} VND"
                    st.markdown(response_bot)
                    st.session_state.messages.append({"role": "assistant", "content": response_bot})
                    memory.chat_memory.add_ai_message(response_bot)
                elif message == "Hỏi về hoàn vé" or message == "Hỏi về thú cưng":
                    response_bot = rag(user_input)
                    st.markdown(response_bot)
                    st.session_state.messages.append({"role": "assistant", "content": response_bot})
                    memory.chat_memory.add_ai_message(response_bot)

                else:
                    print('input:', user_input)
                    response = conversation_chain.invoke({"input": user_input})
                    memory.chat_memory.add_ai_message(response['response'])
                    print('response:', response)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})

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
                memory.chat_memory.add_ai_message(confirm_message)
                st.success(confirm_message)
                st.session_state["chosen_flight"] = flight.to_dict()
                st.session_state.messages.append({"role": "assistant", "content": confirm_message})
                # Sau khi xác nhận xong, ẩn giao diện chọn chuyến bay
                st.session_state["show_flights"] = False
                entities = st.session_state.flight_infor
                entities["cost"] =  flight["cost"]
                st.session_state.flight_infor.update(entities)
            else:
                st.warning("Không tìm thấy chuyến bay đã chọn.")

