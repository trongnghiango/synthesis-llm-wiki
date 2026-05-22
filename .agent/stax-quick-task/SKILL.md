---
name: stax-quick-task
description: "Xử lý task nhỏ, sửa bug, hoặc fix lỗi từ naming-auditor. Code nhanh, tuân thủ Clean Architecture, có cơ chế chặn over-scope và update-safety. Ghi log vào CHANGELOG."
risk: low
source: custom-stax-team
date_added: "2026-05-09"
version: "2.0.0"
---

# STAX Quick Task & Micro-feature Implementation

## 1. Mục đích

Thực thi nhanh gọn các yêu cầu nhỏ lẻ (thêm field, thêm endpoint, sửa bug) trên các module CÓ SẴN.

Bỏ qua quy trình sinh tài liệu Context rườm rà để tối ưu tốc độ, nhưng **TUÂN THỦ TUYỆT ĐỐI** kiến trúc STAX và có cơ chế bảo vệ dự án khỏi Scope Creep.

---

## 2. Chế độ Đầu vào (Operating Modes)

Khi bắt đầu, xác định chế độ:

**Mode 1 — Standard (Task nhỏ thông thường):**
User đưa ra yêu cầu sửa đổi/thêm mới bằng văn bản.

**Mode 2 — Fix (Handoff từ stax-naming-auditor):**
User cung cấp một "Audit Manifest" (`02_fix_manifest.md`).

> *Hành vi bắt buộc Mode 2:* KHÔNG phân tích lỗi từ đầu. Đọc Manifest trực tiếp và map các đề xuất sửa chữa vào code. Đặc biệt chú ý cờ `Breaking Change` để xử lý tương thích ngược.

---

## 3. Quy trình Nhanh 3 Bước

### Bước 1: Pre-Scope Check & Analysis (Phân tích & Chặn Over-scope)

**[BẮTT BUỘC TRƯỚC KHI ESTIMATE]** — Chạy lệnh search thực tế, KHÔNG tự estimate bằng trí nhớ:

```bash
# Tìm tất cả file bị ảnh hưởng bởi symbol/function/type cần sửa
grep -r "[tên symbol/function/type]" src/ --include="*.ts" -l

# Dán kết quả vào chat. Số dòng output = số file thực tế bị ảnh hưởng.
```

Sau khi có kết quả grep, trả lời trong **1 tin nhắn duy nhất**:
- Lỗi/Tính năng này nằm ở file nào?
- Phương án sửa/thêm mới là gì? (Bullet points ngắn gọn)
- Số file thực tế bị ảnh hưởng: [N file]

**🛑 SCOPE GATE:** Nếu phương án yêu cầu:
- Tạo Module mới hoàn toàn, HOẶC
- Sửa đổi cấu trúc Database lõi, HOẶC
- Chạm vào **nhiều hơn 3 files logic** (dựa trên kết quả grep thực tế)

→ BẮT BUỘC DỪNG và phản hồi:
*"Yêu cầu này vượt quá scope của quick-task. Hãy dùng skill `@stax-backend` hoặc `@stax-frontend` để đảm bảo an toàn kiến trúc."*

Nếu pass Scope Gate, hỏi: *"Phương án này OK chưa để tôi bắt đầu code?"*

---

### Bước 2: Coding & Anti-Creep (Thực thi & Chặn phình task)

Sau khi User đồng ý, viết code tuân thủ **5 Luật Thép STAX** (Mục 4).

**🛑 ANTI-SCOPE CREEP:** Nếu User bổ sung yêu cầu mới không có trong thỏa thuận ở Bước 1:
- TỪ CHỐI code phần mới
- Cảnh báo: *"Đây là yêu cầu mới ngoài scope đã thỏa thuận. Tôi sẽ hoàn thành task hiện tại trước, sau đó tạo task mới cho phần này."*
- Ghi nhận yêu cầu mới vào danh sách pending

---

### Bước 3: Exit Verification & Quick Logging

**[🛑 EXIT VERIFICATION — Bắt buộc trước khi báo "Xong"]**

Chạy và DÁN KẾT QUẢ THỰC TẾ vào chat:

```bash
# 1. Build check
npm run build
# → Paste output. Nếu có error → FIX trước.

# 2. No any check (chỉ trong file đã sửa)
grep -n ": any\|as any" [đường dẫn file đã sửa]
# → Phải trống. Nếu có → FIX trước.

# 3. Test liên quan
npm test -- --testPathPattern="[tên module]"
# → Paste output. Phải pass xanh.
```

Sau khi verification sạch, ghi log vào `docs/STAX/06_CHANGELOG.md` (tạo nếu chưa có), thêm lên ĐẦU file:

```markdown
### [YYYY-MM-DD] - {Tên Task Ngắn Gọn}
- **Module:** `tên-module`
- **Loại:** `Feature` | `Bugfix` | `Auditor-Fix`
- **Files đã sửa:** [danh sách]
- **Thay đổi:**
  - [mô tả thay đổi 1]
  - [mô tả thay đổi 2]
- **Exit Verification:** ✅ Build pass | ✅ No any | ✅ Tests pass
```

---

## 4. STAX Hard Constraints (5 Luật Thép Không Thể Vi Phạm)

Dù task nhỏ đến đâu, BẮT BUỘC tuân thủ:

1. **No Framework Leakage:** Cấm ném `BadRequestException`, `NotFoundException` ở tầng Domain/Application. Phải ném `EntityNotFoundException` hoặc `BusinessRuleValidationException` từ `core/shared`.

2. **Transaction Management:** Nếu ghi vào từ 2 bảng trở lên, bắt buộc bọc trong `this.txManager.runInTransaction(async (tx) => { ... })`.

3. **DTO Strictness:** Cấm trả về Entity thô hoặc Drizzle Record ra ngoài API. Phải đi qua Mapper hoặc Response DTO.

4. **No Magic Strings:** Trạng thái/phân loại phải dùng TypeScript Enum và pgEnum.

5. **Update Safety:** Khi thực hiện UPDATE, tuyệt đối không ghi đè `id`, `createdAt`, `organizationId`. BẮT BUỘC sử dụng `mapToUpdate()` trước khi đẩy vào Database.

---

## 5. Exit Criteria

```
[ ] Pre-Scope grep đã chạy và kết quả được paste
[ ] Scope Gate đã pass (≤3 files logic)
[ ] 5 Luật Thép không bị vi phạm
[ ] Exit Verification: Build pass, no any, tests pass — kết quả paste thực tế
[ ] CHANGELOG.md đã được cập nhật với entry đúng format
[ ] Pending requests (nếu có) đã được ghi nhận cho task tiếp theo
```
