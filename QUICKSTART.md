# Quick Start Guide

## Prerequisites

- Python 3.8+ installed
- Node.js 18+ installed
- npm or yarn installed

## 5-Minute Setup

### Step 1: Set up Supabase (2 minutes)

1. Go to https://supabase.com and create a free account
2. Click "New Project"
3. Choose a name and password
4. Wait for project to initialize
5. Go to Settings → API
6. Copy your "Project URL" and "anon public" key

### Step 2: Configure Backend (1 minute)

```bash
cd backend

# Edit .env file and add your Supabase credentials:
nano .env  # or use any text editor

# Add these lines:
SUPABASE_URL=your_project_url_here
SUPABASE_KEY=your_anon_key_here
```

### Step 3: Set up Database Schema (1 minute)

1. Open Supabase dashboard
2. Go to SQL Editor
3. Create new query
4. Copy and paste this SQL:

```sql
CREATE TABLE IF NOT EXISTS candidates (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    email TEXT,
    x_profile JSONB,
    github_profile JSONB,
    linkedin_url TEXT,
    current_title TEXT,
    current_company TEXT,
    experiences JSONB,
    total_years_experience NUMERIC DEFAULT 0,
    education JSONB,
    publications JSONB,
    score JSONB,
    priority_tier TEXT DEFAULT 'low',
    discovered_from TEXT,
    discovery_date TIMESTAMP DEFAULT NOW(),
    last_updated TIMESTAMP DEFAULT NOW(),
    notes TEXT,
    CONSTRAINT priority_tier_check CHECK (priority_tier IN ('low', 'medium', 'high', 'top'))
);

CREATE INDEX idx_candidates_priority_tier ON candidates(priority_tier);
CREATE INDEX idx_candidates_score ON candidates((score->>'total_score') DESC);
```

4. Click "Run"

### Step 4: Install Dependencies (1 minute)

```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend (in new terminal)
cd frontend
npm install
```

### Step 5: Start the Application

**Option A: Use the startup script (easiest)**
```bash
./start.sh
```

**Option B: Start manually**

Terminal 1 (Backend):
```bash
cd backend
python app.py
```

Terminal 2 (Frontend):
```bash
cd frontend
npm run dev
```

### Step 6: Access the Application

- Frontend: http://localhost:3000
- Backend API: http://localhost:5000
- API Health: http://localhost:5000/health

## Your First Discovery

### Discover from GitHub

```bash
curl -X POST http://localhost:5000/api/candidates/discover/github \
  -H "Content-Type: application/json" \
  -d '{
    "query": "machine learning",
    "min_followers": 100
  }'
```

Then refresh http://localhost:3000 to see discovered candidates!

## Troubleshooting

**Backend won't start?**
- Check that Python dependencies are installed: `pip list`
- Verify .env file has Supabase credentials
- Check backend/app.py for errors

**Frontend won't start?**
- Run `npm install` again in frontend directory
- Check that Node.js version is 18+: `node --version`
- Delete node_modules and reinstall: `rm -rf node_modules && npm install`

**No candidates showing?**
- Run a discovery command (see above)
- Check backend is running: http://localhost:5000/health
- Check browser console for errors (F12)

**Database errors?**
- Verify Supabase credentials in .env
- Make sure SQL schema was run in Supabase
- Check Supabase project is active

## Next Steps

1. **Get Twitter API Access** (optional but recommended)
   - Apply at https://developer.twitter.com
   - Add bearer token to .env

2. **Get GitHub Token** (recommended for higher rate limits)
   - Create at https://github.com/settings/tokens
   - Add to .env

3. **Customize Scoring**
   - Edit backend/config.py
   - Adjust company lists and weights

4. **Deploy to Production**
   - Backend: Deploy to Render or Railway
   - Frontend: Deploy to Vercel
   - Update NEXT_PUBLIC_API_URL in Vercel

## Support

- Check the main README.md for detailed documentation
- Review backend/README.md for API details
- Check code comments for implementation details
