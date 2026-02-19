# PowerShell script to export Mermaid diagrams as images
# Requires: Node.js and mmdc (mermaid-cli)

# Install mermaid-cli if not already installed
Write-Host "Installing mermaid-cli..." -ForegroundColor Green
npm install -g @mermaid-js/mermaid-cli

# Create diagrams directory
$diagramsDir = ".\diagrams_output"
if (-not (Test-Path $diagramsDir)) {
    New-Item -ItemType Directory -Path $diagramsDir | Out-Null
}

# Array of diagram definitions
$diagrams = @(
    @{
        name = "architecture"
        file = "diagrams_output\architecture.mmd"
        mermaid = @"
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
"@
    },
    @{
        name = "workflow"
        file = "diagrams_output\workflow.mmd"
        mermaid = @"
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
"@
    },
    @{
        name = "usecase"
        file = "diagrams_output\usecase.mmd"
        mermaid = @"
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
"@
    }
)

# Create .mmd files and convert to PNG
foreach ($diagram in $diagrams) {
    $mmdFile = $diagram.file
    $pngFile = $mmdFile -replace '\.mmd$', '.png'
    $svgFile = $mmdFile -replace '\.mmd$', '.svg'
    
    # Write the Mermaid file
    Write-Host "Creating $($diagram.name)..." -ForegroundColor Cyan
    Set-Content -Path $mmdFile -Value $diagram.mermaid
    
    # Convert to PNG and SVG
    Write-Host "Converting $($diagram.name) to PNG..." -ForegroundColor Yellow
    mmdc -i $mmdFile -o $pngFile -w 1920 -H 1080
    
    Write-Host "Converting $($diagram.name) to SVG..." -ForegroundColor Yellow
    mmdc -i $mmdFile -o $svgFile
    
    Write-Host "✓ $($diagram.name) complete" -ForegroundColor Green
}

Write-Host "`nAll diagrams exported successfully!" -ForegroundColor Green
Write-Host "Check the 'diagrams_output' folder for PNG and SVG files" -ForegroundColor Cyan
Write-Host "`nYou can now:" -ForegroundColor Magenta
Write-Host "  1. Copy PNG files to Word/PowerPoint" -ForegroundColor White
Write-Host "  2. Use SVG files in web/PDF documents" -ForegroundColor White
Write-Host "  3. Insert into your final documentation" -ForegroundColor White
