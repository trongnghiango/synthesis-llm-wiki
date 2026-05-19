---
name: stax-quick-task
description: "Xử lý task nhỏ, sửa bug, hoặc fix lỗi từ naming-auditor. Code nhanh, tuân thủ Clean Architecture, có cơ chế chặn over-scope và update-safety. Ghi log vào CHANGELOG."
risk: low
source: custom-stax-team
date_added: "2026-05-09"
version: "1.1.0"
---

# STAX Quick Task & Micro-feature Implementation

## Purpose

Thực thi nhanh gọn các yêu cầu nhỏ lẻ (thêm field, thêm endpoint, sửa bug) trên các module CÓ SẴN.
Bỏ qua quy trình sinh tài liệu Context rườm rà để tối ưu tốc độ, nhưng **TUÂN THỦ TUYỆT ĐỐI** kiến trúc STAX và có cơ chế bảo vệ dự án khỏi tình trạng Scope Creep (phình to yêu cầu).

---

## Operating Modes (Chế độ đầu vào)

Khi bắt đầu, hãy xác định bạn đang ở chế độ nào:

1. **Standard Mode (Task nhỏ thông thường):** User đưa ra một yêu cầu sửa đổi/thêm mới bằng văn bản.
2. **Fix Mode (Handoff từ stax-naming-auditor):** User cung cấp một "Audit Manifest". 
   👉 *Hành vi bắt buộc:* Bạn KHÔNG phân tích lỗi từ đầu. Hãy đọc Manifest (chứa Severity, File, Dòng, Breaking Change flag) và trực tiếp map các đề xuất sửa chữa vào code. Đặc biệt chú ý cờ `Breaking Change` để xử lý tương thích ngược nếu có.

---

## The Workflow (Quy trình Nhanh 3 Bước)

### Bước 1: Analysis & Scope Gate (Phân tích & Chặn Over-scope)

Khi nhận yêu cầu, BẮT BUỘC rà soát nhanh codebase và trả lời trong **1 tin nhắn duy nhất**:
- Lỗi/Tính năng này nằm ở file nào? (Hoặc list file từ Audit Manifest).
- Phương án sửa/thêm mới là gì? (Bullet points ngắn gọn).
- 🛑 **GATE CHỐNG OVER-SCOPE:** Nếu phương án yêu cầu tạo Module mới hoàn toàn, sửa đổi cấu trúc Database lõi, hoặc chạm vào **nhiều hơn 3 files logic**, bạn BẮT BUỘC phải DỪNG LẠI và phản hồi: *"Yêu cầu này vượt quá scope của quick-task. Hãy dùng skill `stax-feature-implementation` để đảm bảo an toàn kiến trúc."*

👉 _Nếu pass Scope Gate, hỏi User: "Phương án này OK chưa để tôi bắt đầu code?"_

### Bước 2: Coding & Anti-Creep (Thực thi & Chặn phình task)

Sau khi User đồng ý, tiến hành viết code tuân thủ **Luật Thép STAX** bên dưới.
🛑 **ANTI-SCOPE CREEP:** Nếu trong quá trình này User bổ sung thêm các yêu cầu mới không có trong thỏa thuận ở Bước 1, bạn BẮT BUỘC TỪ CHỐI code tiếp các phần mới, cảnh báo User về Scope Creep và yêu cầu hoàn thành task hiện tại trước.

### Bước 3: Quick Logging (Ghi chú thay đổi)

Sau khi hoàn thiện code, KHÔNG tạo thư mục docs mới.
Mở file (hoặc tạo nếu chưa có) theo **đúng đường dẫn này**: `docs/STAX/06_CHANGELOG.md`

Thêm một mục mới lên ĐẦU file theo định dạng chuẩn:

### [YYYY-MM-DD] - {Tên Task Ngắn Gọn}
- **Module:** `tên-module`
- **Loại:** `Feature` | `Bugfix` | `Auditor-Fix`
- **Thay đổi:**
  - Thêm field `x` vào schema `y`.
  - Cập nhật service `z` để xử lý logic mới.

---

## STAX Hard Constraints (5 Luật Thép Không Thể Vi Phạm)

Dù task nhỏ đến đâu, BẮT BUỘC tuân thủ:

1. **No Framework Leakage:** Cấm ném `BadRequestException`, `NotFoundException` ở tầng Domain/Application. Phải ném `EntityNotFoundException` hoặc `BusinessRuleValidationException` từ `core/shared`.
2. **Transaction Management:** Nếu ghi vào từ 2 bảng trở lên, bắt buộc bọc trong `this.txManager.runInTransaction(async (tx) => { ... })`.
3. **DTO Strictness:** Cấm trả về Entity thô hoặc Drizzle Record ra ngoài API. Phải đi qua Mapper hoặc Response DTO.
4. **No Magic Strings:** Trạng thái/phân loại phải dùng TypeScript Enum và pgEnum.
5. **Update Safety (Bảo vệ dữ liệu):** Khi thực hiện thao tác UPDATE, tuyệt đối không được ghi đè các trường immutable. BẮT BUỘC sử dụng pattern `mapToUpdate()` (hoặc loại bỏ thủ công `id`, `createdAt`, `organizationId` khỏi payload) trước khi đẩy vào Database.

---

## Exit Criteria (Điều kiện hoàn thành)

Quy trình chỉ được xem là kết thúc khi đạt ĐỦ các tiêu chí đo lường sau:
1. Code chạy qua lệnh `npm run build` thành công (không có warning do thay đổi này gây ra).
2. Code mới thêm KHÔNG sử dụng type `any`.
3. Chạy unit tests liên quan pass xanh và KHÔNG xuất hiện `console.error` trong log của test.
4. Có đúng 1 entry log tóm tắt được thêm vào file `docs/STAX/06_CHANGELOG.md`.