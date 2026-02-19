# API Documentation - Bursary Management System

This document describes all API endpoints available in the Bursary Management System.

## Base URL

```
http://localhost:8000
```

## API Endpoints

### 1. Schools API

#### Get All School Categories

```
GET /schools/categories/
```

**Response:**
```json
{
  "status": "success",
  "data": [
    {
      "id": "uuid-here",
      "name": "University"
    },
    {
      "id": "uuid-here",
      "name": "College"
    },
    {
      "id": "uuid-here",
      "name": "TVET"
    }
  ]
}
```

#### Get Schools by Category

```
GET /schools/by-category/?category_id=<category-uuid>
```

**Parameters:**
- `category_id` (required): UUID of the school category

**Response:**
```json
{
  "status": "success",
  "data": [
    {
      "id": "uuid-here",
      "name": "University of Nairobi",
      "location": "Nairobi"
    }
  ]
}
```

#### Get Campuses by School

```
GET /schools/campuses/?school_id=<school-uuid>
```

**Parameters:**
- `school_id` (required): UUID of the school

**Response:**
```json
{
  "status": "success",
  "data": [
    {
      "id": "uuid-here",
      "name": "Main Campus",
      "location": "Nairobi",
      "city": "Nairobi"
    }
  ]
}
```

#### Get Programs by School

```
GET /schools/programs/?school_id=<school-uuid>
```

**Parameters:**
- `school_id` (required): UUID of the school

**Response:**
```json
{
  "status": "success",
  "data": [
    {
      "id": "uuid-here",
      "name": "Computer Science",
      "level": "Degree",
      "duration_months": 48,
      "tuition_fee": "50000.00"
    }
  ]
}
```

### 2. Users API

#### User Registration

```
POST /users/register/
Content-Type: application/x-www-form-urlencoded
```

**Request Parameters:**
- `username` (required): Unique username
- `email` (required): Valid email address
- `first_name` (required): User's first name
- `last_name` (required): User's last name
- `password1` (required): Password
- `password2` (required): Password confirmation

**Response:**
- Redirect to login on success
- Form errors on failure

#### User Login

```
POST /users/login/
Content-Type: application/x-www-form-urlencoded
```

**Request Parameters:**
- `username` (required): User's username
- `password` (required): User's password

**Response:**
- Redirect to dashboard on success
- Error message on failure

#### User Logout

```
GET /users/logout/
```

**Response:**
- Redirect to login page

#### Get User Profile

```
GET /users/profile/
Authentication: Required (login_required)
```

**Response:**
```html
Profile page with user information and admin role (if applicable)
```

#### Update User Profile

```
POST /users/profile/edit/
Authentication: Required (login_required)
Content-Type: multipart/form-data
```

**Request Parameters:**
- `first_name`: User's first name
- `last_name`: User's last name
- `email`: User's email
- `phone_number`: User's phone number
- `national_id`: User's national ID
- `county`: County selection
- `ward`: Ward selection
- `profile_photo`: Profile image (max 5MB)

**Response:**
- Redirect to profile on success
- Form errors on failure

### 3. Applications API

#### Get Applicant Dashboard

```
GET /applications/dashboard/
Authentication: Required (applicant)
```

**Response:**
```html
Dashboard with statistics and list of user's applications
```

#### Start New Application (Step 1)

```
POST /applications/new/step1/
Authentication: Required (applicant)
Content-Type: application/x-www-form-urlencoded
```

**Request Parameters:**
- `category`: UUID of school category
- `school`: UUID of school
- `program`: UUID of program

**Response:**
- Redirect to step 2 on success
- Error message on failure

#### Fill Application Form (Step 2)

```
POST /applications/new/<application-id>/step2/
Authentication: Required (applicant)
Content-Type: application/x-www-form-urlencoded
```

**Request Parameters:**
- `date_of_birth`: Date (YYYY-MM-DD)
- `gender`: Male/Female
- `national_id`: National ID
- `marital_status`: Single/Married/Other
- `phone_number`: Applicant's phone
- `email`: Applicant's email
- `family_income`: Annual family income (KES)
- `income_source`: Source of income
- `number_of_dependents`: Number of dependents
- `other_siblings_in_school`: Number of siblings in school
- `kcse_score`: KCSE aggregate score
- `stream`: Science/Arts/Commercial
- `admission_letter_number`: University admission letter number
- `motivation_letter`: Why you need bursary
- `expected_challenges`: Financial challenges

**Response:**
- Redirect to step 3 on success
- Form errors on failure

#### Upload Documents (Step 3)

