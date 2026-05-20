# 📂 DANH MỤC NỐT NGUYÊN TỬ STAX (STAX ATOMIC KNOWLEDGE INDEX)

Chào mừng bạn đến với Layer 3 - Hệ thống **Nốt nguyên tử (Atomic Notes)** của dự án STAX. Các tài liệu ở đây được thiết kế siêu gọn nhẹ (dưới 50 dòng) và độc lập nhằm phục vụ việc tìm kiếm chính xác và tiết kiệm Token tối đa cho các AI Agents.

---

## 🏗️ 1. Nhóm Kiến trúc & Hạ tầng (Architecture & Infrastructure)

| Nốt Nguyên Tử | Tóm tắt (1 dòng) | Phụ thuộc | Tags |
| :--- | :--- | :--- | :--- |
| [[arch-modular-monolith-tiers]] | Phân loại module thành 3 Tiers tránh circular dependency. | *Không* | `#architecture` `#modular` |
| [[arch-clean-boundaries]] | Ranh giới độc lập của 4 lớp Clean Architecture. | [[arch-modular-monolith-tiers]] | `#clean-arch` `#layers` |
| [[arch-als-tenant-isolation]] | Tự động hóa cô lập tenant lọc CSDL thông qua ALS. | [[arch-clean-boundaries]] | `#multi-tenancy` `#als` |
| [[arch-als-transactions]] | Quản lý transactional boundary ngầm định qua ALS. | [[arch-als-tenant-isolation]] | `#transactions` `#als` |
| [[arch-exception-handling]] | Luật xử lý và ném exception an toàn trong Clean Arch. | [[arch-clean-boundaries]] | `#exceptions` `#error` |

---

## 🏰 2. Nhóm Tiêu chuẩn & Quy tắc (Standards & Governance)

| Nốt Nguyên Tử | Tóm tắt (1 dòng) | Phụ thuộc | Tags |
| :--- | :--- | :--- | :--- |
| [[std-naming-rules]] | Quy ước đặt tên tệp, thư mục, hàm, biến và CSDL. | *Không* | `#standards` `#naming` |
| [[std-import-boundaries]] | Luật import chéo cấm import sâu, xuất qua index.ts. | [[arch-modular-monolith-tiers]] | `#boundaries` `#modularity` |
| [[std-api-contracts]] | Thiết kế API hướng hợp đồng dùng chung qua Zod Schema. | *Không* | `#contracts` `#zod` |
| [[std-team-workflow]] | Quy trình 4 bước lưu vết từ BA đến code và đóng băng history. | *Không* | `#workflow` `#history` |

---

## 📚 3. Nhóm Sổ tay Thực thi (Technical Handbooks)

| Nốt Nguyên Tử | Tóm tắt (1 dòng) | Phụ thuộc | Tags |
| :--- | :--- | :--- | :--- |
| [[hb-drizzle-base-repo]] | Triển khai Repository Adapter kế thừa từ Base Repo. | [[arch-clean-boundaries]], [[arch-als-tenant-isolation]] | `#drizzle` `#orm` |
| [[hb-delta-logging]] | Ghi nhật ký thay đổi dữ liệu nghiệp vụ dạng Delta JSON. | *Không* | `#logging` `#delta-log` |
| [[hb-rbac-permissions]] | Phân quyền vai trò tĩnh định dạng domain:resource:action. | *Không* | `#rbac` `#permissions` |
| [[hb-http-request-flow]] | Sơ đồ luồng chạy tuần tự của một HTTP Request qua NestJS. | [[arch-als-tenant-isolation]], [[hb-rbac-permissions]] | `#request-flow` `#nestjs` |

---

## 📦 4. Nhóm Nghiệp vụ & Từ điển (Domain Knowledge)

| Nốt Nguyên Tử | Tóm tắt (1 dòng) | Phụ thuộc | Tags |
| :--- | :--- | :--- | :--- |
| [[dom-hrm-position-model]] | Triết lý quản lý nhân sự dựa trên Vị trí (Position-based). | *Không* | `#domain` `#hrm` `#position` |
| [[dom-accounting-finote]] | Luồng chứng từ phiếu thu/chi và đồng bộ số dư Sổ quỹ. | *Không* | `#domain` `#accounting` `#finote` |
| [[dom-crm-pipelines]] | Quản lý cơ hội qua Kanban và tự động chuyển đổi sang Org. | *Không* | `#domain` `#crm` `#leads` |

---
*Mạng lưới liên kết chéo chằng chịt giúp AI duyệt đồ thị tri thức cực kỳ linh hoạt.*
