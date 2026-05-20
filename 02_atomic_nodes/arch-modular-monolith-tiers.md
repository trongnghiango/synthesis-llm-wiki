---
id: arch-modular-monolith-tiers
title: Phân tầng Module (Modular Monolith Tiers)
layer: 3-atomic
parent: "[[01_core_architecture]]"
depends_on: []
summary: "Phân loại các module nghiệp vụ thành 3 tầng (Tiers) có mức độ độc lập giảm dần nhằm ngăn ngừa Circular Dependency."
tags: [architecture, module, modular-monolith, dependencies]
---

# Phân tầng Module (Modular Monolith Tiers)

Để quản lý độ phức tạp hệ thống, STAX tổ chức các module nghiệp vụ (Bounded Contexts) theo cấu trúc phân tầng nghiêm ngặt:

## 1. Ba Tầng Module (The 3-Tier System)
*   **Tier 1 - Foundation (Hạ tầng):** Các module kỹ thuật dùng chung, không chứa business logic doanh nghiệp.
    *   *Ví dụ:* `Rbac` (Phân quyền), `Notification` (Thông báo), `AuditLog` (Lưu vết), `Storage` (Lưu trữ file).
*   **Tier 2 - Domain Core (Xương sống):** Các module chứa thực thể và nghiệp vụ cốt lõi, định hình ADN hệ thống.
    *   *Ví dụ:* `User` (Tài khoản), `OrgStructure` (Cấu trúc tổ chức), `Employee` (Nhân sự).
*   **Tier 3 - Process Flow (Quy trình nghiệp vụ):** Các dòng chảy nghiệp vụ động và tiền tệ, phụ thuộc sâu vào Tier 2.
    *   *Ví dụ:* `CRM` (Khách hàng), `Accounting` (Kế toán), `Contracts` (Hợp đồng).

## 2. Luật Cô lập Tầng (Tier Isolation Rule)
1. **Hướng phụ thuộc:** Tầng dưới tuyệt đối không được biết hoặc import bất kỳ file nào từ tầng trên.
    *   *Đúng:* Tier 3 import từ Tier 2. Tier 2 import từ Tier 1.
    *   *Sai:* Tier 2 import bất kỳ thứ gì từ Tier 3 (`User` import `CRM`).
2. **Giao tiếp ngang hàng / vượt tầng:** Phải được thực hiện gián tiếp thông qua **Ports (Interfaces)** hoặc bắn **Domain Events** qua EventBus để đảm bảo khớp nối lỏng (Loose Coupling).
