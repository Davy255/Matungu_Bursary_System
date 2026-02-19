# Software Requirements Specification (SRS)

## 1. Introduction

### 1.1 Purpose

This document specifies the functional and non-functional requirements for the Matungu Subcounty Bursary Management System.

### 1.2 Scope

The system supports bursary applications, document submission, review, scoring, approval, and reporting for Matungu Subcounty.

### 1.3 Definitions and Acronyms

- Applicant: Student applying for bursary support.
- Ward Admin: Reviews applications at ward level.
- CDF Admin: Final approval authority.
- TVET: Technical and Vocational Education and Training.

## 2. Overall Description

### 2.1 Product Perspective

The system is a web-based application built with Django and MySQL. It integrates applicant-facing forms and an admin review workflow.

### 2.2 Product Functions

- User registration and authentication.
- Applicant profile management.
- Application submission with document upload.
- Review, scoring, and approval workflow.
- Notifications and reporting.

### 2.3 User Classes and Characteristics

- Applicants: Submit applications and track status.
- Ward Admins: Review and score applications in their wards.
- CDF Admins: Approve or reject applications.
- System Admins: Manage users, roles, and system settings.

### 2.4 Operating Environment

- Server: Linux/Windows server with Python 3.x and MySQL.
- Client: Modern web browser (Chrome, Edge, Firefox).

### 2.5 Design and Implementation Constraints

- Data privacy and integrity requirements.
- Internet connectivity requirements for users.

## 3. Functional Requirements

- FR1: The system shall allow applicants to register and log in.
- FR2: The system shall allow applicants to submit bursary applications.
- FR3: The system shall support document uploads per application.
- FR4: The system shall allow ward admins to review and score applications.
- FR5: The system shall allow CDF admins to approve or reject applications.
- FR6: The system shall generate reports by ward, category, and approval status.
- FR7: The system shall notify applicants of status changes.

## 4. Non-Functional Requirements

- Security: Role-based access control and data integrity.
- Reliability: System availability during application windows.
- Usability: Simple, mobile-friendly user interface.
- Performance: Handle concurrent users during peak periods.
- Maintainability: Modular architecture and clear documentation.

## 5. External Interface Requirements

- Web UI: Browser-based interface for applicants and admins.
- Email/SMS: Optional notification channels.

## 6. Data Requirements

Key entities include:

- User
- UserProfile
- SchoolCategory
- School
- Campus
- Program
- Ward
- Application
- ApplicationDocument
- ApplicationReview
- ApplicationApproval

## 7. Assumptions and Dependencies

- Users have reliable internet access.
- Administrators have valid credentials and assigned roles.
- External SMS or email services are configured when used.

## 8. Acceptance Criteria

- Applicants can register and submit applications.
- Admins can review and approve applications.
- Reports can be generated without errors.
- System prevents unauthorized access.
