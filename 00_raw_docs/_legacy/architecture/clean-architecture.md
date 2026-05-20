---
title: "Sổ tay Clean Architecture (v2)"
status: "actual"
level: "architecture"
tags: ["clean-architecture", "patterns", "nestjs"]
last_updated: "2026-05-11"
---

# 📘 CLEAN ARCHITECTURE HANDBOOK (Phiên bản V2)

```
booking-system/
├── src/
│   ├── modules/
│   │   ├── ticket/          # Quản lý vé
│   │   ├── booking/         # Đặt vé
│   │   ├── payment/         # Thanh toán
│   │   └── notification/    # Thông báo
│   ├── shared/
│   │   ├── common/          # Shared code
│   │   ├── config/          # Configuration
│   │   └── utils/           # Utilities
│   └── main.ts              # Entry point
├── infra/
│   ├── docker-compose.yml   # Local dev
│   ├── Dockerfile           # Production
│   └── nginx/               # Load balancer config
├── scripts/
│   ├── deploy.sh            # Deployment
│   └── db-migrations/       # DB migrations
└── README.md
```

Cấu trúc thư mục trên đưa ra là mô hình **Modular Monolith** (Monolith chia theo module). Đây là cấu trúc rất tốt, cân bằng giữa sự đơn giản của Monolith và tính tổ chức của Microservices.

Tuy nhiên, **nội dung bên trong mỗi folder module** (`ticket`, `booking`, `payment`) sẽ biến đổi hoàn toàn khác nhau tùy theo "Stage" tư duy mà bạn áp dụng.

Dưới đây là sự so sánh chi tiết sự biến đổi của folder `src/modules/booking/` qua từng giai đoạn:

---

### 1. Stage 0 — "Service vạn năng" (Spaghetti Code)

Ở giai đoạn này, cấu trúc bên trong module rất phẳng và đơn giản. Mọi thứ trộn lẫn vào nhau.

**Cấu trúc thư mục `src/modules/booking/`:**
```
booking/
├── booking.controller.ts  # Nhận request
├── booking.service.ts     # Chứa TẤT CẢ logic (validate, db, email)
├── booking.entity.ts      # DB Schema (TypeORM entity)
└── booking.module.ts      # Khai báo dependency
```

*   **Tác động đến `shared/`:** Chỉ chứa các hàm tiện ích vô thưởng vô phạt (ví dụ: `formatDate`, `logger`).
*   **Đánh giá:**
    *   **Nhìn:** Rất gọn, dễ hiểu cho người mới.
    *   **Thực tế:** File `booking.service.ts` sẽ dài hàng nghìn dòng. Code trong này import trực tiếp `PaymentService` và `NotificationService` từ module khác -> **Coupling cực cao**.
    *   **Hậu quả:** Sửa module `payment` có thể làm chết module `booking`.

---

### 2. Stage 1 — Layered Architecture (Service + Repository)

Bạn bắt đầu tách lớp truy cập dữ liệu và lớp vận chuyển dữ liệu (DTO).

**Cấu trúc thư mục `src/modules/booking/`:**
```
booking/
├── dto/
│   ├── create-booking.dto.ts
│   └── update-booking.dto.ts
├── entities/
│   └── booking.entity.ts
├── repositories/             # NEW: Tách câu query DB ra đây
│   └── booking.repository.ts
├── booking.controller.ts
├── booking.service.ts        # Vẫn chứa logic business + logic flow
└── booking.module.ts
```

*   **Tác động đến `shared/`:** Bắt đầu xuất hiện các `BaseRepository` hoặc `BaseEntity`.
*   **Đánh giá:**
    *   **Nhìn:** Ngăn nắp hơn.
    *   **Thực tế:** `booking.service.ts` vẫn phụ thuộc trực tiếp vào `PaymentService`. Logic nghiệp vụ vẫn dính chặt vào Framework.

---

### 3. Stage 3 & 4 — Clean Architecture (Hexagonal)

Đây là lúc cấu trúc thư mục thay đổi **chất lượng**. Module `booking` được chia thành các vòng tròn đồng tâm (Domain, App, Infra).

**Cấu trúc thư mục `src/modules/booking/`:**
```
booking/
├── domain/                   # INNER CIRCLE (Không phụ thuộc bên ngoài)
│   ├── booking.entity.ts     # Pure Class, logic nghiệp vụ
│   ├── booking-status.vo.ts  # Value Object
│   └── booking.repository.interface.ts # Port (Interface)
├── application/              # USE CASES
│   ├── use-cases/
│   │   └── create-booking.usecase.ts
│   └── dtos/
├── infra/                    # OUTER CIRCLE (Phụ thuộc Framework)
│   ├── database/
│   │   ├── typeorm-booking.repository.ts # Adapter
│   │   └── booking.schema.ts             # DB Schema
│   └── http/
│       └── booking.controller.ts
└── booking.module.ts
```

