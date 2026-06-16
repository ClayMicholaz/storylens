# Personal News Intelligence Platform Project Charter

## Vision

Build a news platform that helps users discover high-quality articles relevant to their interests without relying on clickbait or algorithmic outrage.

The platform will:

- Aggregate real news from RSS feeds
- Learn user interests
- Recommend personalized content
- Track evolving stories
- Provide intelligent filtering and discovery

---

## Success Criteria

By the end of the project, a user should be able to:

1. Create an account
2. Read news from multiple sources
3. Save and organize articles
4. Receive personalized recommendations
5. Search articles efficiently
6. Follow specific topics over time
7. Receive a customized daily feed

---

## Resume Pitch

> Built a full-stack news recommendation platform using Next.js, FastAPI, PostgreSQL, and NLP-based recommendation models. Developed personalized content ranking, article similarity search, user profiling, and automated news aggregation from real-world RSS sources.

---

## Technical Stack

### Frontend

- Next.js
- TypeScript
- Tailwind CSS
- TanStack Query

### Backend

- FastAPI
- Python

### Database

- PostgreSQL

### ML/NLP

- Sentence Transformers
- scikit-learn
- Pandas

### Infrastructure

- Docker
- GitHub Actions
- Vercel
- Render or VPS

---

## Development Phases

### Phase 0 â€” Foundations

**Duration:** 1 week

**Goal:** Become comfortable with the stack

**Deliverables:**

- GitHub repository
- Project structure
- CI pipeline
- Development environment

#### Checkpoint 0.1

Install PostgreSQL, Python, Node.js

#### Checkpoint 0.2

Create directory structure:

```
frontend/
backend/
database/
docs/
```

#### Checkpoint 0.3

Initialize:

- **Frontend:** Next.js, TypeScript, Tailwind
- **Backend:** FastAPI, SQLAlchemy, Alembic

**Success Metric:** Frontend and backend communicate successfully

---

### Phase 1 News Collection Engine

**Duration:** 2 weeks

**Goal:** Collect real news automatically

#### Checkpoint 1.1

Create article schema with fields:

- id
- title
- content
- source
- url
- published_date
- category

#### Checkpoint 1.2

Build RSS parser using feedparser to collect from:

- Major tech feeds
- World news feeds
- Science feeds

#### Checkpoint 1.3

Implement deduplication using:

- URL hash
- Content hash

#### Checkpoint 1.4

Background job to fetch every hour

**Success Metric:** Database contains 500+ articles

---

### Phase 2 User System

**Duration:** 1 week

**Goal:** Users can create accounts

#### Checkpoint 2.1

Authentication system:

- Register
- Login
- Logout

#### Checkpoint 2.2

JWT implementation

#### Checkpoint 2.3

User preferences storage:

- Favorite topics
- Blocked topics
- Preferred sources

**Success Metric:** Users can customize interests

---

### Phase 3 Core Reader Experience

**Duration:** 1â€“2 weeks

**Goal:** Become usable as a news reader

#### Checkpoint 3.1

Homepage feed

#### Checkpoint 3.2

Article page

#### Checkpoint 3.3

Search using PostgreSQL Full Text Search

#### Checkpoint 3.4

Save articles functionality

#### Checkpoint 3.5

Reading history tracking

**Success Metric:** You personally use the app for several days

---

### Phase 4 NLP Pipeline

**Duration:** 2 weeks

**Goal:** Understand article content

#### Checkpoint 4.1

Article cleaning (remove HTML, scripts, noise)

#### Checkpoint 4.2

Generate embeddings using all-MiniLM-L6-v2 and store vectors

#### Checkpoint 4.3

Topic clustering using:

- KMeans
- HDBSCAN (later)

#### Checkpoint 4.4

Automatic tagging for: AI, Politics, Science, Business

**Success Metric:** Every article receives meaningful tags

---

### Phase 5 Recommendation System V1

**Duration:** 2 weeks

**Goal:** Personalized recommendations

#### Checkpoint 5.1

Track behavior:

- Clicks
- Saves
- Reading time

#### Checkpoint 5.2

Build user profile vectors (user embeddings)

#### Checkpoint 5.3

Content-based recommendations for articles similar to those consumed

#### Checkpoint 5.4

Ranking using: relevance + freshness

**Success Metric:** Feed noticeably improves over random articles

---

### Phase 6 Story Tracking

**Duration:** 2 weeks

**Goal:** Track evolving events (OpenAI releases model, election campaign, product launch)

#### Checkpoint 6.1

Cluster similar articles

#### Checkpoint 6.2

Create story entity with schema:

- stories

#### Checkpoint 6.3

Story page showing:

- Timeline
- Related articles

**Success Metric:** Users can follow developing events

---

### Phase 7 Recommendation System V2

**Duration:** 2 weeks

**Goal:** More advanced ranking

#### Checkpoint 7.1

Collaborative filtering for users with similar interests

#### Checkpoint 7.2

Hybrid recommendations combining:

- Embeddings
- User behavior
- Popularity

#### Checkpoint 7.3

Explore/exploit strategy to avoid filter bubbles

**Success Metric:** Recommendations feel personalized and diverse

---

### Phase 8 Production Engineering

**Duration:** 1â€“2 weeks

**Goal:** Make it professional

#### Checkpoint 8.1

Dockerize:

- Frontend
- Backend
- Database

#### Checkpoint 8.2

Monitoring (logs, metrics)

#### Checkpoint 8.3

Rate limiting

#### Checkpoint 8.4

Caching with Redis

**Success Metric:** Stable deployment

---

### Phase 9 Portfolio Polish

**Duration:** 1 week

**Goal:** Recruiter-ready

#### Checkpoint 9.1

Landing page

#### Checkpoint 9.2

Screenshots

#### Checkpoint 9.3

Architecture diagram

#### Checkpoint 9.4

README with:

- Motivation
- Architecture
- ML approach
- Deployment instructions

**Success Metric:** Someone can understand the project in 5 minutes

---

## Stretch Goals

Only after MVP is complete:

- Daily Digest (email personalized summaries)
- Topic Explorer (interactive topic graph)
- Follow Sources (subscribe to favorite publishers)
- Bias Analyzer (compare reporting across sources)
- Explain This Topic (generate beginner-friendly summaries)
- Mobile App (React Native)

---

## Portfolio Milestones

### Bronze ~35% Complete

- RSS aggregation
- Accounts
- Search
- Saved articles

### Silver ~65% Complete

- Embeddings
- Recommendations
- User profiling

### Gold ~90% Complete

- Story tracking
- Hybrid ranking
- Production deployment

### Platinum ~100% Complete

- Daily active users
- Analytics dashboard
- Email digests
- Advanced recommendation system

---

## The Most Important Rule

**Do not start with ML.**

Build in this order:

1. News collection
2. User accounts
3. Reading experience
4. Search
5. Recommendation engine
6. Advanced ML

A usable product with a simple recommendation engine is far more impressive than a sophisticated ML model attached to an unfinished website.
