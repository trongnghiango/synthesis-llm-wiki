---
title: "Hiến pháp Kiến trúc"
description: "Quy tắc phân lớp nghiêm ngặt và ranh giới các thành phần trong Clean Architecture"
tags: [standards, architecture, boundaries, clean-architecture]
last_updated: "2026-05-21"
---

# Quy tắc Kiến trúc v1 (Architecture Rules)

> Nguyên bản từ: `docs/kien-truc.md`

## 1) Mục tiêu
Tài liệu này chuẩn hóa kiến trúc cho dự án theo hướng **mở rộng dài hạn**, tập trung vào:
1. Tăng tốc phát triển tính năng khi team lớn dần.
2. Giảm rủi ro “file trung tâm phình to”, conflict khi nhiều người cùng làm.
3. Chuẩn hóa boundary giữa `client`, `server`, `shared`.

## 2) Nguyên tắc Boundary bắt buộc
1. Module chỉ import chéo qua public API (`index.ts`) đã định nghĩa.
2. Không import sâu xuyên domain (ví dụ CRM import trực tiếp internals của HRM).
3. `shared/` chỉ chứa: contract (DTO/schema/type), primitives dùng chung, constants thuần kỹ thuật.
4. Không đặt business logic nặng vào `server/` BFF.

## 3) Cấu trúc thư mục mục tiêu
Tham khảo chi tiết tại: [Architecture Overview](../architecture/01_ARCHITECTURE.md)

### Client
```txt
client/src/
  app/          <-- Bootstrap, Router, Providers
  core/         <-- Shared logic (API client, Auth, RBAC)
  modules/      <-- Domain-driven modules (crm, hrm, etc.)
  shared-ui/    <-- Components dùng chung toàn hệ thống
  store/        <-- Global App State (Auth, UI metadata, Sockets)

## 4) Quy tắc Global Store (Zustand)
1. **App State Only**: Chỉ chứa dữ liệu dùng chung toàn hệ thống (Auth, Theme, Page Title, Sockets).
2. **No Domain Data**: Tuyệt đối không đưa dữ liệu nghiệp vụ (Employees, Leads, Invoices) vào Global Store. Hãy sử dụng React Query hoặc Module-level Store.
3. **Sliced Pattern**: Chia store thành các slices nhỏ và kết hợp tại `appStore.ts`.
```

### Server (BFF)
```txt
server/src/
  config/
  middlewares/
  proxy/
  routes/
```

## 4) Quy tắc thiết kế theo domain
- Mỗi domain có API layer riêng, hooks riêng, page/component riêng.
- Export qua `index.ts` để làm public API.
- Query key chuẩn: `['domain', 'resource', filters]`.

---
*Vui lòng tuân thủ nghiêm ngặt để đảm bảo tính module hóa của hệ thống.*
