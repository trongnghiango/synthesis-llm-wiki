# 🤖 STAX Agentic AI Engine — Cẩm nang Vận hành Kỹ năng

Thư mục `.agent/` chứa toàn bộ các **Skill cấu hình kỹ năng hành vi** chuyên biệt được tối ưu hóa cho vị trí **Senior System Design, Business Analyst (BA), và NestJS Backend DDD/Clean Architecture Architect**.

Tài liệu này là hướng dẫn chuẩn mực giúp bạn và AI phối hợp nhịp nhàng các Agent để xử lý mọi yêu cầu trong dự án theo các quy trình chuyên nghiệp, có chốt chặn kỹ luật chặt chẽ.

---

## 🗺️ Sơ đồ Luồng Phối hợp Tổng thể (Workflow Architecture)

Dưới đây là sơ đồ hóa cách các Skill tự động phân loại, phối hợp và chuyển giao công việc (Handoff) tùy theo loại yêu cầu của bạn:

```mermaid
flowchart TD
    User([Yêu cầu từ Bạn]) --> Category{Phân loại Yêu cầu}

    %% Nhánh 1: Tư duy & Thiết kế
    Category -->|Hỏi đáp / Thiết kế / Kiến trúc| Think["🧠 `@stax-think`"]
    Think --> D1[Bước D1: Khảo sát & Đặt câu hỏi Socratic]
    D1 -->|Phản hồi của bạn| D2[Bước D2: Chốt thông tin Understanding Lock]
    D2 -->|Duyệt OK| D3[Bước D3: So sánh 2-3 Approaches]
    D3 -->|Chọn Approach| D4[Bước D4: Thiết kế chi tiết Schema / API]
    D4 -->|Duyệt từng phần| D5[Bước D5: Khóa thiết kế & Ghi Decision Log]
    
    %% Chuyển giao từ Thiết kế sang Thực thi
    D5 -->|Handoff| BE["⚙️ `@stax-backend`"]

    %% Nhánh 2: Tính năng lớn Backend
    Category -->|Thực thi module / Tính năng lớn| BE
    BE --> BE1["1️⃣ Phân tích Nghiệp vụ
    (00_be_analysis.md)"]
    BE1 -->|Gate 1: Duyệt OK| BE2["2️⃣ Kế hoạch Kiến trúc
    (01_be_implementation_plan.md)"]
    BE2 -->|Gate 2: Duyệt OK| BE3["3️⃣ Checklist Thực thi
    (02_be_tasks.md)"]
    BE3 -->|Gate 3: Viết Code| BE_Code[Thực thi viết mã nguồn NestJS + DDD]
    BE_Code --> BE4["4️⃣ Báo cáo & Bàn giao
    (03_be_walkthrough.md)"]
    BE4 --> Docs["📚 `@stax-docs-architect`"]
    
    %% Nhánh 3: Tái cấu trúc Tài liệu
    Category -->|Sắp xếp, dọn dẹp tài liệu| Docs
    Docs --> Docs1[Phase 1: Quét kiểm kê & phát hiện Smell tài liệu]
    Docs1 -->|Duyệt OK| Docs2[Phase 2: Viết INDEX.md, cấu trúc cây tài liệu và README]

    %% Nhánh 4: Sửa đổi nhỏ & Vá lỗi
    Category -->|Sửa lỗi / Viết task nhỏ| QT["⚡ `@stax-quick-task`"]
    QT --> Q_Gate{Scope Gate:
    Ảnh hưởng ≤ 3 files &
    Không sửa DB schema?}
    Q_Gate -->|Yes| QT_Code[Sửa code nhanh + Ghi log CHANGELOG.md]
    Q_Gate -->|No| BE

    %% Nhánh 5: Kiểm toán chất lượng
    Category -->|Quét kiểm toán chất lượng code| Auditor["🕵️ `@stax-naming-auditor`"]
    Auditor -->|Chỉ đọc Read-only| Audit_Rep["Báo cáo 01_naming_audit_report.md"]
    Audit_Rep --> Manifest["Fix Manifest 02_fix_manifest.md"]
    Manifest -->|Chuyển giao sửa tự động| QT
```

---

## 🚀 Chi tiết 3 Quy trình Vận hành Chuẩn (Standard Workflows)

### 1. Quy trình Phát triển Tính năng Lớn (Feature Development Workflow)
Áp dụng khi bạn muốn xây dựng một module mới từ đầu (Ví dụ: "Thiết kế và triển khai module Tính lương").

