# TalimBot Backend

FastAPI backend server for the TalimBot student grouping system.

## Quick Start

```bash
# Install dependencies (one time only)
pip install -r requirements.txt

# Start the server
python main.py
```

Server will run on `http://localhost:8000`

## API Endpoints

- `GET /` - Health check
- `GET /api/students` - Get all students
- `GET /api/student/{id}` - Get specific student
- `PUT /api/student/{id}` - Update student info
- `POST /api/grouping/perform` - Perform AI grouping
- `GET /api/grouping/status` - Get grouping statistics
- `POST /api/grouping/toggle-visibility` - Show/hide results to students
- `POST /api/grouping/reset` - Reset grouping

## Configuration

### OpenRouter API Key
Located in `grouping_logic.py`:
```python
OPENROUTER_API_KEY = 'your-key-here'
```

### Teacher Password
Located in `main.py` (SystemData model):
```python
teacherPassword: str = "teacher123"
```

## Data Storage

Student data is stored in `data/students.json` (auto-created on first run)

## Dependencies

- fastapi - Web framework
- uvicorn - ASGI server
- pydantic - Data validation
- aiohttp - Async HTTP client for API calls

See `requirements.txt` for versions.
