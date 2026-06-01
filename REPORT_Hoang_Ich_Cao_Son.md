# Báo Cáo Cá Nhân: Lab 3 - Chatbot vs ReAct Agent

- **Họ tên sinh viên**: Hoàng Ích Cao Sơn
- **Mã sinh viên**: 2A202600553 - Nhóm Lab03
- **Ngày**: 2026-06-01

---

## I. Đóng Góp Kỹ Thuật (15 điểm)

- **Công việc cá nhân phụ trách**: Thiết kế Trace và đánh giá Chatbot vs Agent.
- **Module liên quan**: `chatbot.py`, `src/telemetry/logger.py`, `src/telemetry/metrics.py`, `logs/2026-06-01.log`
- **Bằng chứng trong code/log**:
  - `chatbot.py` có danh sách test cases baseline cho các tình huống đặt vé.
  - `IndustryLogger.log_event()` ghi log dạng JSON với `timestamp`, `event`, và `data`.
  - `PerformanceTracker.track_request()` ghi provider, model, token usage, latency và cost estimate.
  - `logs/2026-06-01.log` có các event `CHATBOT_CASE_START`, `LLM_METRIC`, và `CHATBOT_CASE_END`.

Phần đóng góp tập trung vào observability và đánh giá. Baseline chatbot được chạy qua các case chuyến bay, sau đó hệ thống ghi lại latency, token count và mock cost. Các số liệu này dùng để so sánh với agent sau khi ReAct loop hoàn thiện.

**Lưu ý kiểm tra thực tế**: Trace cho chatbot baseline đã có thật trong log. Trace đầy đủ cho agent chưa có vì `ReActAgent.run()` chưa thực thi tool thật. Vì vậy phần đánh giá Chatbot vs Agent hiện là đánh giá baseline thật kết hợp với kết quả agent kỳ vọng theo thiết kế.

---

## II. Case Debugging (10 điểm)

- **Mô tả vấn đề**: Baseline chatbot sinh câu trả lời mà không có tool, dẫn đến khó xác minh câu trả lời có đúng dữ liệu `flight_data.py` hay không.
- **Nguồn log**: `logs/2026-06-01.log`.
- **Chẩn đoán**: Log cho thấy baseline đã gọi Gemini và ghi metric, nhưng không có event nào thể hiện tool call hoặc Observation. Điều này xác nhận baseline chỉ là LLM direct answer.
- **Cách khắc phục đề xuất**: Khi hoàn thiện agent, cần log thêm `AGENT_STEP`, `TOOL_CALL`, `TOOL_RESULT`, `PARSER_ERROR`, và `FINAL_ANSWER` để trace được toàn bộ Thought-Action-Observation.

---

## III. Nhận Xét Cá Nhân: Chatbot vs ReAct (10 điểm)

1. **Reasoning**: Chatbot trả lời một lần nên nhanh về mặt flow, nhưng thiếu quá trình kiểm chứng. ReAct agent chậm hơn vì có nhiều bước, nhưng mỗi bước có thể được trace.
2. **Reliability**: Agent chỉ tốt hơn chatbot khi tool execution thật sự hoạt động. Nếu agent loop còn skeleton, chatbot vẫn là phần duy nhất có log thực nghiệm.
3. **Observation**: Observation giúp biến trace thành bằng chứng. Khi có tool result, người đánh giá có thể kiểm tra vì sao agent chọn chuyến bay hoặc tính ra giá đó.

---

## IV. Cải Tiến Tương Lai (5 điểm)

- **Scalability**: Chuẩn hóa log schema cho cả chatbot và agent để dễ tổng hợp bằng script.
- **Safety**: Ghi lại lỗi tool và lỗi parser để không che giấu failure.
- **Performance**: Thêm dashboard tính average latency, P50/P99, tổng token, cost và success rate theo từng phiên chạy.

---

