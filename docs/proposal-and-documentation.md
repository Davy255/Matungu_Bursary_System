# MATUNGU SUBCOUNTY BURSARY MANAGEMENT SYSTEM

## Project Proposal and Documentation (Full Pack)

### Cover Page

**Title:** MATUNGU SUBCOUNTY BURSARY MANAGEMENT SYSTEM  
**Student:** WESONGA DAVID ONGOMA  
**Registration/ID:** SWESDA2211  
**Institution:** UNIVERSITY OF EASTERN AFRICA BARATON  
**Department:** INFORMATION SYSTEM AND COMMUNICATION  
**Submission Date:** ______________________

---

## Abstract

Bursary allocation in many counties is often slowed by manual processes, inconsistent eligibility verification, and weak audit trails. This project designs and implements a web-based Bursary Management System for Matungu Subcounty to streamline applicant intake, verification, scoring, approval workflows, and notification. The system provides role-based access for administrators, ward/CDF officers, and applicants. It integrates document uploads, automated validation, and a reporting layer that improves accountability. The solution is built with Django and MySQL and supports secure authentication, audit logging, and configurable business rules. The expected outcomes are reduced processing time, transparent selection, and improved service delivery to students.

---

# CHAPTER ONE: INTRODUCTION

## 1.1 Background of the Study

Bursaries play a critical role in supporting students from financially constrained households. In many subcounties, bursary processing involves paper-based forms, physical record storage, and manual approvals. This leads to delays, duplicate applications, loss of records, and minimal traceability. The Matungu Subcounty Bursary Management System seeks to digitize the end-to-end workflow, enabling applicants to submit forms and documents online, while administrators can review, score, and approve requests in a centralized system.

## 1.2 Problem Statement

The current bursary process in Matungu Subcounty is characterized by slow turnaround time, limited transparency, poor data accuracy, and weak security of applicant records. Manual verification and approval also increase administrative overhead and create opportunities for bias and errors. There is a need for a reliable, secure, and auditable system to manage bursary applications and decisions.

## 1.3 Objectives

### 1.3.1 General Objective

To design and implement a secure and efficient Bursary Management System for Matungu Subcounty that automates application, verification, and approval processes.

### 1.3.2 Specific Objectives

1. To develop a web-based application portal for bursary applicants.
2. To implement role-based access for ward, CDF, and system administrators.
3. To automate document submission and verification workflows.
4. To provide scoring, review, and approval tools for bursary committees.
5. To generate reports and analytics on bursary allocation.
6. To notify applicants about application status updates.

## 1.4 Research Questions

1. How can bursary application processes be digitized to reduce delays?
2. What security mechanisms are needed to protect applicant data?
3. How can the system ensure transparency and traceability in approvals?
4. What reporting features are required for audit and accountability?

## 1.5 Scope of the Study

The system focuses on bursary processing within Matungu Subcounty. It includes applicant registration, application submission, document upload, approval workflow, and notifications. The system does not handle tuition fee payment processing or integration with external national databases in the current scope.

## 1.6 Significance of the Study

The system improves service delivery for students, reduces administrative workload, and enhances transparency in bursary allocation. It also provides a structured database for reporting and decision-making.

## 1.7 Limitations

- Reliance on internet connectivity for applicants and administrators.
- Document verification is limited to uploaded evidence unless integrated with external systems.
- Future integration with SMS gateways and national ID verification is outside the current scope.

---

# CHAPTER TWO: LITERATURE REVIEW

## 2.1 Overview

This chapter reviews prior work on bursary systems, e-government application platforms, and workflow automation in public service management.

## 2.2 E-Government and Digital Service Delivery

E-government platforms improve citizen access to services by reducing physical visits and enabling transparent workflows. Studies show that digital portals reduce administrative bottlenecks and improve auditability.

## 2.3 Scholarship and Bursary Management Systems

Existing scholarship platforms emphasize online submission, document verification, and role-based decision approval. However, local contexts require custom workflows aligned with county structures.

## 2.4 Security and Data Protection

Systems handling personal and financial data require secure authentication, encryption of sensitive fields, role-based access, and audit logs. Compliance with data protection principles is critical.

## 2.5 Gap Analysis

Many existing systems are generalized, while Matungu Subcounty requires a tailored solution that supports ward-level filtering, local eligibility criteria, and a clear approval chain.

---

# CHAPTER THREE: SYSTEM ANALYSIS AND DESIGN

## 3.1 Requirements Analysis

### Functional Requirements

- User registration and login.
- Applicant profile creation.
- Bursary application submission with document uploads.
- Ward selection and filtering of schools by category.
- Review and scoring by admins.
- Approval, rejection, or pending decisions.
- Notifications for applicants.
- Reports and export features.

### Non-Functional Requirements

