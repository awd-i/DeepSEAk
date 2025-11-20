# Grok Talent Engineer - Backend

Flask-based API for discovering and scoring engineering talent using Grok AI.

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment:**
   - Copy `.env.example` to `.env`
   - Add your Supabase credentials (create project at https://supabase.com)
   - Grok API key is already configured

3. **Set up Supabase database:**
   - Create a Supabase project
   - Run the SQL schema from `services/database.py` in the SQL editor
   - Update `.env` with your Supabase URL and key

4. **Run the server:**
   ```bash
   python app.py
   ```

   Or with gunicorn:
   ```bash
   gunicorn app:app --bind 0.0.0.0:5000
   ```

## API Endpoints

### Candidates
- `GET /api/candidates` - List all candidates
- `POST /api/candidates` - Create candidate
- `GET /api/candidates/:id` - Get candidate
- `PUT /api/candidates/:id` - Update candidate
- `DELETE /api/candidates/:id` - Delete candidate
- `GET /api/candidates/top` - Get top candidates
- `POST /api/candidates/discover/x` - Discover from X/Twitter
- `POST /api/candidates/discover/github` - Discover from GitHub

### Search
- `GET /api/search/candidates` - Search with filters
- `GET /api/search/by-tier` - Group by priority tier
- `GET /api/search/stats` - Get statistics
- `POST /api/search/suggestions` - Get Grok search suggestions

## Architecture

```
backend/
├── app.py                 # Flask application
├── config.py              # Configuration and constants
├── models/
│   └── candidate.py      # Pydantic models
├── services/
│   ├── grok_client.py    # Grok API integration
│   ├── x_analyzer.py     # X/Twitter analysis
│   ├── github_analyzer.py # GitHub analysis
│   ├── linkedin_scraper.py # LinkedIn scraping
│   ├── scoring_service.py # Candidate scoring
│   └── database.py       # Supabase integration
└── routes/
    ├── candidates.py     # Candidate endpoints
    └── search.py         # Search endpoints
```

## Features

- **Multi-source discovery**: Find candidates from X, GitHub, and LinkedIn
- **Intelligent scoring**: Weighted algorithm for FAANG/Frontier Labs/Top Tech experience
- **Grok AI integration**: Use Grok for analyzing posts and profiles
- **Comprehensive profiles**: Education, experience, research, and social presence
- **Priority tiers**: Automatic classification (top/high/medium/low)