1.  **Bước 1 - Lên ý tưởng & Chốt kiến trúc:**
    *   Gọi **`@stax-think`** để AI brainstorm giải pháp.
    *   AI sẽ đặt các câu hỏi Socratic để hiểu rõ **Mục đích, Context, Constraints, và Non-goals**.
    *   Sau khi thống nhất, AI khóa thiết kế bằng **Decision Log** và sẵn sàng bàn giao.
2.  **Bước 2 - Lập kế hoạch & Triển khai Backend:**
    *   Gọi **`@stax-backend`** để bắt đầu viết code NestJS + Drizzle + DDD.
    *   AI bắt buộc phải đi qua 3 cổng chặn nghiêm ngặt (Phân tích $\to$ Kế hoạch $\to$ Checklist) trước khi viết dòng code đầu tiên. Bạn gõ `OK` để duyệt qua từng bước.
    *   Sau khi code xong và chạy tests thành công, AI xuất file Bàn giao `03_be_walkthrough.md`.
3.  **Bước 3 - Cập nhật cây tài liệu:**
    *   Gọi **`@stax-docs-architect`** để cập nhật tài liệu thiết kế mới vào `docs/README.md` và `docs/history/INDEX.md` để các AI khác trong tương lai kế thừa.

---

### 2. Quy trình Sửa lỗi & Vá nhanh (Quick Patch Workflow)
Áp dụng khi bạn muốn sửa một bug nhỏ hoặc thêm một trường thông tin đơn giản.

1.  **Bước 1 - Gọi nhanh:**
    *   Gọi **`@stax-quick-task`** và cung cấp yêu cầu.
2.  **Bước 2 - Kiểm tra Cổng Scope Gate:**
    *   AI rà soát mã nguồn. Nếu phát hiện thay đổi chạm vào **nhiều hơn 3 files** hoặc phải **thay đổi cấu trúc Database schema**, AI sẽ tự động từ chối và yêu cầu bạn chuyển sang gọi `@stax-backend` để đảm bảo an toàn kiến trúc.
3.  **Bước 3 - Thực thi & Ghi Log:**
    *   AI tiến hành viết code nhanh, đảm bảo 0 lỗi TypeScript `any` và không vi phạm "Domain Purity".
    *   Sau khi hoàn tất, AI ghi nhận thay đổi trực tiếp lên đầu tệp `docs/STAX/06_CHANGELOG.md`.

---

### 3. Quy trình Kiểm soát Chất lượng Code (Quality Assurance Workflow)
Áp dụng khi bạn muốn quét toàn bộ codebase để tìm "nợ kỹ thuật" (Technical Debt) hoặc vi phạm quy tắc đặt tên.

1.  **Bước 1 - Quét kiểm toán:**
    *   Gọi **`@stax-naming-auditor`**.
    *   AI hoạt động ở chế độ **Chỉ Đọc (Read-only)**, tuyệt đối không chỉnh sửa mã nguồn của bạn. Nó quét các files theo từ điển Ubiquitous Language và phát hiện các rò rỉ dữ liệu (như lộ mật khẩu trong DTO).
2.  **Bước 2 - Xuất báo cáo kiểm toán:**
    *   AI tạo thư mục `docs/audits/YYYYMMDD_{module_name}/` chứa báo cáo lỗi chi tiết (`01_...`) và danh sách hành động sửa lỗi (`02_fix_manifest.md`).
3.  **Bước 3 - Tự động sửa chữa:**
    *   Bạn gọi **`@stax-quick-task`** và yêu cầu: *"Thực thi sửa lỗi tự động dựa trên file 02_fix_manifest.md"*.
    *   AI sẽ đọc manifest và tự động thực thi sửa lỗi nhanh chóng, chính xác.

---

## ⌨️ Cú pháp lệnh gọi nhanh (Shortcuts & Commands)

Bạn chỉ cần gõ các câu lệnh sau trong chat, AI sẽ ngay lập tức kích hoạt đúng Persona và Skill tương ứng:

*   **Để thiết kế / brainstorm:**
    > *"Hãy dùng @stax-think để thiết kế giải pháp cho [yêu cầu] của tôi."*
*   **Để code module mới:**
    > *"Hãy dùng @stax-backend để bắt đầu lập kế hoạch triển khai [yêu cầu]."*
*   **Để sửa nhanh / vá lỗi:**
    > *"Hãy dùng @stax-quick-task để sửa lỗi [yêu cầu]."*
*   **Để quét kiểm toán chất lượng code:**
    > *"Hãy dùng @stax-naming-auditor để quét toàn bộ module [tên-module]."*
*   **Để cấu trúc lại tài liệu:**
    > *"Hãy dùng @stax-docs-architect để dọn dẹp thư mục docs."*