```
POST /applications/new/<application-id>/step3/
Authentication: Required (applicant)
Content-Type: multipart/form-data
```

**Request Parameters:**
- `document_type_1`: Document type (KCSE_Certificate, etc.)
- `file_1`: File upload (max 5MB)
- `document_type_2`: Second document type
- `file_2`: Second file
- ... (multiple document types)

**Document Types:**
- KCSE_Certificate
- Admission_Letter
- Birth_Certificate
- National_ID
- Clearance_Letter
- Fee_Structure
- Income_Evidence
- Parents_ID
- Other

**Response:**
- Redirect to step 4 on success
- Error message on failure

#### Submit Application (Step 4)

```
POST /applications/new/<application-id>/step4/
Authentication: Required (applicant)
```

**Response:**
- Redirect to dashboard on success
- Error message on failure

#### Upload Single Document

```
POST /applications/<application-id>/upload-document/
Authentication: Required
Content-Type: multipart/form-data
```

**Request Parameters:**
- `document_type`: Document type
- `file`: File to upload

**Response:**
```json
{
  "status": "success",
  "message": "Document uploaded successfully",
  "document_id": "uuid-here"
}
```

#### Get Application Details

```
GET /applications/<application-id>/
Authentication: Required
```

**Response:**
```html
Application detail page with all information and documents
```

#### Track Application Status

```
GET /applications/track/
Authentication: Required (applicant)
```

**Response:**
```html
Page showing all applications and their statuses
```

#### Add Comment to Application

```
POST /applications/<application-id>/add-comment/
Authentication: Required
Content-Type: application/x-www-form-urlencoded
```

**Request Parameters:**
- `comment`: Comment text
- `is_internal`: True/False (internal notes)

**Response:**
```json
{
  "status": "success",
  "message": "Comment added successfully",
  "comment": {
    "id": "uuid-here",
    "text": "comment text",
    "author": "User Name",
    "date": "2024-02-19 10:30"
  }
}
```

### 4. Admin Applications API

#### Get Applications for Review

```
GET /admin-panel/applications/
Authentication: Required (admin)
```

**Query Parameters:**
- `status`: Application status (optional)
- `school`: School name (optional)
- `date_from`: Start date (optional)
- `date_to`: End date (optional)
- `search`: Search by name/ID (optional)
- `page`: Page number (optional)

**Response:**
```html
List of applications pending review with filters and pagination
```

#### Review Application

```
POST /admin-panel/applications/<application-id>/review/
Authentication: Required (admin)
Content-Type: application/x-www-form-urlencoded
```

**Request Parameters:**
- `academic_score`: Score 0-100
- `financial_need_score`: Score 0-100
- `supporting_documents_score`: Score 0-100
- `recommendation`: Approve/Reject/Clarify
- `comments`: Detailed comments

**Response:**
- Redirect to applications list on success
- Form errors on failure

#### Approve Application

```
POST /admin-panel/applications/<application-id>/approve/
Authentication: Required (admin)
Content-Type: application/x-www-form-urlencoded
```

**Request Parameters:**
- `amount_approved`: Approved amount (optional)
- `comments`: Approval comments

**Response:**
- Redirect to applications list on success
- Notification sent to applicant

#### Reject Application

```
POST /admin-panel/applications/<application-id>/reject/
Authentication: Required (admin)
Content-Type: application/x-www-form-urlencoded
```

**Request Parameters:**
- `reason`: Rejection reason

**Response:**
- Redirect to applications list on success
- Notification sent to applicant

#### Get Approved Applicants

```
GET /admin-panel/approved-applicants/
Authentication: Required (admin)
```

**Response:**
```html
List of all approved applicants with export options
```

#### Export Approved Applicants CSV

```
GET /admin-panel/export-csv/
Authentication: Required (admin)
```

**Response:**
- CSV file download

#### Get Admin Dashboard

```
GET /admin-panel/dashboard/
Authentication: Required (admin)
```

**Response:**
```html
Admin dashboard with statistics and recent applications
```

#### Get Reports

```
GET /admin-panel/reports/
Authentication: Required (admin)
```

**Response:**
```html
Reports page with graphs and statistics
```

### 5. Notifications API

#### Get User Notifications

```
GET /users/notifications/
Authentication: Required
```

**Query Parameters:**
- `page`: Page number (optional)

**Response:**
```html
List of user's notifications with pagination
```

#### Mark Notification as Read

```
POST /users/notifications/<notification-id>/read/
Authentication: Required
```

**Response:**
```json
{
  "status": "success"
}
```

