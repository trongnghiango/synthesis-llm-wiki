# TIPS: CÁCH QUẢN LÝ VÀ ĐIỀU KHIỂN AGENTIC AI

Tài liệu này dành cho Developer (Con người) để đảm bảo các AI Agent luôn tuân thủ kỷ luật dự án, không "đi tắt", không trốn tránh quy trình và luôn hành động trong ranh giới của Hiến pháp.

## 1. Lệnh Ép Tuân Thủ (Enforcement Commands)

Khi bắt đầu một phiên làm việc mới hoặc một task mới, hãy sử dụng các câu lệnh sau để "thiết lập lại" tư duy kỷ luật của AI:

- **"Trước khi làm bất cứ điều gì, hãy quét `docs/RULES.md` và cho tôi biết task này chịu sự chi phối của những bộ luật nào."**
- **"Dừng lại! Bạn đã tạo Context Folder cho task này chưa? Nếu chưa, hãy làm đúng quy trình trước khi đề xuất code."**
- **"Hãy tự audit (kiểm tra) hành động vừa rồi của bạn đối với file `standards/team_workflow.md`. Bạn có bỏ sót bước nào không?"**

## 2. Các "Cổng Kiểm Soát" (Control Gates)

Đừng để AI tự tiện sửa code. Hãy bắt chúng đi qua các cổng sau:

- **Cổng 1: Implementation Plan**: Luôn yêu cầu AI tạo file `01_implementation_plan.md` trong thư mục context. Chỉ khi bạn gõ "Proceed" hoặc "Approved" thì AI mới được phép sửa file code.
- **Cổng 2: Task Checklist**: Yêu cầu AI cập nhật `02_task.md` sau mỗi Batch thay đổi. Nếu AI báo "Xong" mà chưa cập nhật checklist, hãy bác bỏ kết quả.
- **Cổng 3: Archiving**: Khi kết thúc task, nếu AI không tự di chuyển context sang `history/`, đó là dấu hiệu của sự cẩu thả. Hãy yêu cầu thực hiện ngay.

## 3. Dấu hiệu AI đang "Trốn Luật" (Red Flags)

Hãy cảnh giác nếu AI:
1. **Hứa "Rút kinh nghiệm" nhưng không sửa đổi file quy trình**: Đây là cách AI "xoa dịu" con người. Hãy bắt AI thực hiện hành động sửa lỗi cụ thể vào file context/history ngay lập tức.
2. **Sửa code trước khi lập kế hoạch**: AI đang cố gắng làm nhanh để lấy kết quả mà bỏ qua tính bền vững của tài liệu.
3. **Quên cập nhật tài liệu**: AI thường tập trung vào logic lập trình mà quên mất "Hợp đồng API" hay "Quy tắc kiến trúc".

## 4. Kỹ thuật "Truy cứu trách nhiệm"

Nếu AI làm sai quy trình, đừng chỉ nói "Bạn làm sai rồi". Hãy nói:
> "Hành động vừa rồi của bạn vi phạm **Nguyên tắc số X** trong `RULES.md`. Hãy đình chỉ việc code, thực hiện các bước quản lý context còn thiếu, và giải trình tại sao bạn lại bỏ qua bước đó."

## 5. Quy tắc Commit

Yêu cầu AI:
- Không commit gộp tất cả vào một lần.
- Phải phân tách commit theo logic: Docs riêng, Feature riêng, Refactor riêng.
- Sử dụng **Conventional Commits** (feat, fix, docs, refactor, chore).

---
*Ghi chú: AI rất giỏi, nhưng AI chỉ thực sự hiệu quả khi có một người quản lý (Orchestrator) nghiêm khắc và một hệ thống luật lệ (Constitution) chặt chẽ.*
