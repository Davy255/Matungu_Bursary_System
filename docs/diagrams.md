# System Diagrams

## Figure 3.1: System Architecture Diagram

```mermaid
graph TB
    subgraph "Client Layer"
        A[Web Browser]
        B[Mobile Browser]
    end
    
    subgraph "Presentation Layer"
        C[Django Templates]
        D[Bootstrap 5 UI]
        E[Static Files CSS/JS]
    end
    
    subgraph "Application Layer"
        F[Django 6.0.2]
        G[URLs Routing]
        H[Views Logic]
        I[Forms Validation]
    end
    
    subgraph "Business Logic Layer"
        J[Users Module]
        K[Applications Module]
        L[Schools Module]
        M[Reviews Module]
        N[Notifications Module]
    end
    
    subgraph "Data Layer"
        O[Django ORM]
        P[Models]
        Q[Migrations]
    end
    
    subgraph "Database Layer"
        R[(MySQL 9.6)]
    end
    
    subgraph "Security Layer"
        S[Authentication]
        T[Authorization]
        U[HTTPS/SSL]
    end
    
    A --> C
    B --> C
    C --> D
    D --> E
    C --> G
    G --> H
    H --> I
    H --> J
    H --> K
    H --> L
    H --> M
    H --> N
    J --> O
    K --> O
    L --> O
    M --> O
    N --> O
    O --> P
    P --> Q
    Q --> R
    S --> H
    T --> H
    U --> A
    U --> B
```

---

## Figure 3.2: Entity-Relationship Diagram

```mermaid
erDiagram
    USER ||--o| USER_PROFILE : has
    USER {
        int id PK
        string username
        string email
        string password
        datetime date_joined
    }
    
    USER_PROFILE {
        int id PK
        int user_id FK
        string phone_number
        string national_id
        string role
        datetime created_at
    }
    
    SCHOOL_CATEGORY ||--o{ SCHOOL : contains
    SCHOOL_CATEGORY {
        int id PK
        string name
        string description
    }
    
    SCHOOL ||--o{ CAMPUS : has
    SCHOOL {
        int id PK
        int category_id FK
        string name
        string code
        string location
    }
    
    CAMPUS ||--o{ PROGRAM : offers
    CAMPUS {
        int id PK
        int school_id FK
        string name
        string location
    }
    
    PROGRAM {
        int id PK
        int campus_id FK
        string name
        string code
        string level
    }
    
    WARD ||--o{ APPLICATION : from
    WARD {
        int id PK
        string name
        string code
    }
    
    USER_PROFILE ||--o{ APPLICATION : submits
    PROGRAM ||--o{ APPLICATION : for
    APPLICATION {
        int id PK
        int applicant_id FK
        int program_id FK
        int ward_id FK
        string status
        decimal amount_requested
        datetime submitted_at
        string academic_documents
    }
    
    APPLICATION ||--o{ REVIEW : receives
    USER_PROFILE ||--o{ REVIEW : creates
    REVIEW {
        int id PK
        int application_id FK
        int reviewer_id FK
        string decision
        text comments
        datetime reviewed_at
    }
    
    APPLICATION ||--o{ NOTIFICATION : triggers
    NOTIFICATION {
        int id PK
        int application_id FK
        int user_id FK
        string message
        boolean is_read
        datetime created_at
    }
```

---

## Figure 3.3: Use Case Diagram

```mermaid
graph LR
    subgraph "Actors"
        A[Student/Applicant]
        B[Ward Administrator]
        C[Bursary Committee]
        D[System Admin]
    end
    
    subgraph "Use Cases"
        UC1[Register Account]
        UC2[Login]
        UC3[Submit Application]
        UC4[Upload Documents]
        UC5[Track Application]
        UC6[View Notifications]
        UC7[Review Applications]
        UC8[Approve/Reject]
        UC9[Generate Reports]
        UC10[Manage Users]
        UC11[Manage Schools]
        UC12[Configure System]
        UC13[View Dashboard]
    end
    
    A --> UC1
    A --> UC2
    A --> UC3
    A --> UC4
    A --> UC5
    A --> UC6
    
    B --> UC2
    B --> UC7
    B --> UC13
    B --> UC6
    
    C --> UC2
    C --> UC7
    C --> UC8
    C --> UC9
    C --> UC13
    
    D --> UC2
    D --> UC10
    D --> UC11
    D --> UC12
    D --> UC9
    D --> UC13
```

---

## Figure 1.1: Bursary Application Workflow

```mermaid
stateDiagram-v2
    [*] --> Registration: New User
    Registration --> Login: Account Created
    Login --> Dashboard: Authenticated
    
    Dashboard --> NewApplication: Start Application
    NewApplication --> FillForm: Enter Details
    FillForm --> UploadDocs: Add Information
    UploadDocs --> Submit: Complete
    
    Submit --> Pending: Application Submitted
    Pending --> UnderReview: Ward Admin Review
    
    UnderReview --> Verified: Documents Valid
    UnderReview --> Rejected: Documents Invalid
    
    Verified --> CommitteeReview: Forward to Committee
    CommitteeReview --> Approved: Meets Criteria
    CommitteeReview --> Rejected: Does Not Meet Criteria
    
    Approved --> Disbursement: Funds Allocated
    Disbursement --> Completed: Bursary Awarded
    
    Rejected --> Dashboard: Can Reapply
    Completed --> [*]
```

---

## Figure 3.4: Database Schema Overview

```mermaid
graph TB
    subgraph "Authentication"
        AUTH[auth_user]
        PROFILE[users_userprofile]
    end
    
    subgraph "Educational Institutions"
        CAT[schools_schoolcategory]
        SCH[schools_school]
        CAM[schools_campus]
        PRG[schools_program]
    end
    
    subgraph "Geographic"
        WRD[applications_ward]
    end
    
    subgraph "Applications"
        APP[applications_application]
        DOC[applications_document]
    end
    
    subgraph "Review Process"
        REV[reviews_review]
        CMT[reviews_comment]
    end
    
    subgraph "Communication"
        NOT[notifications_notification]
    end
    
    AUTH --> PROFILE
    PROFILE --> APP
    
    CAT --> SCH
    SCH --> CAM
    CAM --> PRG
    PRG --> APP
    
    WRD --> APP
    
    APP --> DOC
    APP --> REV
    APP --> NOT
    
    PROFILE --> REV
    REV --> CMT
    
    style AUTH fill:#e1f5ff
    style PROFILE fill:#e1f5ff
    style APP fill:#fff4e1
    style REV fill:#ffe1e1
    style NOT fill:#e1ffe1
```

---

## How to Use These Diagrams

### In Markdown/PDF:
These diagrams are written in Mermaid syntax and will render automatically in:
- GitHub (in README files)
- VS Code (with Mermaid extension)
- Many Markdown-to-PDF converters

### For Word/PowerPoint:
1. Open this file in VS Code
2. Install "Markdown Preview Mermaid Support" extension
3. Right-click on the diagram and "Copy as Image"
4. Paste into your document

### Online Rendering:
Visit https://mermaid.live/ and paste any diagram code to get a PNG/SVG export.
