---
title: "ADR-006: Chiến lược Delta Logging"
status: accepted
date: 2026-04-26
tags: [architecture, logging, optimization]
---

# ADR-006: Chiến lược Delta Logging (Diff)

## Bối cảnh
Lưu trữ toàn bộ snapshot của thực thể sau mỗi lần thay đổi gây tốn dung lượng database cực lớn.

## Quyết định
Chuyển đổi sang Delta Logging (chỉ lưu phần khác biệt).

## Thiết kế
Sử dụng `ObjectDiff` utility để tính toán sự khác biệt giữa `before` và `after`. Chỉ những key bị thay đổi mới được lưu vào database.

## Lý do
Giảm 60-80% dung lượng database log, tăng hiệu năng query lịch sử.
