---
title: "Quy trình Làm việc Nhóm"
description: "Quy trình quản trị context và vòng đời lưu trữ lịch sử phát triển"
tags: [standards, workflow, git, context, history]
last_updated: "2026-05-21"
---

# Quy trình Làm việc và Quản lý Bối cảnh (Team Workflow)

> Nguyên bản từ: `docs/standard_workflow.md`

## 1. Tổng quan
Để đảm bảo tính nhất quán và hỗ trợ tối đa cho các AI Agents, mọi thay đổi lớn (feature, bug fix, refactor) đều phải được lập tài liệu trong thư mục bối cảnh (`context`).

## 2. Cấu trúc Thư mục và Quy tắc Đặt tên
Mỗi đơn vị công việc phải được tạo trong một thư mục riêng biệt tại:
`docs/context/YYYYMMDD_{slug_tên_công_việc}`

### Cấu trúc tệp tin bắt buộc:
1. **`01_implementation_plan.md`**: Bản kế hoạch triển khai.
2. **`02_task.md`**: Danh sách các đầu việc (checklist).
3. **`03_walkthrough.md`**: Giải thích các thay đổi sau khi hoàn thành.

## 3. Vòng đời của một Context (Lifecycle)
1. **Khởi tạo (Start)**: Tạo thư mục trong `docs/context/`.
2. **Thực thi (Implementation)**: Cập nhật liên tục vào tệp `02_task.md`.
3. **Hoàn tất (Completion)**: Khi PR được Merge hoặc tính năng ổn định.
4. **Lưu trữ (Archiving)**: Di chuyển sang `docs/history/`.

## 4. Hướng dẫn dành riêng cho AI Agents
1. **Trước khi bắt đầu code**: Kiểm tra thư mục context, nếu chưa có hãy tạo mới.
2. **Trong quá trình làm việc**: Cập nhật `02_task.md` sau mỗi bước thành công.
3. **Trước khi kết thúc**: Hoàn thiện `03_walkthrough.md`.

---
*Đây là quy chuẩn bắt buộc cho mọi thành viên và AI hỗ trợ.*
