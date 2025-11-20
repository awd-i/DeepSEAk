from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime, JSON, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
import uuid

Base = declarative_base()

class CandidateModel(Base):
    """SQLAlchemy model for candidates table."""
    __tablename__ = 'candidates'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    email = Column(String, nullable=True)
    
    # Social profiles (stored as JSON)
    x_profile = Column(JSON, nullable=True)
    github_profile = Column(JSON, nullable=True)
    linkedin_url = Column(String, nullable=True)
    
    # Professional info
    current_title = Column(String, nullable=True)
    current_company = Column(String, nullable=True)
    experiences = Column(JSON, default=list)
    total_years_experience = Column(Float, default=0.0)
    
    # Education
    education = Column(JSON, default=list)
    
    # Research
    publications = Column(JSON, default=list)
    
    # Scoring
    score = Column(JSON, default=dict)
    priority_tier = Column(String, default='low')
    
    # Metadata
    discovered_from = Column(String, nullable=True)
    discovery_date = Column(DateTime, default=datetime.utcnow)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    notes = Column(String, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'x_profile': self.x_profile,
            'github_profile': self.github_profile,
            'linkedin_url': self.linkedin_url,
            'current_title': self.current_title,
            'current_company': self.current_company,
            'experiences': self.experiences,
            'total_years_experience': self.total_years_experience,
            'education': self.education,
            'publications': self.publications,
            'score': self.score,
            'priority_tier': self.priority_tier,
            'discovered_from': self.discovered_from,
            'discovery_date': self.discovery_date.isoformat() if self.discovery_date else None,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None,
            'notes': self.notes
        }

class SocialProfile(BaseModel):
    """Social media profile information."""
    platform: str
    username: str
    url: str
    followers: Optional[int] = 0
    engagement_score: Optional[float] = 0.0


class Experience(BaseModel):
    """Work experience entry."""
    company: str
    title: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    duration_months: Optional[int] = 0
    description: Optional[str] = None
    is_faang: bool = False
    is_frontier_lab: bool = False
    is_top_tech: bool = False


class Education(BaseModel):
    """Education entry."""
    institution: str
    degree: Optional[str] = None
    field: Optional[str] = None
    start_year: Optional[int] = None
    end_year: Optional[int] = None
    is_top_university: bool = False


class GitHubStats(BaseModel):
    """GitHub statistics."""
    username: str
    url: str
    followers: int = 0
    public_repos: int = 0
    total_stars: int = 0
    contributions_last_year: int = 0
    top_languages: List[str] = []
    notable_projects: List[Dict] = []


class ResearchPublication(BaseModel):
    """Research publication entry."""
    title: str
    authors: List[str]
    venue: Optional[str] = None
    year: Optional[int] = None
    citations: Optional[int] = 0
    url: Optional[str] = None


class CandidateScore(BaseModel):
    """Scoring breakdown for a candidate."""
    total_score: float = 0.0
    faang_score: float = 0.0
    frontier_labs_score: float = 0.0
    top_tech_score: float = 0.0
    github_score: float = 0.0
    x_engagement_score: float = 0.0
    research_score: float = 0.0
    education_score: float = 0.0
    experience_score: float = 0.0
    open_source_score: float = 0.0
    leadership_score: float = 0.0


class Candidate(BaseModel):
    """Complete candidate profile."""
    id: Optional[str] = None
    name: str
    email: Optional[str] = None

    # Social profiles
    x_profile: Optional[SocialProfile] = None
    github_profile: Optional[GitHubStats] = None
    linkedin_url: Optional[str] = None

    # Professional information
    current_title: Optional[str] = None
    current_company: Optional[str] = None
    experiences: List[Experience] = []
    total_years_experience: float = 0.0

    # Education
    education: List[Education] = []

    # Research
    publications: List[ResearchPublication] = []

    # Scoring
    score: CandidateScore = Field(default_factory=CandidateScore)
    priority_tier: str = "low"  # low, medium, high, top

    # Metadata
    discovered_from: Optional[str] = None  # "x_post", "github_trending", etc.
    discovery_date: datetime = Field(default_factory=datetime.now)
    last_updated: datetime = Field(default_factory=datetime.now)
    notes: Optional[str] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