*   **Tác động đến `shared/`:** Chứa các Interface dùng chung (ví dụ `IUseCase`, `AppError`).
*   **Điểm mấu chốt:** Folder `domain` hoàn toàn không có file nào import từ `nestjs` hay `typeorm`.

---

### 4. Stage 5 & Final — DDD + CQRS + Event Driven

Cấu trúc bùng nổ để phục vụ Enterprise. Tách biệt luồng Đọc/Ghi và giao tiếp qua Event.

**Cấu trúc thư mục `src/modules/booking/`:**
```
booking/
├── domain/
│   ├── aggregates/           # Booking Aggregate
│   ├── events/               # BookingCreatedEvent
│   └── services/             # Domain Services
├── application/
│   ├── commands/             # Write Side (CQRS)
│   │   ├── handlers/
│   │   └── impl/
│   ├── queries/              # Read Side (CQRS)
│   │   ├── handlers/
│   │   └── impl/
│   └── sagas/                # Xử lý transaction phân tán
├── infra/
│   ├── adapters/             # PaymentAdapter, NotificationAdapter
│   ├── persistence/          # Database implementation
│   └── api/                  # Controllers / GraphQL Resolvers
└── booking.module.ts
```

*   **Tác động đến `shared/`:** Trở thành **Shared Kernel**. Chứa `EventBus`, `CommandBus`, `AggregateRoot` base class.
*   **Đánh giá:**
    *   **Nhìn:** Rất phức tạp, nhiều file.
    *   **Thực tế:** Module `booking` **không hề biết** `payment` hay `notification` tồn tại. Nó chỉ bắn ra 1 cái Event. Module khác nghe Event và tự xử lý. Sự phụ thuộc giữa các module = 0.

---

### Bảng so sánh tác động lên dự án Monolith

| Yếu tố | Stage 0 (Spaghetti) | Stage 1 (Layered) | Stage 3 (Clean) | Stage Final (DDD/CQRS) |
| :--- | :--- | :--- | :--- | :--- |
| **Độ sâu thư mục** | 1 cấp (Phẳng) | 2 cấp (Phân loại file) | 3-4 cấp (Phân loại Layer) | 4-5 cấp (Phân loại Intent) |
| **Quan hệ Module** | Import trực tiếp (`PaymentService`) | Import trực tiếp | Qua Interface/Port | Qua EventBus/MessageQueue |
| **Logic Business** | Nằm trong Service | Nằm trong Service | Nằm trong Domain Entity | Nằm trong Domain Aggregate |
| **Testability** | Rất khó | Test được logic đơn lẻ | Unit test dễ dàng 100% | Test độc lập từng luồng |
| **Scalability** | Khó tách service | Khó tách | Dễ tách logic, khó tách DB | Cực dễ tách Microservice |
| **Chi phí Dev** | Thấp (code nhanh) | Trung bình | Cao (nhiều boilerplate) | Rất cao (cần trình độ cao) |

### Kết luận: Nên chọn Stage nào cho cấu trúc dự án này?

Với cấu trúc thư mục bạn đưa ra (`src/modules/...`), tôi khuyến nghị:

1.  **Giai đoạn đầu (MVP/Startup):** Dùng **Stage 1 (Service + Repo)** nhưng tuân thủ quy tắc: *Controller chỉ gọi Service, Service gọi Repo*. Đừng phức tạp hóa.
2.  **Giai đoạn mở rộng (Scale User):** Nâng cấp lên **Stage 3 (Clean Arch)**. Bắt đầu tách folder `domain` ra trong từng module.
3.  **Chỉ lên Stage 5 khi:** Logic quá phức tạp (ví dụ Booking có flow: giữ vé -> thanh toán -> hoàn tiền -> đổi vé -> tích điểm). Nếu chỉ CRUD đơn giản thì Stage 5 là "giết gà dùng dao mổ trâu".

Cấu trúc Modular Monolith bạn đang có là **cái vỏ hoàn hảo**. Việc bạn chọn "ruột" là Stage nào sẽ quyết định độ linh hoạt của từng module đó. Bạn hoàn toàn có thể để module `notification` ở Stage 1 (đơn giản) trong khi `booking` ở Stage 5 (phức tạp).