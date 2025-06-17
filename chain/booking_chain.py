from utils.utils import parse_date, remove_vn_tones
import pandas as pd



df = pd.read_csv(r"C:\Users\Nam Dao\Desktop\chatbot\data\full_flight_schedule_july_2025.csv")


df["datetime"] = pd.to_datetime(df["datetime"], format="%m/%d/%Y %H:%M:%S", errors="coerce")


def handle_intent(intent, entities):
    print('entities:',entities)
    if intent == "book_flight":
        from_city = remove_vn_tones(entities.get("departure_city")) if entities.get("departure_city") is not None else None
        to_city = remove_vn_tones(entities.get("destination_city")) if entities.get("destination_city") is not None else None
        date_text = entities.get("departure_date") or entities.get("departure_time") or ""
        date_obj = parse_date(date_text)
        print('date_obj:', date_obj)

        if not from_city or not to_city:
            return "Không thể xác định thông tin chuyến bay.", None
        print('from_city:', from_city)
        print('to_city:', to_city)
        if date_obj is not None:
            results = df[
                (df["from_city"].str.lower() == from_city.lower()) &
                (df["to_city"].str.lower() == to_city.lower()) &
                (df["datetime"].dt.date == date_obj.date())
            ]
        else:
            results = df[
                (df["from_city"].str.lower() == from_city.lower()) &
                (df["to_city"].str.lower() == to_city.lower())
                ]

        if results.empty:
            return "Xin lỗi, mình không tìm thấy chuyến bay phù hợp.", None
        else:
            return "Chuyến bay phù hợp", results[["flight_id", "from_city", "to_city", "datetime", "cost"]]
    elif intent == "ask_tax":
        return "Giá vé này chưa bao gồm thuế ạ, Anh (chị) có muốn em tính giúp giá vé đã bao gồm thuế không ạ?", None
    elif intent == "yes":
        return "yes", None
    elif intent == "no":
        return "no", None
    else:
        return "Câu này khó quá mình chưa biết trả lời bạn như thế nào", None