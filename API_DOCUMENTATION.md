# API Documentation for HealthHub

## Authentication

All API endpoints (except login/register) require authentication.

### Login

```
POST /api-auth/login/
Content-Type: application/json

{
    "username": "R-dev-07",
    "password": "your_password"
}

Response:
{
    "key": "your_auth_token"
}
```

### Using Token Authentication

Include the token in the `Authorization` header:

```
Authorization: Token <your_token>
```

## Patient API

### Get Current Patient Profile

```
GET /patients/api/users/current_user/
Authorization: Token <token>

Response:
{
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": "+1234567890",
    "role": "patient",
    "profile_image": "https://...",
    "is_verified": true
}
```

### List Patient Profiles

```
GET /patients/api/patients/
Authorization: Token <token>

Response:
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "user": {...},
            "blood_group": "O+",
            "emergency_contact_name": "Jane Doe",
            "emergency_contact_number": "+1234567891",
            "allergies": "Penicillin",
            "medical_history": "Diabetes type 2",
            "height": 180,
            "weight": 75,
            "created_at": "2024-01-01T00:00:00Z"
        }
    ]
}
```

### Leave Review

```
POST /patients/api/reviews/
Authorization: Token <token>
Content-Type: application/json

{
    "doctor_id": 1,
    "rating": 5,
    "review_text": "Excellent doctor!"
}

Response:
{
    "id": 1,
    "patient_name": "John Doe",
    "doctor_name": "Dr. Smith",
    "rating": 5,
    "review_text": "Excellent doctor!",
    "created_at": "2024-01-01T00:00:00Z"
}
```

## Doctor API

### Get Current Doctor Profile

```
GET /doctors/api/doctors/my_profile/
Authorization: Token <token>

Response:
{
    "id": 1,
    "user_name": "Dr. Smith",
    "specialization": "cardiology",
    "registration_number": "REG123",
    "consultation_fee": "50.00",
    "bio": "Cardiology specialist with 10 years experience",
    "years_of_experience": 10,
    "is_verified": true,
    "average_rating": 4.5,
    "created_at": "2024-01-01T00:00:00Z"
}
```

### Get Doctor Reviews

```
GET /doctors/api/doctors/{id}/reviews/
Authorization: Token <token>

Response:
[
    {
        "id": 1,
        "patient_name": "John Doe",
        "doctor_name": "Dr. Smith",
        "rating": 5,
        "review_text": "Excellent doctor!",
        "created_at": "2024-01-01T00:00:00Z"
    }
]
```

### Create Prescription

```
POST /doctors/api/prescriptions/
Authorization: Token <token>
Content-Type: application/json

{
    "patient_id": 1,
    "appointment_id": 1,
    "medicines": "Aspirin 500mg",
    "dosage": "1 tablet twice daily",
    "duration": "7 days",
    "instructions": "Take with food"
}

Response:
{
    "id": 1,
    "doctor_name": "Dr. Smith",
    "patient_name": "John Doe",
    "medicines": "Aspirin 500mg",
    "dosage": "1 tablet twice daily",
    "duration": "7 days",
    "instructions": "Take with food",
    "created_at": "2024-01-01T00:00:00Z"
}
```

## Hospital API

### List Hospitals

```
GET /hospitals/api/hospitals/
Authorization: Token <token>

Response:
{
    "count": 10,
    "next": "http://.../hospitals/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "Central Hospital",
            "email": "info@central.com",
            "phone": "+1234567890",
            "address": "123 Main St",
            "city": "New York",
            "country": "USA",
            "website": "https://central.com",
            "description": "Leading hospital",
            "is_verified": true,
            "total_departments": 10,
            "created_at": "2024-01-01T00:00:00Z"
        }
    ]
}
```

### List Departments

```
GET /hospitals/api/departments/?hospital_id=1
Authorization: Token <token>

Response:
[
    {
        "id": 1,
        "hospital_name": "Central Hospital",
        "name": "cardiology",
        "description": "Heart and cardiology specialist department",
        "head_of_department": "Dr. Johnson",
        "total_beds": 20,
        "available_beds": 15,
        "created_at": "2024-01-01T00:00:00Z"
    }
]
```

