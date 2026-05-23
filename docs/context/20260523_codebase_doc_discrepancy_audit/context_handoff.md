# Handoff Summary — Soi Code & Đối chiếu Tài liệu Kiến trúc STAX

**Skill vừa hoàn thành:** `@stax-think` (Tư duy Kiến trúc - Phân tích Khủng hoảng Bất đồng bộ giữa Tài liệu & Mã nguồn Thực tế)  
**Skill tiếp theo:** `@stax-naming-auditor` & `@stax-think` (Phiên làm việc tiếp theo: Rà soát từng Module nhỏ để bắt lỗi bất nhất)

## 📋 Context (Ngữ cảnh Hiện tại)
- Chúng ta vừa phát hiện một lỗ hổng nghiêm trọng về mặt tri thức: **Tài liệu tham chiếu kiến trúc mẫu (`stax_backend_architecture.md`) có các chi tiết bị lệch pha hoàn toàn với codebase thực tế của `STAX_ASP`** (Ví dụ cụ thể: code mẫu chứa thuộc tính `organizationId` tĩnh trong thực thể `Session`, trong khi codebase thực tế lại sử dụng cơ chế bảo mật động tinh tế qua `VisibilityContext` nhúng trong JWT & AsyncLocalStorage).
- Điều này cực kỳ nguy hiểm vì các AI Agents tương lai sẽ đọc tài liệu mẫu và cố tình đề xuất thay đổi phá vỡ kiến trúc thực tế của dự án.
- **Nhiệm vụ:** Chia nhỏ hệ thống thành từng phân khu/module nhỏ để rà soát sâu, soi mã nguồn thực tế và đối chiếu trực tiếp với tài liệu để vá lỗi kịp thời.

---

## 🛠️ Chia nhỏ Chiến trường (Decomposition Roadmap)

Hệ thống `STAX_ASP` sẽ được chia thành 4 Phân khu chính để rà soát cuốn chiếu trong các session sau:

### Phân khu 1: Core Tiers & Context Gateways (Cực kỳ quan trọng)
- **Tập trung vào:** `core/shared/infrastructure/context/` (`RequestContext`, `TransactionContext`) và `persistence/drizzle-base.repository.ts`.
- **Mục tiêu:** Đối chiếu cách nạp và giải phóng ALS có rò rỉ bộ nhớ hoặc thiếu Tenant Isolation không.

### Phân khu 2: Module Auth & User (Identity vs Tenant Dynamic)
- **Tập trung vào:** `src/modules/auth/` và `src/modules/user/`.
- **Mục tiêu:** Kiểm tra cấu trúc JWT Payload, thực thể `User`, `Session`, `VisibilityResolverService`. Đảm bảo code mẫu hoàn toàn loại bỏ `organizationId` tĩnh khỏi session DB.

### Phân khu 3: Module CRM (Leads, Contact, Org, Service Catalog)
- **Tập trung vào:** `src/modules/crm/` và `shared/contracts/crm`.
- **Mục tiêu:** Đối chiếu các thực thể `Lead`, `Organization`, `Contact` xem các trường ID Suffixes có tuân thủ Hiến pháp STAX không.

### Phân khu 4: Phân hệ Kế toán & HRM (Process Flow T3)
- **Tập trung vào:** `src/modules/accounting/` và `src/modules/hrm/`.
- **Mục tiêu:** Kiểm tra luồng `Finote` chống âm quỹ, event-driven auditing, và tree-path đệ quy của sơ đồ phòng ban.

---

## 📝 Quyết định đã khóa (Decisions Locked)
1. **[D1] Không thay đổi Database Schema & Entity Session:** Bảo toàn nguyên vẹn cơ chế dynamic isolation cực kỳ tinh tế của `STAX_ASP` (JWT Payload + ALS + `VisibilityContext`).
2. **[D2] Chuẩn hóa Tài liệu Kiến trúc thay vì sửa Code:** Đã sửa trực tiếp [stax_backend_architecture.md](../../../memory/stax_backend_architecture.md) để phản ánh đúng thực tế, biến nó thành nguồn tri thức duy nhất đáng tin cậy.
3. **[D3] Áp dụng quy trình Cổng Xác thực Tương tác (Siphon Gate):** Bắt buộc hỏi ý kiến người dùng trước khi AI tự ý nạp tri thức ngoài hoặc đề xuất refactor hệ thống.

## 📌 Assumptions (Giả định cốt lõi)
- [ASSUMPTION 1]: Tài liệu `stax_backend_architecture.md` hiện tại sau khi chỉnh sửa đã chuẩn khớp 100% với module Auth thực tế của `STAX_ASP`.
- [ASSUMPTION 2]: Hệ thống có khả năng xuất hiện các bất đồng bộ tương tự ở các module khác như CRM (tên biến, Zod schema chéo) và Kế toán (cơ chế party/finote).

---

## 🚀 Kế hoạch Hành động cho Session Tiếp theo
1. Khởi động với **Phân khu 1 & 2** (Core Tiers + Auth/User).
2. Dùng `@stax-naming-auditor` để quét cấu trúc thư mục, biến và schema Drizzle để đối chiếu với tài liệu `std-naming-rules.md`.
3. Báo cáo bất kỳ sự sai lệch nào lên User và đề xuất chỉnh sửa tài liệu mẫu hoặc mã nguồn (nếu thực sự là bug).
