# Agentic AI Pharmacy Backend

This backend powers an **Agentic AI Pharmacy System**.
It provides real-time inventory management, order creation,
and stock control for AI agents and frontend dashboards.

---

## Tech Stack
- Python (Flask)
- SQLite (lightweight, persistent)
- ngrok (secure public tunneling for demo)
- REST APIs (JSON-first, agent-friendly)

---

## How to Run (Local)

```bash
cd backend
python app.py
Backend runs on:

http://127.0.0.1:5000
Public Demo Access (ngrok)
ngrok http 5000

Use the generated HTTPS URL as the Base URL for:

AI Agent

Frontend dashboard

API Contract (FINAL)
Health Check
GET /health
Inventory Lookup
GET /inventory/<medicine>
Create Order (reduces stock)
POST /create-order
{
  "customer_id": "PAT001",
  "medicine": "Paracetamol",
  "quantity": 2
}
Update Stock (admin / agent)
POST /update-stock
{
  "medicine": "Paracetamol",
  "delta": 10
}
Customer Order History
GET /customer-history/<customer_id>
Backend Guarantees

Stock never goes negative

Orders are transactional

SQLite is source of truth

APIs are deterministic & JSON-only

Designed for AI agent consumption

Notes for Hackathon Demo

Backend exposed securely via ngrok

No hardcoded mock data

Real inventory mutations

Designed to scale to real DB easily