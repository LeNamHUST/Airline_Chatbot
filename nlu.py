from langchain.prompts import PromptTemplate
from langchain_community.llms import LlamaCpp
from langchain_core.runnables import RunnableSequence


llm = LlamaCpp(
    model_path="models/capybarahermes-2.5-mistral-7b.Q2_K.gguf",
    n_ctx=4096,
    verbose=True
)
prompt = PromptTemplate.from_template("""
Bạn là một trợ lý bán vé máy bay giúp nhận diện ý định và thực thể trong câu tiếng Việt.

Ví dụ:
Đầu vào: "Tôi muốn đặt vé máy bay từ Hà Nội đến Đà Nẵng vào ngày mai"

Kết quả:
Intent: book_flight
Entities:
  - departure_city: Hà Nội
  - destination_city: Đà Nẵng
  - departure_date: ngày mai
  
Đầu vào: "Quy định về thuế khi mua vé cho 2 người lớn và 2 trẻ em"

Kết quả:
Intent: ask_tax_policy
Entities:
  - passenger_adult: 2
  - passenger_child: 2
Phân tích câu sau:
"{user_input}"
Trả về định dạng:
Intent: <intent>
Entities:
  - <entity>: <value>
""")
chain = prompt | llm
output = chain.invoke({"user_input": "Tôi muốn đặt vé từ Hà Nội đi Đà Nẵng ngày mai"})
print(output)