- Security: role-based access control and data integrity.
- Reliability: consistent availability of data and services.
- Usability: simple, mobile-friendly interface.
- Performance: support concurrent users during peak application period.
- Maintainability: modular codebase with clear documentation.

## 3.2 Use Case Summary

- Applicant registers and logs in.
- Applicant fills application and uploads required documents.
- Ward admin reviews and scores applications.
- CDF admin approves or rejects applications.
- System notifies applicant via email/SMS.

## 3.3 System Architecture

The system uses a three-tier architecture:

1. Presentation Layer (HTML/CSS/Bootstrap)
2. Application Layer (Django views, services, business logic)
3. Data Layer (MySQL database)

## 3.4 Database Design

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

## 3.5 Security Design

- Django authentication system.
- Unique user accounts with role-based permissions.
- Secure file upload handling.
- Input validation and server-side checks.

---

# CHAPTER FOUR: SYSTEM IMPLEMENTATION

## 4.1 Development Environment

- Python 3.x
- Django 4.2+ (upgraded for compatibility)
- MySQL database
- Bootstrap 5
- GitHub for version control

## 4.2 Key Modules

### User Module
- Registration, login, and profile management.

### Application Module
- Application creation and document upload.

### Review and Approval Module
- Review workflows and decision tracking.

### Notification Module
- Email and SMS templates (future integration).

## 4.3 Data Migration

Existing data migrated from SQLite to MySQL while preserving all records and relationships. This includes schools, wards, and applications.

---

# CHAPTER FIVE: TESTING, RESULTS, AND DISCUSSION

## 5.1 Testing Strategy

- Unit tests for model constraints.
- Integration testing of application workflows.
- UI testing for forms and admin dashboards.

## 5.2 Test Cases (Examples)

1. Applicant registration and login.
2. Application submission with valid documents.
3. Admin approval and notification triggers.

## 5.3 Results

The system successfully automates bursary processing, reduces manual tasks, and provides transparent audit trails for decisions.

## 5.4 Discussion

The system meets the stated objectives with improved workflow efficiency, security, and data management. Further enhancements can include national ID verification and payment integration.

---

# CHAPTER SIX: CONCLUSION AND RECOMMENDATIONS

## 6.1 Conclusion

The Matungu Subcounty Bursary Management System provides a robust, scalable solution for digitizing bursary applications and approvals. It improves transparency, reduces processing time, and enhances record management.

## 6.2 Recommendations

- Integrate SMS gateway for applicant notifications.
- Add analytics dashboards for allocation trends.
- Implement document verification integration with national databases.

## 6.3 Future Work

- Mobile app for applicants.
- Advanced fraud detection and duplicate checks.
- Integration with payment systems for direct disbursement.

---

# SOFTWARE REQUIREMENTS SPECIFICATION (SRS)

## 1. Introduction

### 1.1 Purpose

This SRS documents functional and non-functional requirements for the Matungu Subcounty Bursary Management System.

### 1.2 Scope

The system handles bursary applications, reviews, approvals, and reporting.

### 1.3 Definitions

- Applicant: Student applying for bursary.
- Ward Admin: Reviews applications at ward level.
- CDF Admin: Final approval authority.

## 2. Overall Description

- Web-based system with role-based access.
- Supports file upload and workflow review.

## 3. Functional Requirements

- FR1: User registration and login.
- FR2: Application submission with documents.
- FR3: Review and scoring.
- FR4: Approval decisions.
- FR5: Notifications and reporting.

## 4. Non-Functional Requirements

- Security: authentication and authorization.
- Usability: clear UI.
- Performance: responsive with concurrent users.

---

# SYSTEM DESIGN

## 1. Data Flow (High Level)

1. Applicant submits data.
2. Data stored in database.
3. Admins review and update status.
4. Notifications sent.

## 2. ER Overview

Key relationships include:

- User 1:1 UserProfile
- SchoolCategory 1:M School
- School 1:M Program
- Application 1:M ApplicationDocument

---

# USER MANUAL (SUMMARY)

## Applicant

1. Register and log in.
2. Complete application form.
3. Upload required documents.
4. Track application status.

## Admin

1. Log in with role account.
2. Review applications.
3. Score and approve/reject.
4. Generate reports.

---

# TESTING PLAN

- Unit tests for models and forms.
- Integration tests for workflows.
- User acceptance testing with administrators.

---

# DEPLOYMENT GUIDE (SUMMARY)

- Use PythonAnywhere free tier for hosting.
- Configure MySQL on PythonAnywhere.
- Set environment variables in `.env`.
- Run migrations and collect static files.

---

# APPENDICES

## Appendix A: Tools and Technologies

- Django
- MySQL
- Bootstrap
- PythonAnywhere

## Appendix B: Glossary

- CDF: Constituency Development Fund
- TVET: Technical and Vocational Education and Training
