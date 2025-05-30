# Subscription Billing System

## 1. Introduction

A lightweight SaaS billing backend built with Django that lets users sign up, subscribe to predefined plans, receive automated MONTHLY/QUATERLY/HALF_YEARLY/YEARLY invoices, pay via Stripe, and get periodic reminder emails before dues for pending invoices.

## 2. Tech Stack

- **Django 5.2.1**: Web framework & ORM
- **Django REST Framework**: RESTful API layer
- **Simple JWT**: Token-based authentication
- **Celery & django-celery-beat**: Asynchronous tasks & periodic scheduling
- **Redis**: Message broker & result backend for Celery
- **Stripe**: Payment processing & webhook integration (Work in process)
- **Docker & Docker Compose**: Containerization of all services

## 3. Installation & Setup

**Prerequisite:** Docker & Docker Compose installed

```bash
# 1. Clone repository
git clone git@github.com:Dhyey189/subscription-billing-system.git
cd subscription-billing-system

# 2. Copy env and set secrets
cp .env-example .env

# 3. Build & start services
docker-compose build
docker-compose up

# 4. Apply migrations & create superuser
docker exec -it django-web python manage.py migrate
docker exec -it django-web python manage.py createsuperuser

# 5. For Local Forward Stripe webhooks
stripe listen --forward-to http://127.0.0.1:8000/api/billing/stripe/webhook/
```

## 4. Access Admin and APIs

- **Admin**: http://127.0.0.1:8000/admin/
- **APIs**: http://127.0.0.1:8000/api/

## 5. Database Tables(Models)

- **User**: Allow signup & login using email and password.
- **Plan**: Predefined subscription tiers for which user can take subscriptions: name (Basic/Pro/Enterprise), plan_term (Monthly/Quarterly/Half Yearly/Yearly/), price, etc.
- **Subscription**: Tracks a user’s plan to which they are subscribed for, includes: user, plan, start_date, status (Active/Cancelled/Expired). Enforces one active subscription per user.
- **Invoice**: Stores invoice billing details which is used to charge users againsts thier subscription on start date of each billing cycle, include: user, subscription, amount, issue_date, due_date, status (Pending/Paid/Overdue), stripe_payment_intent.

## 6. API Endpoints

1. **POST** `/api/users/signup/`

   - Register a new user and receive JWT access tokens, further use access token to call secure authenticated APIs.

2. **POST** `/api/users/login/`

   - Authenticate with email and password to obtain JWT tokens, similary further use access token to call secure authenticated APIs, note: access_token will be valid for 5 mins.

3. **GET, POST** `/api/billing/subscriptions/`

   - GET: List subscriptions of logged-in user.
   - POST: Create a new subscription.

4. **GET, PATCH** `/api/billing/subscriptions/:id/`

   - GET: Retrieve details of subscription.
   - PATCH: Cancel or update subscription(unsubscribe).

5. **GET** `/api/billing/invoices/`

   - List all invoices for the logged-in user.

6. **GET** `/api/billing/invoices/:id/`

   - Get invoice details with payment status.

7. **GET** `/api/billing/invoices/:id/payment`

   - Get invoice's stripe payment intentent secret so that front-end can initiate the payment correctly.

8. To access all APIs using postman import file `Subscription Billing System.postman_collection.json` in your postman.

## 7. Features

- Dockerized setup (Django + Celery + Celery Beat + Redis).
- Django Rest Framework integration, utilized DRF views, serializers, permissions etc.
- DRF's JWT based Signup and Login.
- Admin panel with customized model registration (http://127.0.0.1:8000/admin/).
- Automated Invoice generation using celery on start of new billing cycle as per plan term.
- Automated email sending: invoice generation notification and invoice payment due reminders, using Django's template system.
- Integrated celery logging for automated and async tasks.
- Included POSTMAN collection: import file `Subscription Billing System.postman_collection.json` in your postman.
- Stripe integration for handling payments (WIP).
