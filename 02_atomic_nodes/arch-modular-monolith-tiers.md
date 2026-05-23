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

## 3. Quản lý Sub-module & Tách biệt để Tránh Vi phạm Ranh giới (Sub-module Optimization)
Một lưu ý tối quan trọng khi quản lý hệ thống phân tầng:
* **Tác hại của Sub-module lồng ghép:** Một module lớn (như `HRM`) có thể chứa nhiều sub-module con bên trong (như `Employee`). Nếu để nguyên cấu trúc lồng ghép này, các module cấp ngang hàng với `HRM` (như `CRM`) khi cần gọi đến `Employee` sẽ vô tình tạo liên kết phụ thuộc trực tiếp vào module cha `HRM`, vi phạm nghiêm trọng nguyên tắc độc lập của ranh giới (Domain Boundary).
* **Giải pháp Tách biệt Độc lập (Tối ưu nhất):** Bắt buộc tách sub-module cốt lõi có tần suất tái sử dụng cao (`Employee`) ra khỏi module cha (`HRM`) thành một module độc lập ở **Tier 2 (Domain Core)**. Nhờ đó, cả `HRM` và `CRM` đều có thể gọi trực tiếp và an toàn đến `Employee` mà không phụ thuộc chéo vào nhau.
* **Cơ chế Đăng ký Động (Dynamic Registration - Trường hợp đặc biệt):** Đối với các trường hợp đặc biệt không thể tách rời do đặc thù hạ tầng (ví dụ: các providers của `SystemModule` cần đăng ký Lookup động), ta áp dụng phương pháp **Register Pattern** để đăng ký động các providers/handlers tại thời điểm khởi tạo module (`onModuleInit` / `LookupRegistry`), đảm bảo module gốc vẫn giữ nguyên tính độc lập hoàn toàn mà không bị coupling cứng.
