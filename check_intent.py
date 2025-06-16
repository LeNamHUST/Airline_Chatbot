# def handle_intent(intent, entities):
#     if intent == "book_flight":
#         return handle_book_flight(entities)
#     elif intent == "ask_tax_policy":
#         return handle_tax_policy(entities)
#     elif intent == "ask_refund_policy":
#         return handle_refund_policy(entities)
#     else:
#         return "Xin lỗi, tôi chưa hỗ trợ yêu cầu này."
#
# def handle_book_flight(entities):
#     from_city = entities.get("departure_city", "không rõ")
#     to_city = entities.get("destination_city", "không rõ")
#     date = entities.get("departure_date", "chưa xác định")
#
#     # Ở đây bạn có thể gọi tìm kiếm từ dữ liệu CSV chuyến bay
#     return f"Đang tìm vé máy bay từ **{from_city}** đến **{to_city}** vào **{date}**..."
#
# def handle_tax_policy(entities):
#     adult = entities.get("passenger_adult", 1)
#     child = entities.get("passenger_child", 0)
#     return f"Chính sách thuế cho {adult} người lớn và {child} trẻ em như sau: [...]"
#
# def handle_refund_policy(entities):
#     return "Chính sách hoàn vé: Vé tiết kiệm không hoàn tiền, vé linh hoạt hoàn được với phí 300,000đ/vé."
