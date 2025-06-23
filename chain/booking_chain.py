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
        passenger_adult = int(entities.get("passenger_adult")) if entities.get("passenger_adult") is not None else None
        passenger_child = int(entities.get("passenger_child")) if entities.get("passenger_child") is not None else None
        print('date_obj:', date_obj)

        if not from_city and to_city:
            return "Thiếu điểm khởi hành", None
        elif from_city and not to_city:
            return "Thiếu điểm đến", None
        elif not from_city and not to_city:
            return "Tính thuế", None
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
            return "Xin lỗi, mình không tìm thấy chuyến bay phù hợp", None
        else:
            return "Chuyến bay phù hợp", results[["flight_id", "from_city", "to_city", "datetime", "cost"]]
    elif intent == "ask_tax":
        return "Giá vé này chưa bao gồm thuế ạ, bạn có muốn mình tính giúp giá vé đã bao gồm thuế không ạ?", None
    elif intent == "yes":
        return "yes", None
    elif intent == "no":
        return "no", None
    elif intent == "ask_refund_policy":
        return "Hỏi về hoàn vé", None
    elif intent == "ask_pet_policy":
        return "Hỏi về thú cưng", None
    else:
        return "Câu này khó quá mình chưa biết trả lời bạn như thế nào", None