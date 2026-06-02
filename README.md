# Practice FastAPI Task

### Features

- Add income and expense transactions
- Categorize transactions
- Filter by date range
- Show monthly summary
- Optional: budget limit per category

### WIP

- Filtering
- Add timestamps on modals (totally forgot that)

### Endpoints
```http
GET    /transactions/
POST   /transactions/

GET    /categories/
POST   /categories/

GET    /budget/
GET    /budget/?from=2026-05-01&to=2026-05-31
```