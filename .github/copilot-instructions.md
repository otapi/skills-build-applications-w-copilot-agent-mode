# GitHub Copilot Agent Instructions for OctoFit Tracker

## Project Overview

**OctoFit Tracker** is a fitness application built for Mergington High School to help students track physical activity, compete on leaderboards, and receive personalized workout suggestions. The app enables PE teacher Paul Octo to monitor student progress and create engaging fitness challenges.

**Core Features:**
- User authentication and profiles
- Activity logging (running, walking, strength training)
- Team creation and competition management
- Competitive leaderboards
- Personalized workout suggestions
- Gamification with achievement badges

## Architecture

### Technology Stack
- **Frontend:** React.js with Bootstrap (port 3000)
- **Backend:** Django REST API with Python (port 8000)
- **Database:** MongoDB (port 27017, private)
- **Environment:** GitHub Codespaces with Python virtual environment

### Directory Structure
```
octofit-tracker/
├── backend/
│   ├── venv/                 # Python virtual environment
│   ├── requirements.txt       # Python dependencies
│   └── octofit_tracker/       # Django project root
│       ├── manage.py
│       ├── settings.py
│       ├── urls.py
│       └── apps/             # Django apps
└── frontend/
    ├── src/
    │   ├── components/       # React components
    │   ├── pages/            # Page components
    │   └── index.js          # Bootstrap CSS imported here
    └── package.json
```

## Critical Workflows

### Never Change Directories in Agent Mode
When running commands, always point to the target directory using absolute or relative paths. Do not use `cd` commands. Example:
```bash
# ✅ Correct - point to directory
pip install -r octofit-tracker/backend/requirements.txt

# ❌ Never - change directory first
cd octofit-tracker/backend && pip install -r requirements.txt
```

### Backend Setup
1. Create Python virtual environment:
   ```bash
   python3 -m venv octofit-tracker/backend/venv
   ```

2. Activate and install dependencies (always point to directory):
   ```bash
   source octofit-tracker/backend/venv/bin/activate
   pip install -r octofit-tracker/backend/requirements.txt
   ```

3. Run migrations and start server:
   ```bash
   python octofit-tracker/backend/octofit_tracker/manage.py migrate
   python octofit-tracker/backend/octofit_tracker/manage.py runserver 0.0.0.0:8000
   ```

### Frontend Setup
1. Create React app (command points to correct directory):
   ```bash
   npx create-react-app octofit-tracker/frontend --use-npm
   ```

2. Install dependencies (always prefix with directory):
   ```bash
   npm install bootstrap --prefix octofit-tracker/frontend
   npm install react-router-dom --prefix octofit-tracker/frontend
   ```

3. Bootstrap CSS must be imported at the top of `src/index.js`

### MongoDB Service
- Check if MongoDB is running: `ps aux | grep mongod`
- Use official `mongosh` client tool for shell access
- **Always use Django's ORM for data creation**, never direct MongoDB scripts

## Project Conventions

### Django Backend (`octofit-tracker/backend/octofit_tracker/`)

**settings.py:**
- Always include dynamic `ALLOWED_HOSTS` for Codespace environment:
  ```python
  ALLOWED_HOSTS = ['localhost', '127.0.0.1']
  if os.environ.get('CODESPACE_NAME'):
      ALLOWED_HOSTS.append(f"{os.environ.get('CODESPACE_NAME')}-8000.app.github.dev")
  ```

**Serializers:**
- Convert MongoDB `ObjectId` fields to strings in serializer output

**URLs/URLs Configuration:**
- Use Codespace environment variable for dynamic URL generation:
  ```python
  codespace_name = os.environ.get('CODESPACE_NAME')
  if codespace_name:
      base_url = f"https://{codespace_name}-8000.app.github.dev"
  else:
      base_url = "http://localhost:8000"
  ```

**API Testing:**
- Use `curl` to test REST API endpoints

### React Frontend (`octofit-tracker/frontend/`)

- Always use `--prefix octofit-tracker/frontend` flag for npm commands
- Bootstrap CSS import should be first line in `src/index.js`
- App logo: `docs/octofitapp-small.png` (at repository root)

## Port Configuration

**Public ports (externally accessible):**
- 8000: Django backend API
- 3000: React frontend

**Private ports (internal only):**
- 27017: MongoDB

Do not propose or make other ports public.

## Required Python Dependencies

Key packages in `requirements.txt`:
- `Django==4.1.7` - Web framework
- `djangorestframework==3.14.0` - REST API support
- `djongo==1.3.6` - MongoDB integration with Django ORM
- `pymongo==3.12` - MongoDB driver
- `django-cors-headers==4.5.0` - CORS support
- `dj-rest-auth==2.2.6` - Auth endpoints
- `django-allauth==0.51.0` - User authentication

## Key Integration Points

1. **Frontend ↔ Backend Communication:** React components fetch data from Django API at `http://localhost:8000/api/`
2. **Database Access:** Django ORM (via djongo) handles all MongoDB interactions
3. **Authentication:** Use django-allauth for user registration/login flows
4. **CORS:** django-cors-headers manages cross-origin requests

## Important Reminders

- MongoDB must be running before Django migrations
- Use Django's ORM exclusively for data operations
- Test API endpoints with curl before integrating with frontend
- Environment variables determine URLs (Codespace vs. localhost)
- Never hardcode base URLs; use `CODESPACE_NAME` environment variable
