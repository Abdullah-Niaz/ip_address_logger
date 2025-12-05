# IP Activity Logger

A lightweight Django application that tracks visitor IP addresses, user agents, visit frequency, and request paths. It offers a clean analytics dashboard to monitor recent visitors, traffic patterns, and per-IP activity. This project revises key Django concepts including middleware, models, admin customization, ORM queries, and optional third-party API integration.

## Features

* Logs every incoming request through custom middleware
* Extracts IP address, user agent, request path, and timestamp
* Tracks each unique visitor and their visit frequency
* Records per-request logs for better analytics
* Dashboard with recent visitors, unique IP count, top paths, and daily traffic
* Admin panel enhancements such as search, filters, and read-only fields
* Optional geolocation lookup using a public IP API
* Simple codebase suitable for beginners reviewing Django fundamentals

## Project Structure

```
ip_address_logger/
│
├─ iplogger/
│   ├─ middleware.py
│   ├─ models.py
│   ├─ views.py
│   ├─ admin.py
│   ├─ utils.py
│   ├─ templates/
│   │     └─ dashboard.html
│   ├─ urls.py
│
├─ ip_address_logger/
│   ├─ settings.py
│   ├─ urls.py
│
└─ manage.py
```

## How It Works

1. Every request is intercepted by `VisitorTrackingMiddleware`.
2. Middleware extracts IP, user agent, path, and timestamp.
3. A `Visitor` record is created or updated.
4. A new `VisitLog` entry is created for each request.
5. The analytics dashboard aggregates and displays visitor activity.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Abdullah-Niaz/ip_address_logger.git
   cd ip-activity-logger
   ```
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
3. Apply migrations:

   ```bash
   python manage.py migrate
   ```
4. Run the development server:

   ```bash
   python manage.py runserver
   ```

## Usage

Add the middleware to your Django settings.

```python
MIDDLEWARE = [
    ...
    'iplogger.middleware.VisitorTrackingMiddleware',
]
```

Include the app URLs in your `urls.py`:

```python
path('ip-dashboard/', include('iplogger.urls')),
```

Visit the dashboard:

```
http://127.0.0.1:8000/ip-dashboard/
```

## Optional: Geolocation Integration

Enable location lookup by adding an API call in `utils.py`.
For example, using `ipapi.co`:

```python
requests.get(f"https://ipapi.co/{ip}/json/")
```

Store the city, region, country in the `Visitor` model for richer insights.

## Admin Panel

The Django admin displays visitors and logs with:

* Search by IP
* Filters by date
* Read-only timestamps
* Visit count and last seen time

To access the admin panel:

```bash
python manage.py createsuperuser
```

## Technologies Used

* Python
* Django
* SQLite/PostgreSQL
* Requests (optional, for geolocation API)

## Learning Outcomes

This project reinforces:

* Custom middleware design
* Django ORM modeling
* Working with `request.META`
* Query filtering, aggregation, joins
* Template rendering and dashboard UI
* Integrating external APIs
* Admin panel customization


## Contribution

Pull requests are welcome. For major changes, open an issue to discuss your proposal.
