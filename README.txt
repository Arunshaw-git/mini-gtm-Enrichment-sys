Company Enrichment Service
What i Built

A small gtm enriching system using the Explorium API as per requirements:

Backend (Python(FastAPI) + Celery + PostgreSQL + Redis)

Upload company domains via CSV.

Asynchronous enrichment using Celery workers:
    -first the parsed domains is saved in DB 
    -if not duplicate, it will trigger Celery task 
    -Celery uses Redis to store the tasks in a queue 
    -Celery take the tasks one by one asynchronously, updating the status to processing
    -Explorium api is called (first we get the business_id through the domain then call firmographics api which needs the id) and map the returned data to DB

Exposes REST endpoints to list companies and track enrichment status.

Frontend (react)
Table displaying enrichment status and results in real-time.



Key Tradeoffs:

Used Celery + Redis for async processing instead of full-featured task queue frameworks for simplicity.

Limited enrichment fields (industry, company size, revenue) for requirements; ignored optional fields.

Basic error handling and retries; did not implement advanced validation or rate-limiting.

UI is minimal — functionality prioritized over styling.


What i would Improve Next:

Add authentication and access control for API and UI.

Implement batch status updates to reduce DB queries.

Extend enrichment to include more fields from Explorium.

Improve frontend UX and UI, add filters, search, and sorting for companies.

Add unit & integration tests for backend tasks and API endpoints.