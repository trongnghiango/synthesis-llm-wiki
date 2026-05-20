---
id: dom-hrm-position-model
title: Nghiệp vụ Quản lý Nhân sự dựa trên Vị trí (Position-based HRM)
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on: []
summary: "Triết lý nghiệp vụ quản lý nhân sự dựa trên Vị trí công tác (Position-based) thay vì dựa trên Thực thể cá nhân độc lập."
tags: [domain, hrm, business, org-structure, position]
---

# Nghiệp vụ Quản lý Nhân sự dựa trên Vị trí (Position-based HRM)

Khác với các hệ thống quản trị nhân sự truyền thống tập trung vào hồ sơ cá nhân cá thể, STAX thiết kế module HRM theo triết lý **Position-based HRM** (Quản trị dựa trên Vị trí).

## 1. Triết lý Vị trí là Trung tâm
*   **Vấn đề của mô hình cũ:** Khi gán trực tiếp quyền hạn, tài sản, báo cáo cho một "Cá nhân Nhân viên" (Employee), khi nhân sự đó nghỉ việc hoặc thuyên chuyển, hệ thống phải cấu hình lại toàn bộ liên kết chéo cực kỳ phức tạp và dễ sót.
*   **Giải pháp STAX (Position-centric):** 
    *   Hệ thống định nghĩa sơ đồ tổ chức là một mạng lưới các **Vị trí công tác** (`Position`) thuộc các **Đơn vị tổ chức** (`OrgUnit`).
    *   Các quyền hạn, nhiệm vụ, quy trình phê duyệt, và luồng báo cáo (Reporting Line) được gán trực tiếp cho **Vị trí** (`Position`).
    *   **Nhân viên** (`Employee`) chỉ đóng vai trò là một thực thể tạm thời được bổ nhiệm (Assign) ngồi vào Vị trí đó trong một khoảng thời gian xác định.

## 2. Lợi ích vượt trội
Khi một nhân viên nghỉ việc:
1. Hệ thống chỉ cần rút gán bổ nhiệm nhân viên đó ra khỏi Vị trí.
2. Vị trí đó tạm thời trống (Vacant).
3. Khi nhân viên mới vào và được bổ nhiệm vào Vị trí này, họ tự động thừa hưởng toàn bộ quyền hạn, luồng công việc và lịch sử của Vị trí đó mà không cần bất kỳ thao tác phân quyền cấu hình lại nào.
