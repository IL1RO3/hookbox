# HookBox

HookBox is a lightweight webhook inspection, debugging, and mock response server built with Django and Django REST Framework.

It allows you to generate webhook endpoints, capture and inspect incoming HTTP requests, return custom mock responses, replay requests to target servers, and export logs.

---

## 🚀 Running with Docker

### 1. Prerequisites
- [Docker](https://docs.docker.com/get-docker/) & [Docker Compose](https://docs.docker.com/compose/)

### 2. Configure Environment
Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Ensure `.env` contains your database connection string (used by both Django and Postgres containers):

```env
DATABASE_URL=postgres://postgres:postgres@db:5432/hookbox
```

### 3. Start Containers
Build and start the services in the background:

```bash
docker compose up -d --build
```

The database healthcheck will run and migrations will apply automatically before starting the server.

- **Base URL:** `http://localhost:8001`
- **Admin & API Auth:** `http://localhost:8001/api-auth/login/`

### 4. Create an API / Admin User
Create a superuser to access the management API:

```bash
docker compose exec backend python manage.py createsuperuser
```

---

## 🛠️ Features & Usage Guide

All management endpoints require authentication (Basic Auth or Session Auth). Webhook capture URLs are public.

### 1. Endpoint Management

#### Create an Endpoint
```bash
curl -X POST http://localhost:8001/api/endpoints/ \
  -u username:password \
  -H "Content-Type: application/json" \
  -d '{"name": "Stripe Webhook"}'
```
*Optional fields:*
- `expiration_date`: ISO 8601 timestamp (e.g. `"2026-12-31T23:59:59Z"`).
- `mock_enabled`: `true` or `false`.
- `mock_status`: HTTP status code (e.g. `200`).
- `mock_body`: JSON object returned to the sender.

Response includes your unique UUID `token`:
```json
{
  "name": "Stripe Webhook",
  "token": "4b68019e-e09b-44bb-ba5f-bbf4c15da021",
  "created_at": "...",
  "revoked": false
}
```

#### List & Filter Endpoints
```bash
# List all your endpoints
curl -u username:password http://localhost:8001/api/endpoints/

# Search by name and order by date
curl -u username:password "http://localhost:8001/api/endpoints/?search=Stripe&ordering=-created_at"
```

#### Rotate or Revoke Webhook Token
- **Rotate Token (generates new UUID):**
  ```bash
  curl -X PATCH http://localhost:8001/api/endpoints/<id>/token/ -u username:password
  ```
- **Revoke Token (deactivates endpoint):**
  ```bash
  curl -X DELETE http://localhost:8001/api/endpoints/<id>/token/ -u username:password
  ```

---

### 2. Capturing Incoming Webhooks

Send any HTTP request (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`) to your public webhook URL without authentication:

```bash
curl -X POST http://localhost:8001/api/webhook/<token>/ \
  -H "Content-Type: application/json" \
  -H "X-Custom-Header: value" \
  -d '{"event": "payment_succeeded", "amount": 1000}'
```

- Returns `{"recived": true}` with HTTP 201 Created by default.
- Returns `HTTP 410 Gone` if the endpoint is expired or revoked.
- Automatically captures payload, headers, query parameters, client IP, content type, and request duration.
- Protected by built-in rate limits (burst: 60/min, sustained: 1000/day).

---

### 3. Custom Mock Responses

Configure an endpoint to return custom status codes and payloads instead of default 201 responses:

```bash
curl -X PATCH http://localhost:8001/api/endpoints/<id>/ \
  -u username:password \
  -H "Content-Type: application/json" \
  -d '{
    "mock_enabled": true,
    "mock_status": 200,
    "mock_body": {"status": "success", "message": "Acknowledged"}
  }'
```

Any subsequent requests to `/api/webhook/<token>/` will receive HTTP `200` with your custom JSON payload.

---

### 4. Inspecting Request Logs

#### View Requests for a Specific Endpoint
```bash
# Get request history
curl -u username:password http://localhost:8001/api/endpoints/<id>/requests/

# Filter by HTTP method and order by date
curl -u username:password "http://localhost:8001/api/endpoints/<id>/requests/?method=POST&ordering=-received_at"
```

#### Global Request Logs
```bash
# List all captured requests across your endpoints
curl -u username:password "http://localhost:8001/api/request-logs/?method=POST&endpoint=<id>"

# Retrieve full details for a single request
curl -u username:password http://localhost:8001/api/request-logs/<request_id>/
```

---

### 5. Replaying Captured Requests

Forward a captured webhook to your local dev environment, staging, or production service:

```bash
curl -X POST http://localhost:8001/api/request-logs/<request_id>/replay/ \
  -u username:password \
  -H "Content-Type: application/json" \
  -d '{"url": "https://webhook.site/my-test-url"}'
```

HookBox preserves the original HTTP method, custom headers, query params, and body, and stores the response status and body in `replay_results`.

---

### 6. Exporting Logs to CSV

Export your request logs as a CSV file:

```bash
curl -u username:password http://localhost:8001/api/request-logs/export/ -o request-logs.csv
```

---

## 📋 Useful Docker Commands

| Command | Description |
|---|---|
| `docker compose up -d` | Start services in background |
| `docker compose down` | Stop services |
| `docker compose down -v` | Stop services and remove Postgres volume |
| `docker compose logs -f backend` | Follow application logs |
| `docker compose exec backend python manage.py test` | Run unit tests |
| `docker compose exec backend python manage.py shell` | Open Django shell |

---

## 📄 License
This project is licensed under the MIT License.
