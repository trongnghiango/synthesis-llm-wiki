# 🚨 STAX Docs Issues Report (Báo cáo vấn đề tài liệu)

Dưới đây là tổng hợp các vấn đề lớn nhất được phát hiện trong quá trình quét hệ thống tài liệu STAX.

---

## 1. Trùng lặp & Chồng chéo Nội dung (Duplicate / Overlap)

Nhiều tài liệu đang nói về cùng một chủ đề theo nhiều phiên bản hoặc đặt tên khác nhau:

| Chủ đề | Các file trùng lặp | Vấn đề | Đề xuất xử lý |
| :--- | :--- | :--- | :--- |
| **Clean Architecture** | `docs/handbooks/clean-architecture-handbook.md`<br>`docs/handbooks/clean-architecture-handbook-v1.md`<br>`docs/handbooks/clean-architecture-handbook-v2.md`<br>`docs/architecture/clean-architecture.md` | Có 4 file nói cùng nội dung, bản v2 là chuẩn nhất, các bản khác cũ hơn hoặc viết thô. | Giữ `clean-architecture-handbook-v2.md` làm Canonical Handbook, chuyển các file còn lại vào `_legacy/` hoặc xóa. |
| **Kiến trúc Cốt lõi** | `docs/STAX/architecture/01_STAX_CORE_ARCHITECTURE.md`<br>`docs/architecture/01_ARCHITECTURE.md` | Bản `01_ARCHITECTURE.md` ở ngoài mới hơn và tối ưu hơn. Bản trong `STAX/` là bản sơ khởi. | Merge phần chi tiết kỹ thuật từ bản STAX vào bản chính ngoài và archive bản cũ. |
| **Drizzle ORM & ORM** | `docs/handbooks/orm.md`<br>`docs/handbooks/orm-mapping.md` | `orm.md` dài dòng, `orm-mapping.md` tập trung vào kỹ thuật map Flat↔Nested. | Gộp orm.md vào orm-mapping.md để thành 1 file ORM Handbook hoàn chỉnh. |
| **Chiến lược Dữ liệu** | `docs/architecture/data-strategy.md`<br>`docs/architecture/03_DATA_STRATEGY.md` | `03_DATA_STRATEGY.md` là bản cập nhật chuẩn nhất. | Thay thế `data-strategy.md` bằng `03_DATA_STRATEGY.md`. |
| **Nghiệp vụ Kế toán Thuế** | `docs/Quy trình...docx.md`<br>`docs/STAX/business/Quy trình...docx.md` | Bản sao chép trùng lặp y hệt. | Chỉ giữ lại 1 file duy nhất trong thư mục nghiệp vụ (`docs/domain/`). |

---

## 2. Trùng lặp tên do viết hoa/thường (Capitalization Clash)

Đây là vấn đề nghiêm trọng khi chạy trên các hệ điều hành phân biệt chữ hoa/thường (Linux) so với không phân biệt (macOS/Windows), dẫn đến xung đột Git:

- **`docs/handbooks/INDEX.md`** vs **`docs/handbooks/index.md`**
- **`docs/handbooks/LOGGING.md`** vs **`docs/handbooks/logging.md`**
- **`docs/architecture/INDEX.md`** vs **`docs/architecture/index.md`**

**Đề xuất:** Chuẩn hóa toàn bộ thành viết hoa `INDEX.md` và viết thường `logging.md` để đồng nhất, xóa các file trùng lặp.

---

## 3. Liên kết hỏng & Đường dẫn Tuyệt đối (Broken & Absolute Links)

- **Đường dẫn tuyệt đối hệ máy khác:** Trong file `docs/architecture/README.md`, các link đến tài liệu V2 đều đang trỏ đến đường dẫn tuyệt đối của máy dev cũ:
  `file:///home/ka/Repos/github.com/trongnghiango/rbac-nest-project/docs/STAX_V2/...`
  Các link này hoàn toàn bị hỏng trên máy khác.
- **Link trỏ vào thư mục ảo:** `docs/INDEX.md` và `docs/README.md` trỏ đến `./vision/index.md`, `./governance/index.md`, `./domain/index.md`, `./history/INDEX.md` nhưng các thư mục này thực tế không hề tồn tại ở root của `docs/`!

---

## 4. Tài liệu Mồ côi (Orphan Files)

Các tài liệu sau đây nằm rải rác trong thư mục `handbooks/` nhưng không được liên kết hay nhắc đến trong bất kỳ file `INDEX.md` hay `README.md` nào:
- `docs/handbooks/fix_logic_mapping.md`
- `docs/handbooks/nang-cap-mo-hinh-ung-dung-theo-nhieu-level.md`
- `docs/handbooks/nhan-xet-va-cai-thien-du-an.md`
- `docs/handbooks/quy-tac-dat-ten-interface.md`
- `docs/handbooks/smell.md`
- `docs/handbooks/policy-engine-abac.md`

Các tài liệu này đa phần là ghi chú nháp cũ từ thời điểm kiểm toán ban đầu.

---

## 5. Thư mục Trùng lặp (Folder Redundancy)

Chúng ta có hai thư mục chứa tài liệu kiến trúc chính:
- `docs/STAX/architecture/`
- `docs/architecture/`

Và tài liệu ADR đang phân mảnh:
- `docs/STAX/adr/`
- `docs/architecture/adr/`

**Đề xuất:** Gom toàn bộ tài liệu kiến trúc, ADR hoạt động vào một thư mục gốc thống nhất là `docs/architecture/` và `docs/architecture/adr/`.
