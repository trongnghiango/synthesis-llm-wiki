---
id: hb-delta-logging
title: Nhật ký thay đổi dữ liệu dạng Delta (Delta Logging)
layer: 3-atomic
parent: "[[03_technical_handbooks]]"
depends_on: []
summary: "Hướng dẫn triển khai cơ chế Delta Logging chỉ ghi nhận biến động trước/sau của các trường thực sự thay đổi."
tags: [handbooks, logging, delta-logging, audit-log]
---

# Nhật ký thay đổi dữ liệu dạng Delta (Delta Logging)

Để tối ưu hóa dung lượng lưu trữ CSDL và giúp kiểm toán lịch sử nghiệp vụ dễ dàng, STAX sử dụng giải pháp **Delta Logging** cho tính năng Audit Log.

## 1. Nguyên lý hoạt động
Thay vì lưu trữ toàn bộ bản ghi mới và bản ghi cũ (gây lãng phí tài nguyên và khó so sánh), hệ thống chỉ ghi nhận danh sách các trường (fields) có giá trị thay đổi thực sự.

## 2. Định dạng dữ liệu thay đổi
Cấu trúc cột `changes` trong bảng `audit_logs` được thiết lập kiểu dữ liệu JSON với định dạng chuẩn:

```json
{
  "status": {
    "old": "DRAFT",
    "new": "ACTIVE"
  },
  "amount": {
    "old": 5000000,
    "new": 7500000
  }
}
```

## 3. Cách triển khai trong Use Case
1.  Đọc bản ghi cũ từ Database trước khi cập nhật.
2.  Chạy logic nghiệp vụ và lấy đối tượng mới sau khi thay đổi.
3.  Sử dụng hàm so sánh tĩnh `diff(oldEntity, newEntity)` để sinh ra object thay đổi Delta.
4.  Gửi object Delta này vào `AuditLogService` theo cơ chế **Fire-and-Forget** (chạy ngầm bên ngoài transaction).
