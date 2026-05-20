---
id: arch-clean-boundaries
title: Ranh giới các lớp Clean Architecture
layer: 3-atomic
parent: "[[01_core_architecture]]"
depends_on:
  - "[[arch-modular-monolith-tiers]]"
summary: "Phân chia module nghiệp vụ thành 4 lớp bảo vệ nghiêm ngặt: Domain, Application, Infrastructure và Presentation."
tags: [architecture, clean-architecture, boundaries, layers]
---

# Ranh giới các lớp Clean Architecture

Mỗi module nghiệp vụ (Bounded Context) trong STAX bắt buộc phải phân rã thành 4 lớp độc lập:

## 1. Domain Layer (`domain/`) - *Trọng tâm*
*   **Chứa:** Rich Domain Entities, Value Objects, Domain Events, Repository Interfaces (Ports).
*   **Độ thuần khiết (Domain Purity):** Tuyệt đối cấm import NestJS, Drizzle-ORM, hay các thư viện hạ tầng. Chỉ viết bằng TypeScript thuần.
*   **Rich Entity:** Thực thể phải tự bảo vệ các bất biến nghiệp vụ (Business Invariants) của chính nó thông qua các hàm nghiệp vụ, không dùng Anemic Model.

## 2. Application Layer (`application/`) - *Điều phối*
*   **Chứa:** Use Cases, Services, Application exceptions.
*   **Nhiệm vụ:** Nhận DTO từ Presentation, điều phối Domain Entities xử lý nghiệp vụ, kiểm soát giao dịch qua Transaction Manager.
*   **Ràng buộc:** Cấm ném lỗi HTTP (e.g. `BadRequestException` của NestJS). Bắt buộc ném `BusinessRuleValidationException` từ core.

## 3. Infrastructure Layer (`infrastructure/`) - *Hạ tầng*
*   **Chứa:** Drizzle DB schemas (`pgTable`), Repository Adapters triển khai từ Domain Ports, Mappers (`toDomain` / `toPersistence`), API integrations bên ngoài.
*   **Nhiệm vụ:** Thực thi lưu trữ cơ sở dữ liệu vật lý và giao tiếp phần cứng/mạng.

## 4. Presentation Layer (`presentation/` hoặc `controllers/`) - *Ngoại vi*
*   **Chứa:** NestJS Controllers, Request/Response DTOs, Swagger, Guards, Decorators.
*   **Nhiệm vụ:** Đón nhận request, validate DTO thô, kiểm tra sơ bộ vai trò, chuyển luồng vào Use Cases.
