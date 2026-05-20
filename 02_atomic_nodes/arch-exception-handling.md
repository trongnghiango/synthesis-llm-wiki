---
id: arch-exception-handling
title: Quản trị Lỗi & Exception Safety
layer: 3-atomic
parent: "[[01_core_architecture]]"
depends_on:
  - "[[arch-clean-boundaries]]"
summary: "Quy tắc quản trị và xử lý exception an toàn trong Clean Architecture, cấm rò rỉ lỗi framework ở tầng nghiệp vụ."
tags: [architecture, exceptions, error-handling, clean-architecture]
---

# Quản trị Lỗi & Exception Safety

Để đảm bảo tính nhất quán của hệ thống và tránh rò rỉ thông tin lỗi hạ tầng kỹ thuật ra client, STAX áp dụng quy chuẩn xử lý exception nghiêm ngặt:

## 1. Phân chia ranh giới Exception
*   **Domain & Application Layers:** Tuyệt đối **cấm** sử dụng hoặc ném các NestJS HTTP exceptions (`BadRequestException`, `NotFoundException`, `ForbiddenException`).
    *   *Tại sao:* Để giữ lớp nghiệp vụ độc lập hoàn toàn khỏi Web Framework. Nếu đổi NestJS sang Express hoặc CLI, code nghiệp vụ sẽ bị lỗi biên dịch.
    *   *Thay thế:* Bắt buộc ném các exception nghiệp vụ thuần khiết từ core như: `BusinessRuleValidationException` hoặc `EntityNotFoundException`.

*   **Presentation Layer (NestJS Controllers):**
    *   Thực hiện việc đón nhận (catch) các Exception nghiệp vụ thuần khiết.
    *   Ánh xạ (Map) chúng sang mã lỗi HTTP tương ứng (e.g., `EntityNotFoundException` ──► `NotFoundException` (404)).

## 2. Exception Filter trung tâm
*   Một Exception Filter toàn cục (`GlobalExceptionFilter`) được cấu hình tại NestJS.
*   Nhiệm vụ: Bắt toàn bộ các exception chưa được xử lý, log chi tiết lỗi kèm trace-id lên hệ thống Winston Logger, và đóng gói response trả về định dạng chuẩn cho client, che giấu các thông tin lỗi thô của CSDL (SQL errors).
