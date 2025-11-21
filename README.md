# DeepSEAk

AI-powered talent discovery platform that uses Grok and X API to find and score engineering candidates from X (Twitter), GitHub, and LinkedIn.

## Features

- **Multi-Source Discovery**: Automatically discover candidates from:
  - X/Twitter (high-engagement posts)
  - GitHub (trending developers, high-star repositories)
  - LinkedIn (via optional Proxycurl integration)

- **Intelligent Scoring**: Weighted algorithm that evaluates:
  - FAANG company experience (30 points)
  - Frontier AI Labs experience (35 points)
  - Top tech companies (25 points)
  - GitHub activity & stars (15 points)
  - X/Twitter engagement (10 points)
  - Research publications (20 points)
  - Education (top universities) (15 points)
  - Years of experience (10 points)
  - Open source contributions (12 points)
  - Leadership roles (8 points)

- **Priority Tiers**: Automatic classification
  - Top (75+ score)
  - High (60-74)
  - Medium (40-59)
  - Low (<40)

## Tech Stack

### Backend
- Python 3.8+
- Flask (API framework)
- Grok API (xAI)
- Supabase (PostgreSQL database)
- BeautifulSoup (web scraping)
- Pydantic (data validation)

### Frontend
- Next.js 15
- React 19
- TypeScript
- Tailwind CSS
- Vercel deployment ready

## Project Structure

```
grok-talent-engineer/
├── backend/
│   ├── app.py              # Flask application
│   ├── config.py           # Configuration
│   ├── requirements.txt    # Python dependencies
│   ├── .env               # Environment variables
│   ├── models/
│   │   └── candidate.py   # Data models
│   ├── services/
│   │   ├── grok_client.py # Grok API client
│   │   ├── x_analyzer.py  # X/Twitter analyzer
│   │   ├── github_analyzer.py # GitHub analyzer
│   │   ├── linkedin_scraper.py # LinkedIn scraper
│   │   ├── scoring_service.py # Scoring algorithm
│   │   └── database.py    # Supabase integration
│   └── routes/
│       ├── candidates.py  # Candidate endpoints
│       └── search.py      # Search endpoints
└── frontend/
    ├── app/
    │   └── page.tsx       # Main dashboard
    ├── components/
    │   └── CandidateCard.tsx
    ├── lib/
    │   └── api.ts         # API client
    ├── types/
    │   └── candidate.ts   # TypeScript types
    └── package.json
```

## Setup Instructions

### 1. Backend Setup

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
# The .env file already contains your Grok API key
# Add your Supabase credentials:
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
```

### 2. Supabase Database Setup

1. Create a free account at https://supabase.com
2. Create a new project
3. In the SQL Editor, run the schema from `backend/services/database.py`
4. Copy your project URL and anon key to `.env`

### 3. Run Backend

```bash
cd backend
python app.py
```

Backend will run on http://localhost:5000

### 4. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Frontend will run on http://localhost:3000

## API Endpoints

### Candidates
- `GET /api/candidates` - List all candidates
- `GET /api/candidates/:id` - Get specific candidate
- `POST /api/candidates` - Create candidate manually
- `PUT /api/candidates/:id` - Update candidate
- `DELETE /api/candidates/:id` - Delete candidate
- `GET /api/candidates/top` - Get top-ranked candidates
- `POST /api/candidates/discover/x` - Discover from X/Twitter
- `POST /api/candidates/discover/github` - Discover from GitHub

### Search
- `GET /api/search/candidates?q=query&tier=top&min_score=70`
- `GET /api/search/by-tier` - Group candidates by tier
- `GET /api/search/stats` - Get statistics
- `POST /api/search/suggestions` - Get Grok search suggestions

## Usage

### Discovering Candidates from X

```bash
curl -X POST http://localhost:5000/api/candidates/discover/x \
  -H "Content-Type: application/json" \
  -d '{
    "query": "machine learning engineer",
    "min_likes": 100,
    "min_retweets": 20
  }'
```

### Discovering Candidates from GitHub

```bash
curl -X POST http://localhost:5000/api/candidates/discover/github \
  -H "Content-Type: application/json" \
  -d '{
    "query": "machine learning",
    "min_followers": 100
  }'
```

### Searching Candidates

```bash
curl "http://localhost:5000/api/search/candidates?tier=top&min_score=75"
```

## Configuration

### Scoring Weights

Edit `backend/config.py` to adjust scoring weights:

```python
SCORING_WEIGHTS = {
    'faang_experience': 30,
    'frontier_labs_experience': 35,
    'top_tech_companies': 25,
    'github_activity': 15,
    'x_engagement': 10,
    'research_publications': 20,
    'education_tier': 15,
    'years_experience': 10,
    'open_source_contributions': 12,
    'leadership_roles': 8
}
```

### Company Lists

Add/modify companies in `backend/config.py`:

```python
FAANG_COMPANIES = ['Facebook', 'Meta', 'Apple', 'Amazon', 'Netflix', 'Google', 'Microsoft']
FRONTIER_LABS = ['OpenAI', 'Anthropic', 'DeepMind', ...]
TOP_TECH_COMPANIES = ['Tesla', 'SpaceX', 'Stripe', ...]
TOP_UNIVERSITIES = ['MIT', 'Stanford', 'Harvard', ...]
```

## Optional Integrations

### Twitter API (Recommended)

For better X/Twitter data:
1. Apply for Twitter API access at https://developer.twitter.com
2. Add bearer token to `.env`:
   ```
   TWITTER_BEARER_TOKEN=your_token_here
   ```

### GitHub Token (Recommended)

For higher rate limits:
1. Create token at https://github.com/settings/tokens
2. Add to `.env`:
   ```
   GITHUB_TOKEN=your_token_here
   ```

### LinkedIn via Proxycurl (Optional)

For LinkedIn data:
1. Sign up at https://nubela.co/proxycurl/
2. Add API key to `.env`:
   ```
   PROXYCURL_API_KEY=your_key_here
   ```

## Deployment

### Backend (Render/Railway)

```bash
# Create Procfile
web: gunicorn app:app

# Deploy to Render/Railway with environment variables
```

### Frontend (Vercel)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
cd frontend
vercel

# Set environment variable on Vercel:
NEXT_PUBLIC_API_URL=your_backend_url
```

## License

MIT

## Credits

- Powered by Grok API (xAI)
- Built with Next.js, Flask, and Supabase