## Appointment API

### List User's Appointments

```
GET /appointments/api/appointments/
Authorization: Token <token>

Response:
[
    {
        "id": 1,
        "patient_name": "John Doe",
        "doctor_name": "Dr. Smith",
        "hospital_name": "Central Hospital",
        "doctor_specialization": "Cardiology",
        "appointment_date": "2024-02-15T14:00:00Z",
        "status": "approved",
        "reason_for_visit": "Checkup",
        "is_paid": true,
        "created_at": "2024-01-01T00:00:00Z"
    }
]
```

### Create Appointment

```
POST /appointments/api/appointments/
Authorization: Token <token>
Content-Type: application/json

{
    "doctor_id": 1,
    "hospital_id": 1,
    "appointment_date": "2024-02-15T14:00:00Z",
    "reason_for_visit": "Checkup",
    "is_paid": false
}

Response:
{
    "id": 1,
    "patient_name": "John Doe",
    "doctor_name": "Dr. Smith",
    "hospital_name": "Central Hospital",
    "appointment_date": "2024-02-15T14:00:00Z",
    "status": "pending",
    "reason_for_visit": "Checkup",
    "is_paid": false,
    "created_at": "2024-01-01T00:00:00Z"
}
```

## Lab API

### List Available Tests

```
GET /labs/api/tests/
Authorization: Token <token>
Pagination: ?page=1&page_size=10

Response:
{
    "count": 50,
    "next": "http://.../tests/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "Complete Blood Count",
            "category": "blood",
            "description": "Full blood count analysis",
            "price": "25.00",
            "normal_range": "4.5-5.9 million/μL",
            "sample_required": "Blood",
            "turnaround_time": "24 hours",
            "is_active": true
        }
    ]
}
```

### Get Lab Reports

```
GET /labs/api/reports/
Authorization: Token <token>

Response:
[
    {
        "id": 1,
        "test_name": "Complete Blood Count",
        "patient_name": "John Doe",
        "result_value": "5.2 million/μL",
        "normal_range": "4.5-5.9 million/μL",
        "status": "completed",
        "test_date": "2024-01-15T10:00:00Z",
        "completion_date": "2024-01-16T15:00:00Z",
        "created_at": "2024-01-01T00:00:00Z"
    }
]
```

## Pharmacy API

### List Medicines

```
GET /pharmacy/api/medicines/?category=antibiotic
Authorization: Token <token>

Response:
[
    {
        "id": 1,
        "name": "Amoxicillin",
        "generic_name": "Amoxicillin Trihydrate",
        "category": "antibiotic",
        "price": "5.50",
        "stock_quantity": 100,
        "requires_prescription": true,
        "dosage": "500mg",
        "manufacturer": "Generic Pharma",
        "is_available": true,
        "in_stock": true
    }
]
```

### Get Medicine Details

```
GET /pharmacy/api/medicines/{id}/
Authorization: Token <token>

Response:
{
    "id": 1,
    "name": "Amoxicillin",
    "generic_name": "Amoxicillin Trihydrate",
    "category": "antibiotic",
    "description": "Beta-lactam antibiotic",
    "price": "5.50",
    "stock_quantity": 100,
    "requires_prescription": true,
    "dosage": "500mg",
    "side_effects": "Allergic reactions, nausea",
    "manufacturer": "Generic Pharma",
    "expiry_date": "2025-12-31",
    "is_available": true,
    "in_stock": true
}
```

### Place Medicine Order

```
POST /pharmacy/api/orders/
Authorization: Token <token>
Content-Type: application/json

{
    "items": [
        {
            "medicine_id": 1,
            "quantity": 2
        }
    ],
    "delivery_address": "123 Main St",
    "notes": "Call before delivery"
}

Response:
{
    "id": 1,
    "patient_name": "John Doe",
    "items": [
        {
            "id": 1,
            "medicine_name": "Amoxicillin",
            "quantity": 2,
            "unit_price": "5.50"
        }
    ],
    "total_amount": "11.00",
    "status": "pending_payment",
    "order_date": "2024-01-01T00:00:00Z",
    "delivery_date": null,
    "created_at": "2024-01-01T00:00:00Z"
}
```

