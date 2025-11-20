import os
from typing import Dict, List, Optional
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker, Session
from models.candidate import Candidate, CandidateModel, Base
import json
from datetime import datetime


class Database:
    """Database service for PostgreSQL operations using SQLAlchemy."""

    def __init__(self):
        url = os.getenv('DATABASE_URL')
        
        if not url:
            print("Warning: DATABASE_URL not found. Database operations will fail.")
            self.engine = None
            self.SessionLocal = None
        else:
            import time
            from sqlalchemy.exc import OperationalError
            
            retries = 5
            while retries > 0:
                try:
                    self.engine = create_engine(url)
                    # Test connection
                    with self.engine.connect() as conn:
                        pass
                    self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
                    print("Successfully connected to database.")
                    break
                except OperationalError as e:
                    retries -= 1
                    print(f"Database connection failed. Retrying in 5 seconds... ({retries} retries left)")
                    time.sleep(5)
            
            if retries == 0:
                print("Failed to connect to database after multiple attempts.")
                self.engine = None
                self.SessionLocal = None

    def init_schema(self):
        """Initialize database schema."""
        if self.engine:
            Base.metadata.create_all(bind=self.engine)
            print("Database schema initialized.")
            return "Schema initialized"
        return "Database not configured"

    def get_db(self):
        """Get database session."""
        if not self.SessionLocal:
            return None
        db = self.SessionLocal()
        try:
            return db
        except Exception:
            db.close()
            raise

    def add_candidate(self, candidate: Candidate) -> Optional[str]:
        """
        Add a new candidate to the database.
        """
        db = self.get_db()
        if not db:
            return None

        try:
            # Convert Pydantic model to SQLAlchemy model
            candidate_data = self._candidate_to_dict(candidate)
            # Remove id if it's None so database generates it
            if not candidate_data.get('id'):
                candidate_data.pop('id', None)
            
            db_candidate = CandidateModel(**candidate_data)
            db.add(db_candidate)
            db.commit()
            db.refresh(db_candidate)
            return db_candidate.id
        except Exception as e:
            print(f"Error adding candidate: {e}")
            db.rollback()
            return None
        finally:
            db.close()

    def update_candidate(self, candidate_id: str, updates: Dict) -> bool:
        """
        Update a candidate's information.
        """
        db = self.get_db()
        if not db:
            return False

        try:
            db_candidate = db.query(CandidateModel).filter(CandidateModel.id == candidate_id).first()
            if not db_candidate:
                return False

            for key, value in updates.items():
                if hasattr(db_candidate, key):
                    setattr(db_candidate, key, value)
            
            db_candidate.last_updated = datetime.utcnow()
            db.commit()
            return True
        except Exception as e:
            print(f"Error updating candidate: {e}")
            db.rollback()
            return False
        finally:
            db.close()

    def get_candidate(self, candidate_id: str) -> Optional[Candidate]:
        """
        Get a candidate by ID.
        """
        db = self.get_db()
        if not db:
            return None

        try:
            db_candidate = db.query(CandidateModel).filter(CandidateModel.id == candidate_id).first()
            if db_candidate:
                return self._model_to_candidate(db_candidate)
            return None
        except Exception as e:
            print(f"Error getting candidate: {e}")
            return None
        finally:
            db.close()

    def search_candidates(
        self,
        priority_tier: Optional[str] = None,
        min_score: Optional[float] = None,
        company: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Candidate]:
        """
        Search candidates with filters.
        """
        db = self.get_db()
        if not db:
            return []

        try:
            query = db.query(CandidateModel)

            if priority_tier:
                query = query.filter(CandidateModel.priority_tier == priority_tier)

            # Note: JSON querying in SQLAlchemy depends on dialect, 
            # but for simple score filtering we might need to cast or extract.
            # For now, we'll filter in Python if complex JSON query is needed, 
            # or assume score is stored in a way we can query. 
            # Since score is JSON, we can't easily do > comparison without specific PG operators.
            # Let's fetch and filter for min_score if it's critical, or rely on ordering.
            
            if company:
                query = query.filter(CandidateModel.current_company.ilike(f'%{company}%'))

            # Order by total score descending
            # We need to cast the JSON value to float for ordering
            # This syntax is specific to PostgreSQL
            from sqlalchemy import text
            query = query.order_by(text("(score->>'total_score')::float DESC"))

            results = query.limit(limit).offset(offset).all()
            
            candidates = [self._model_to_candidate(row) for row in results]
            
            if min_score is not None:
                candidates = [c for c in candidates if c.score.total_score >= min_score]
                
            return candidates

        except Exception as e:
            print(f"Error searching candidates: {e}")
            return []
        finally:
            db.close()

    def get_top_candidates(self, limit: int = 20) -> List[Candidate]:
        """Get top-ranked candidates."""
        return self.search_candidates(limit=limit)

    def get_candidates_by_tier(self, tier: str) -> List[Candidate]:
        """Get all candidates in a specific priority tier."""
        return self.search_candidates(priority_tier=tier, limit=1000)

    def delete_candidate(self, candidate_id: str) -> bool:
        """Delete a candidate."""
        db = self.get_db()
        if not db:
            return False

        try:
            db_candidate = db.query(CandidateModel).filter(CandidateModel.id == candidate_id).first()
            if db_candidate:
                db.delete(db_candidate)
                db.commit()
                return True
            return False
        except Exception as e:
            print(f"Error deleting candidate: {e}")
            db.rollback()
            return False
        finally:
            db.close()

    def get_all_candidates(self, limit: int = 1000) -> List[Candidate]:
        """Get all candidates."""
        db = self.get_db()
        if not db:
            return []

        try:
            results = db.query(CandidateModel).limit(limit).all()
            return [self._model_to_candidate(row) for row in results]
        except Exception as e:
            print(f"Error getting all candidates: {e}")
            return []
        finally:
            db.close()

    def _candidate_to_dict(self, candidate: Candidate) -> Dict:
        """Convert Candidate object to dictionary for database storage."""
        return {
            'id': candidate.id,
            'name': candidate.name,
            'email': candidate.email,
            'x_profile': candidate.x_profile.dict() if candidate.x_profile else None,
            'github_profile': candidate.github_profile.dict() if candidate.github_profile else None,
            'linkedin_url': candidate.linkedin_url,
            'current_title': candidate.current_title,
            'current_company': candidate.current_company,
            'experiences': [exp.dict() for exp in candidate.experiences],
            'total_years_experience': candidate.total_years_experience,
            'education': [edu.dict() for edu in candidate.education],
            'publications': [pub.dict() for pub in candidate.publications],
            'score': candidate.score.dict(),
            'priority_tier': candidate.priority_tier,
            'discovered_from': candidate.discovered_from,
            'discovery_date': candidate.discovery_date,
            'notes': candidate.notes
        }

    def _model_to_candidate(self, model: CandidateModel) -> Candidate:
        """Convert database model to Candidate object."""
        return Candidate(
            id=model.id,
            name=model.name,
            email=model.email,
            x_profile=model.x_profile,
            github_profile=model.github_profile,
            linkedin_url=model.linkedin_url,
            current_title=model.current_title,
            current_company=model.current_company,
            experiences=model.experiences or [],
            total_years_experience=model.total_years_experience or 0.0,
            education=model.education or [],
            publications=model.publications or [],
            score=model.score or {},
            priority_tier=model.priority_tier or 'low',
            discovered_from=model.discovered_from,
            discovery_date=model.discovery_date,
            last_updated=model.last_updated,
            notes=model.notes
        )
