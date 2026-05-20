---
title: "Event-Driven Architecture & Audit Log"
summary: "Kiến trúc hướng sự kiện (EDA) và hệ thống ghi vết hoạt động (Audit Trail) của STAX"
description: |
  Mô tả cách STAX sử dụng Event Bus để giao tiếp giữa các module (Decoupling) 
  và cách Audit Log tự động ghi lại các thay đổi quan trọng.
tags:
  - event-driven
  - event-bus
  - audit-log
  - decoupling
  - activity-feed
status: current
last_updated: "2026-05-10"
---

# 📂 Event-Driven Architecture & Audit Log

## 1. Event Bus System
STAX sử dụng một lớp trừu tượng `IEventBus` để decouple (giảm sự phụ thuộc) giữa các module.

### 1.1. Các loại Adapter
Hệ thống hỗ trợ 3 loại adapter tùy theo môi trường triển khai:
- **In-Memory**: Dùng cho phát triển local và test (nhanh, đơn giản).
- **RabbitMQ**: Dùng cho Production cần độ tin cậy cao.
- **Kafka**: Dùng khi hệ thống cần xử lý lượng sự kiện khổng lồ.

### 1.2. Luồng xử lý sự kiện
1. **Emit**: Một module (VD: Accounting) phát đi sự kiện `FinoteCreatedEvent`.
2. **Dispatch**: Event Bus chuyển sự kiện đến các Listener đã đăng ký.
3. **Listen**: Các module khác (VD: Notification) nhận sự kiện và thực hiện hành động (Gửi email).

## 2. Audit Log & Activity Feed
Hệ thống Audit Log của STAX được thiết kế để không xâm lấn (Non-invasive) và hiệu năng cao.

### 2.1. Ghi log tự động
Sử dụng Decorator hoặc Interceptor để tự động ghi lại:
- **Who**: Ai thực hiện? (User ID).
- **When**: Lúc nào? (Timestamp).
- **What**: Hành động gì? (Create/Update/Delete).
- **On**: Thực thể nào? (Lead, Finote, Contract).
- **Changes**: Thay đổi cụ thể là gì? (Old values vs New values).

### 2.2. Delta Logging
Thay vì lưu toàn bộ object, STAX chỉ lưu **Delta** (phần khác biệt). Điều này giúp tiết kiệm dung lượng database và dễ dàng hiển thị lịch sử thay đổi dưới dạng "X đã đổi Trạng thái từ A sang B".

## 3. Quy tắc "Fire and Forget"
Audit Log thường được thực hiện theo cơ chế "Fire and Forget" để không làm chậm request chính của người dùng. Nếu việc ghi log thất bại, request chính vẫn thành công.

---
*Tham khảo: `backend/src/modules/logging/` và `backend/src/core/shared/infrastructure/event-bus/`*
