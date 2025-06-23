from datetime import datetime, timedelta
from openai import OpenAI
import unicodedata
import re

# format time
def parse_date(date_str):
    print('date_str:',date_str)
    now = datetime.now()
    if "ngày mai" in date_str:
        date = now + timedelta(days=1)
    elif "hôm nay" in date_str:
        date = now
    else:
        try:
            return datetime.strptime(date_str, "%d/%m/%Y %H:%M")
        except:
            return None

    if "tối" in date_str:
        print('date:', date_str)
        return date.replace(hour=20, minute=0)
    elif "sáng" in date_str:
        return date.replace(hour=8, minute=0)
    else:
        return date.replace(hour=12, minute=0)

def remove_vn_tones(text):
    text = unicodedata.normalize('NFD', text)
    text = ''.join(char for char in text if unicodedata.category(char) != 'Mn')
    return text

def parse_output(content: str):
    intent_match = re.search(r"Intent:\s*(\w+)", content)
    intent = intent_match.group(1) if intent_match else None

    # Trích xuất entities
    entities = re.findall(r"-\s*(\w+):\s*(.+)", content)

    # Đưa vào dict
    entity_dict = {key: value for key, value in entities}

    return intent, entity_dict

def call_llm(prompt, api_key):
    client = OpenAI(api_key=api_key)
    messages = [{"role": "system", "content": "You are a intelligent assistant."}]
    if prompt:
        messages.append(
            {"role": "user", "content": prompt},
        )
        chat = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.0,
            top_p=0.1
        )
    response_llm = chat.choices[0].message.content
    return response_llm

def calculator_tax(cost, passage_adult, passage_child):
    return passage_adult*cost*1.1 + passage_child*cost*1.05