## Payment API

### Get Payment History

```
GET /payments/api/payments/
Authorization: Token <token>

Response:
[
    {
        "id": 1,
        "transaction_id": "TXN123456",
        "patient_name": "John Doe",
        "payment_type": "appointment",
        "amount": "50.00",
        "status": "completed",
        "payment_method": "credit_card",
        "created_at": "2024-01-01T00:00:00Z",
        "paid_at": "2024-01-01T12:00:00Z"
    }
]
```

### Request Refund

```
POST /payments/api/refunds/
Authorization: Token <token>
Content-Type: application/json

{
    "payment_id": 1,
    "requested_amount": "50.00",
    "reason": "Doctor's appointment cancelled"
}

Response:
{
    "id": 1,
    "payment_info": {...},
    "requested_amount": "50.00",
    "reason": "Doctor's appointment cancelled",
    "status": "pending",
    "requested_at": "2024-01-01T00:00:00Z",
    "processed_at": null
}
```

## Chat API

### List Chat Rooms

```
GET /chat/api/chat-rooms/
Authorization: Token <token>

Response:
[
    {
        "id": 1,
        "patient_name": "John Doe",
        "doctor_name": "Dr. Smith",
        "is_active": true,
        "created_at": "2024-01-01T00:00:00Z",
        "last_message_at": "2024-01-15T10:30:00Z",
        "last_message": {
            "id": 5,
            "sender_name": "Dr. Smith",
            "message_type": "text",
            "content": "How are you feeling?",
            "is_read": true,
            "created_at": "2024-01-15T10:30:00Z"
        }
    }
]
```

### Get Messages in Room

```
GET /chat/api/chat-rooms/{id}/messages/
Authorization: Token <token>

Response:
[
    {
        "id": 1,
        "sender_name": "John Doe",
        "message_type": "text",
        "content": "Hello Doctor",
        "is_read": true,
        "created_at": "2024-01-15T10:00:00Z"
    },
    {
        "id": 2,
        "sender_name": "Dr. Smith",
        "message_type": "text",
        "content": "Hi John, how can I help?",
        "is_read": true,
        "created_at": "2024-01-15T10:15:00Z"
    }
]
```

## Error Responses

All errors follow this format:

```json
{
    "detail": "Error message",
    "error_code": "ERROR_CODE"
}
```

### Common Status Codes

- `200 OK` - Successful GET request
- `201 Created` - Successful POST request
- `204 No Content` - Successful DELETE request
- `400 Bad Request` - Invalid data
- `401 Unauthorized` - Missing authentication
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

## Rate Limiting

API calls are rate-limited to 1000 requests per hour per user.

Headers in response:
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1234567890
```

## WebSocket Endpoints

### Chat WebSocket

```
ws://localhost:8000/ws/chat/{chat_room_id}/

Messages:
{
    "message": "Your message content"
}

Response:
{
    "message": "Message content",
    "username": "John Doe",
    "user_id": 1,
    "timestamp": "2024-01-15T10:30:00Z"
}
```

## Pagination

```
GET /patients/api/patients/?page=1&page_size=10

Response:
{
    "count": 100,
    "next": "http://.../patients/?page=2&page_size=10",
    "previous": null,
    "results": [...]
}
```

## Filtering & Search

```
# Search by name
GET /patients/api/patients/?search=john

# Filter by status
GET /appointments/api/appointments/?status=approved

# Combine filters
GET /doctors/api/doctors/?specialization=cardiology&city=new_york
```

## Sorting

```
# Sort ascending (default)
GET /appointments/api/appointments/?ordering=appointment_date

# Sort descending
GET /appointments/api/appointments/?ordering=-appointment_date

# Multiple sort fields
GET /appointments/api/appointments/?ordering=-appointment_date,patient_name
```
