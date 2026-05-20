---
id: hb-http-request-flow
title: Luồng xử lý yêu cầu HTTP (HTTP Request Flow)
layer: 3-atomic
parent: "[[03_technical_handbooks]]"
depends_on:
  - "[[arch-als-tenant-isolation]]"
  - "[[hb-rbac-permissions]]"
summary: "Sơ đồ và phân tích luồng chạy tuần tự của một HTTP Request đi qua các thành phần chặn lọc của NestJS."
tags: [handbooks, request-flow, guards, interceptors, pipes, nestjs]
---

# Luồng xử lý yêu cầu HTTP (HTTP Request Flow)

Việc nắm vững vòng đời của một yêu cầu HTTP (HTTP Request Life Cycle) giúp nhà phát triển can thiệp đúng lúc, đúng lớp kỹ thuật.

## 1. Sơ đồ luồng chạy tuần tự
Một request từ Client đi qua các chốt chặn NestJS theo thứ tự nghiêm ngặt sau:

```
[Request]
   │
   ▼
1. Middleware (Thiết lập ALS organizationId, Giải mã JWT token)
   │
   ▼
2. Guards (RBAC permissions check - Chặn thô)
   │
   ▼
3. Interceptors (Bắt đầu đo lường hiệu năng, đính trace-id)
   │
   ▼
4. Pipes (DTO validation & convert kiểu dữ liệu)
   │
   ▼
5. Controller (Định tuyến, gọi Use Case)
   │
   ▼
6. Use Case / Application Layer (Transaction Boundary)
   │
   ▼
[Response]
```

## 2. Các điểm can thiệp cốt lõi
*   **Middleware:** Chỗ duy nhất được phép khởi tạo Async Local Storage (ALS) vì nó chạy đầu tiên trước khi đi vào bộ định tuyến NestJS.
*   **Guards:** Chạy trước Interceptors và Pipes. Chỉ dùng để xác thực tĩnh quyền truy cập.
*   **Pipes:** Chạy ngay trước Controller. Dùng để ném các lỗi xác thực DTO thô (ví dụ: thiếu email, sai định dạng điện thoại) bằng `class-validator`.