#### Get Notification Preferences

```
GET /notifications/preferences/
Authentication: Required
```

**Response:**
```html
Form to manage email and SMS notification preferences
```

#### Update Notification Preferences

```
POST /notifications/preferences/
Authentication: Required
Content-Type: application/x-www-form-urlencoded
```

**Request Parameters:**
- `email_on_submission`: true/false
- `email_on_approval`: true/false
- `email_on_rejection`: true/false
- `email_on_comment`: true/false
- `email_on_update`: true/false
- `sms_on_submission`: true/false
- `sms_on_approval`: true/false
- `sms_on_rejection`: true/false
- `sms_on_update`: true/false

**Response:**
- Redirect to preferences on success
- Success message

### 6. Admin Role Management API

#### Assign Admin Role

```
POST /users/assign-admin-role/
Authentication: Required (superuser)
Content-Type: application/x-www-form-urlencoded
```

**Request Parameters:**
- `user`: UUID of user to assign
- `role_type`: Ward_Admin or CDF_Admin
- `ward`: Ward name

**Response:**
- Redirect to admin list on success
- Error message on failure

#### List All Admins

```
GET /users/admins/
Authentication: Required (superuser)
```

**Response:**
```html
List of all admin accounts with their roles and wards
```

#### Deactivate Admin

```
POST /users/admins/<admin-id>/deactivate/
Authentication: Required (superuser)
```

**Response:**
- Redirect to admin list on success
- Success message

## Authentication

Most endpoints require authentication. The system uses Django's session-based authentication.

### Login Before Using Protected Endpoints

```
1. POST to /users/login/ with credentials
2. Use returned session cookie for subsequent requests
```

## Error Responses

### Bad Request (400)
```json
{
  "status": "error",
  "message": "Missing required parameters"
}
```

### Unauthorized (401/403)
```json
{
  "status": "error",
  "message": "Permission denied"
}
```

### Not Found (404)
```json
{
  "status": "error",
  "message": "Resource not found"
}
```

## Rate Limiting

Currently not implemented. Consider implementing for production:
- IP-based rate limiting
- User-based rate limiting
- API key-based rate limiting

## Pagination

List endpoints support pagination with:
- `page`: Page number
- Default page size: 20 items

Example:
```
GET /applications/admin/list/?page=1
```

## Filtering & Search

Most list endpoints support:
- `search`: Search term
- `status`: Filter by status
- `date_from`: Start date (YYYY-MM-DD)
- `date_to`: End date (YYYY-MM-DD)

## File Upload Limits

- **Max file size**: 5 MB
- **Allowed formats**: PDF, PNG, JPG, JPEG, DOC, DOCX, XLS, XLSX

## Status Codes

- **200 OK**: Successful request
- **201 Created**: Resource created
- **204 No Content**: Successful deletion
- **400 Bad Request**: Invalid parameters
- **401 Unauthorized**: Not authenticated
- **403 Forbidden**: Permission denied
- **404 Not Found**: Resource not found
- **500 Internal Server Error**: Server error

## Example Workflows

### Complete Application Submission

```
1. POST /users/login/
   - Get session cookie

2. GET /schools/categories/
   - Get available school categories

3. GET /schools/by-category/?category_id=<cat-id>
   - Get schools in selected category

4. GET /schools/campuses/?school_id=<school-id>
   - Get campuses

5. GET /schools/programs/?school_id=<school-id>
   - Get programs

6. POST /applications/new/step1/
   - Create application

7. POST /applications/new/<app-id>/step2/
   - Fill personal info

8. POST /applications/new/<app-id>/step3/
   - Upload documents (multiple requests for each doc)

9. POST /applications/new/<app-id>/step4/
   - Submit application

10. Applicant receives email/SMS notification
```

### Admin Review Workflow

```
1. POST /users/login/
   - Admin login

2. GET /admin-panel/applications/
   - View pending applications

3. GET /applications/<app-id>/
   - View application details

4. POST /applications/<app-id>/add-comment/
   - Add comments if needed

5. POST /admin-panel/applications/<app-id>/approve/
   OR
   POST /admin-panel/applications/<app-id>/reject/
   - Make decision

6. Applicant receives notification
```

## Future API Enhancements

- RESTful API with DRF
- OAuth2 authentication
- API versioning
- GraphQL support
- WebSocket for real-time updates
- Rate limiting
- API documentation with Swagger/OpenAPI

---

**API Version**: 1.0  
**Last Updated**: February 2024

For more details, see the code or contact the development team.
