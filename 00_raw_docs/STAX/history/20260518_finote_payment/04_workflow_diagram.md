# Quy trình hoạt động (Workflow): Ghi nhận thanh toán Finote

Dưới đây là sơ đồ hóa toàn bộ kiến trúc và luồng dữ liệu (Data Flow) của tính năng **Ghi nhận thanh toán (Record Finote Payment)** mà chúng ta vừa triển khai, bao quát từ giao diện người dùng (Frontend) xuống đến cơ sở dữ liệu (Backend).

## 1. Sequence Diagram (Luồng tương tác hệ thống)

Sơ đồ này mô tả tuần tự các bước xảy ra từ khi Kế toán viên bấm nút "Thanh toán" cho đến khi giao diện cập nhật.

```mermaid
sequenceDiagram
    actor User as "Kế toán viên"
    participant UI as "React Frontend"
    participant API as "FinoteController"
    participant Service as "FinotePaymentService"
    participant TX as "TransactionManager"
    participant Domain as "Finote Entity"
    participant DB as "Postgres (Drizzle)"
    participant Bus as "EventBus & AuditLog"

    User->>UI: Bấm "Ghi nhận thanh toán"
    UI->>UI: Mở RecordPaymentDialog (Zod Validate)
    User->>UI: Nhập số tiền & Xác nhận
    
    UI->>API: POST /api/accounting/finotes/{id}/payments
    
    API->>Service: Gọi recordPayment(dto)
    Service->>TX: Mở Transaction (runInTransaction)
    
    rect rgb(234, 246, 255)
        Note right of TX: Bắt đầu Transaction (ALS)
        TX->>DB: Lấy thông tin Finote hiện tại
        DB-->>TX: Dữ liệu Finote
        
        TX->>Domain: Khởi tạo Entity & gọi finote.recordPayment()
        
        alt Nếu số tiền > Số dư còn lại
            Domain-->>Service: Ném lỗi BusinessRuleValidationException
            Service-->>API: 400 Bad Request
            API-->>UI: Hiển thị Toast báo lỗi
        else Hợp lệ
            Domain->>Domain: Cập nhật paidAmount & Status (PARTIALLY_PAID / PAID)
            
            TX->>DB: Insert vào bảng `cash_transactions` (Dòng tiền thật)
            TX->>DB: Insert vào bảng `finote_payments` (Mapping)
            TX->>DB: Update trạng thái & paidAmount bảng `finotes`
        end
    end
    
    Service->>Bus: Emit PaymentAllocatedEvent
    Service->>Bus: Ghi log (Action: PAYMENT_RECORDED)
    
    Service-->>API: Trả về Finote Entity mới
    API-->>UI: 200 OK (Response DTO)
    
    UI->>UI: Đóng Dialog & Invalidate Query
    UI->>API: Tự động fetch lại dữ liệu mới nhất
    API-->>UI: Dữ liệu đã cập nhật (Server-Driven UI)
    UI-->>User: Hiển thị trạng thái mới & Bảng Lịch sử thanh toán
```

---

## 2. Server-Driven UI (Kiểm soát giao diện từ Server)

Kiến trúc UI được thiết kế để không chứa logic cứng về nghiệp vụ, mà hoàn toàn dựa vào `_actions` từ backend trả về thông qua **Contract**.

```mermaid
graph TD
    subgraph BACKEND
        Entity["Finote Entity"] -->|Status PENDING| Rules{"Quy tac phan quyen"}
        Entity -->|Status PAID| Rules
        
        Rules -->|Da duyet, Chua tra het| ActionA["actions.recordPayment = true"]
        Rules -->|Da tra het PAID| ActionB["actions.recordPayment = false"]
        
        ActionA --> DTO["FinoteResponseDto"]
        ActionB --> DTO
    end

    subgraph FRONTEND
        DTO --> ReactQuery["useQuery Cache"]
        ReactQuery --> UI_List["Finotes List Page"]
        ReactQuery --> UI_Detail["Finotes Detail Page"]
        
        UI_List --> If1{"is allowed?"}
        UI_Detail --> If2{"is allowed?"}
        
        If1 -->|True| Btn1["Hien menu Thanh toan"]
        If2 -->|True| Btn2["Hien nut Thanh toan"]
        
        If1 -->|False| Hide1["An chuc nang"]
        If2 -->|False| Hide2["An chuc nang"]
    end
```

---

## 3. Cấu trúc Database (Rich Domain Model)

Mỗi lần thanh toán được ghi nhận, hệ thống lưu vết toàn diện để phục vụ đối soát (Reconciliation) sau này.

```mermaid
erDiagram
    FINOTES ||--o{ FINOTE_PAYMENTS : "được thanh toán qua"
    FINOTES {
        int id PK
        string status "PENDING, PARTIALLY_PAID, PAID"
        numeric amount "Tổng cần thu/chi"
        numeric paidAmount "Đã thu/chi (Tính toán)"
    }
    
    FINOTE_PAYMENTS ||--|| CASH_TRANSACTIONS : "liên kết với"
    FINOTE_PAYMENTS {
        int id PK
        int finoteId FK
        int cashTransactionId FK
        numeric amountMapped "Số tiền được gán cho phiếu này"
    }

    CASH_TRANSACTIONS {
        int id PK
        enum type "IN / OUT"
        numeric amount "Dòng tiền thực tế vào/ra khỏi két"
        datetime transactionDate "Ngày giao dịch thật"
        string transactionRef "Mã GD Ngân hàng"
    }
```
