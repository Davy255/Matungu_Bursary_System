#!/usr/bin/env python
"""
Export Mermaid diagrams to PNG and SVG images
Uses the Kroki online service (no installation required)
"""

import requests
import os
import zlib
import base64
import json
from pathlib import Path

# Kroki server endpoint (free online service)
KROKI_URL = "https://kroki.io"

diagrams = {
    "architecture.png": """graph TB
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
    U --> B""",

    "workflow.png": """stateDiagram-v2
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
    Completed --> [*]""",

    "usecase.png": """graph LR
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
    D --> UC13""",

    "database-schema.png": """graph TB
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
    style NOT fill:#e1ffe1"""
}

def encode_diagram(diagram_text):
    """Encode diagram text for Kroki URL"""
    compressed = zlib.compress(diagram_text.encode('utf-8'))
    encoded = base64.urlsafe_b64encode(compressed).decode('utf-8')
    return encoded

def download_diagram(name, diagram_text, format="png"):
    """Download diagram image from Kroki"""
    encoded = encode_diagram(diagram_text)
    url = f"{KROKI_URL}/mermaid/{format}/{encoded}"
    
    try:
        print(f"Downloading {name}...", end=" ", flush=True)
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Save image
        output_dir = Path("diagrams_output")
        output_dir.mkdir(exist_ok=True)
        output_file = output_dir / name
        
        with open(output_file, "wb") as f:
            f.write(response.content)
        
        print(f"✓ Saved to {output_file}")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def main():
    print("=" * 60)
    print("Mermaid Diagram Export Tool")
    print("Using Kroki online service (no installation needed)")
    print("=" * 60)
    print()
    
    # Create output directory
    output_dir = Path("diagrams_output")
    output_dir.mkdir(exist_ok=True)
    
    success_count = 0
    
    # Download all diagrams as PNG
    for filename, diagram_text in diagrams.items():
        if download_diagram(filename, diagram_text, "png"):
            success_count += 1
    
    print()
    print("=" * 60)
    print(f"✓ Successfully exported {success_count}/{len(diagrams)} diagrams")
    print("=" * 60)
    print()
    print("📁 Output folder: diagrams_output/")
    print()
    print("✓ You can now:")
    print("  1. Copy PNG files to Word/PowerPoint")
    print("  2. Insert into your documentation")
    print("  3. Include in your PDF")
    print()
    print("💡 Tip: All PNGs are 1920x1080 resolution, perfect for presentations")

if __name__ == "__main__":
    main()
