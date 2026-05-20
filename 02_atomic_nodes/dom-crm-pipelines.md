---
id: dom-crm-pipelines
title: Quản lý Đường ống cơ hội bán hàng (CRM Kanban Pipeline)
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on: []
summary: "Nghiệp vụ quản trị cơ hội bán hàng (Leads) qua bảng trực quan Kanban và cơ chế tự động chuyển đổi sang tài khoản Organization."
tags: [domain, crm, kanban, leads, pipeline, business]
---

# Quản lý Đường ống cơ hội bán hàng (CRM Kanban Pipeline)

Hệ thống quản lý quan hệ khách hàng (CRM) của STAX tập trung vào việc quản lý vòng đời chuyển đổi của cơ hội kinh doanh (Leads) thông qua đường ống trực quan.

## 1. Trạng thái cơ hội (Lead Pipeline Stages)
Một Lead đi qua các giai đoạn chuyển đổi được thể hiện trên giao diện bảng Kanban:
1.  `Acquired` (Đã thu thập): Đầu mối thô được thu nhận qua web form hoặc Google Drive.
2.  `Contacted` (Đã liên hệ): Nhân viên bán hàng đã thực hiện cuộc gọi hoặc email trao đổi.
3.  `Qualified` (Đạt tiêu chuẩn): Cơ hội khả thi, khách hàng có nhu cầu thực tế và tài chính phù hợp.
4.  `Converted` (Đã chuyển đổi): Khách hàng đồng ý ký hợp đồng sử dụng dịch vụ.

## 2. Cơ chế chuyển đổi tự động (Automation Trigger)
Khi người dùng kéo thả Lead sang trạng thái `Converted`:
*   Hệ thống tự động kích hoạt Use Case tạo mới một **Doanh nghiệp (`Organization`)** tương ứng trong module Tier 2.
*   Đồng thời tự động sinh một tài khoản quản trị **User** cho người đại diện (`Contact`) của doanh nghiệp đó để họ có thể đăng nhập vào hệ thống khách hàng.
*   Giao dịch này được ràng buộc Transaction chặt chẽ chéo module để đảm bảo tính an toàn dữ liệu.
