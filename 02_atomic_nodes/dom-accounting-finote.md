---
id: dom-accounting-finote
title: Nghiệp vụ Chứng từ Kế toán dòng tiền (Finote & Cash Book)
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on: []
summary: "Chi tiết nghiệp vụ chứng từ thu/chi dòng tiền (Finote) và cơ chế tự động đồng bộ số dư Sổ quỹ (Cash Book)."
tags: [domain, accounting, finote, cash-book, business]
---

# Nghiệp vụ Chứng từ Kế toán dòng tiền (Finote & Cash Book)

Kế toán dòng tiền là mạch máu tài chính của doanh nghiệp, đòi hỏi sự kiểm soát giao dịch chặt chẽ và tính chính xác số dư tuyệt đối.

## 1. Thực thể Phiếu tài chính (`Finote`)
*   `Finote` (Financial Note) đại diện cho một chứng từ thu hoặc chi tiền thực tế của doanh nghiệp.
*   **Trạng thái vòng đời:** `DRAFT` (Nháp) ──► `PENDING_APPROVAL` (Chờ duyệt) ──► `APPROVED` (Đã duyệt) / `REJECTED` (Từ chối).
*   **Ràng buộc nghiệp vụ:** `Finote` khi tạo ra bắt buộc liên kết với một `organizationId` hợp lệ (Tenant context) và phải có `actorId` của kế toán viên thực hiện hành động.

## 2. Sổ quỹ tiền mặt (`Cash Book`) & Sự đồng bộ số dư
*   `Cash Book` theo dõi dòng lưu chuyển tiền thực tế và số dư tức thời.
*   **Cơ chế kích hoạt:** Khi và chỉ khi một `Finote` chuyển sang trạng thái `APPROVED` (Đã duyệt):
    *   Hệ thống sẽ tự động cộng (nếu là thu) hoặc trừ (nếu là chi) số tiền vào Sổ quỹ tương ứng.
    *   Tác vụ này được thực thi ngầm định trong cùng một Transaction cơ sở dữ liệu để bảo đảm tính nguyên tử: không thể có chuyện phê duyệt phiếu thành công mà số quỹ chưa đổi.
