from typing import Dict, List
from models.candidate import Candidate, CandidateScore, Experience, Education, GitHubStats
from config import Config


class ScoringService:
    """Service for scoring and ranking candidates."""

    def __init__(self):
        self.weights = Config.SCORING_WEIGHTS
        self.faang_companies = Config.FAANG_COMPANIES
        self.frontier_labs = Config.FRONTIER_LABS
        self.top_tech_companies = Config.TOP_TECH_COMPANIES
        self.top_universities = Config.TOP_UNIVERSITIES

    def score_candidate(self, candidate: Candidate) -> CandidateScore:
        """
        Calculate comprehensive score for a candidate.

        Args:
            candidate: Candidate object with all profile information

        Returns:
            CandidateScore object with detailed scoring breakdown
        """
        score = CandidateScore()

        # Score FAANG experience
        score.faang_score = self._score_faang_experience(candidate.experiences)

        # Score Frontier Labs experience
        score.frontier_labs_score = self._score_frontier_labs_experience(candidate.experiences)

        # Score top tech companies experience
        score.top_tech_score = self._score_top_tech_experience(candidate.experiences)

        # Score GitHub activity
        if candidate.github_profile:
            score.github_score = self._score_github(candidate.github_profile)

        # Score X/Twitter engagement
        if candidate.x_profile:
            score.x_engagement_score = self._score_x_engagement(candidate.x_profile.engagement_score)

        # Score research publications
        score.research_score = self._score_research(candidate.publications)

        # Score education
        score.education_score = self._score_education(candidate.education)

        # Score years of experience
        score.experience_score = self._score_years_experience(candidate.total_years_experience)

        # Score open source contributions
        if candidate.github_profile:
            score.open_source_score = self._score_open_source(candidate.github_profile)

        # Score leadership roles
        score.leadership_score = self._score_leadership(candidate.experiences)

        # Calculate weighted total score
        score.total_score = (
            score.faang_score * self.weights['faang_experience'] / 100 +
            score.frontier_labs_score * self.weights['frontier_labs_experience'] / 100 +
            score.top_tech_score * self.weights['top_tech_companies'] / 100 +
            score.github_score * self.weights['github_activity'] / 100 +
            score.x_engagement_score * self.weights['x_engagement'] / 100 +
            score.research_score * self.weights['research_publications'] / 100 +
            score.education_score * self.weights['education_tier'] / 100 +
            score.experience_score * self.weights['years_experience'] / 100 +
            score.open_source_score * self.weights['open_source_contributions'] / 100 +
            score.leadership_score * self.weights['leadership_roles'] / 100
        )

        return score

    def determine_priority_tier(self, score: CandidateScore) -> str:
        """
        Determine priority tier based on total score.

        Args:
            score: CandidateScore object

        Returns:
            Priority tier: "top", "high", "medium", or "low"
        """
        total = score.total_score

        if total >= 75:
            return "top"
        elif total >= 60:
            return "high"
        elif total >= 40:
            return "medium"
        else:
            return "low"

    def _score_faang_experience(self, experiences: List[Experience]) -> float:
        """Score FAANG company experience (0-100)."""
        if not experiences:
            return 0.0

        faang_exp = [exp for exp in experiences if self._is_faang_company(exp.company)]

        if not faang_exp:
            return 0.0

        # Base score for having FAANG experience
        score = 50.0

        # Add points for duration
        total_months = sum(exp.duration_months for exp in faang_exp)
        score += min((total_months / 36) * 30, 30)  # Up to 30 points for 3+ years

        # Add points for seniority
        senior_roles = [exp for exp in faang_exp if self._is_senior_role(exp.title)]
        if senior_roles:
            score += 20

        return min(score, 100)

    def _score_frontier_labs_experience(self, experiences: List[Experience]) -> float:
        """Score Frontier AI Labs experience (0-100)."""
        if not experiences:
            return 0.0

        frontier_exp = [exp for exp in experiences if self._is_frontier_lab(exp.company)]

        if not frontier_exp:
            return 0.0

        # High base score - frontier labs are highly valuable
        score = 60.0

        # Add points for duration
        total_months = sum(exp.duration_months for exp in frontier_exp)
        score += min((total_months / 24) * 30, 30)  # Up to 30 points for 2+ years

        # Add points for research roles
        research_roles = [exp for exp in frontier_exp if 'research' in exp.title.lower()]
        if research_roles:
            score += 10

        return min(score, 100)

    def _score_top_tech_experience(self, experiences: List[Experience]) -> float:
        """Score other top tech company experience (0-100)."""
        if not experiences:
            return 0.0

        top_tech_exp = [
            exp for exp in experiences
            if self._is_top_tech_company(exp.company)
            and not self._is_faang_company(exp.company)
            and not self._is_frontier_lab(exp.company)
        ]

        if not top_tech_exp:
            return 0.0

        # Base score
        score = 40.0

        # Add points for duration
        total_months = sum(exp.duration_months for exp in top_tech_exp)
        score += min((total_months / 36) * 40, 40)

        # Add points for multiple companies
        unique_companies = len(set(exp.company for exp in top_tech_exp))
        score += min(unique_companies * 5, 20)

        return min(score, 100)

    def _score_github(self, github: GitHubStats) -> float:
        """Score GitHub activity (0-100)."""
        score = 0.0

        # Followers (max 20 points)
        score += min((github.followers / 500) * 20, 20)

        # Total stars (max 30 points)
        score += min((github.total_stars / 1000) * 30, 30)

        # Contributions (max 25 points)
        score += min((github.contributions_last_year / 500) * 25, 25)

        # Notable projects (max 15 points)
        score += min(len(github.notable_projects) * 3, 15)

        # Public repos (max 10 points)
        score += min((github.public_repos / 50) * 10, 10)

        return min(score, 100)

    def _score_x_engagement(self, engagement_score: float) -> float:
        """Score X/Twitter engagement (0-100)."""
        # engagement_score is already 0-100
        return min(engagement_score, 100)

    def _score_research(self, publications: List) -> float:
        """Score research publications (0-100)."""
        if not publications:
            return 0.0

        score = 0.0

        # Base score for having publications
        score += min(len(publications) * 10, 40)

        # Add points for citations (if available)
        total_citations = sum(pub.citations for pub in publications if hasattr(pub, 'citations') and pub.citations)
        score += min((total_citations / 100) * 40, 40)

        # Add points for recent publications
        recent_pubs = [pub for pub in publications if hasattr(pub, 'year') and pub.year and pub.year >= 2022]
        score += min(len(recent_pubs) * 5, 20)

        return min(score, 100)

    def _score_education(self, education: List[Education]) -> float:
        """Score educational background (0-100)."""
        if not education:
            return 0.0

        score = 0.0

        # Top university (max 60 points)
        top_uni_degrees = [edu for edu in education if self._is_top_university(edu.institution)]
        if top_uni_degrees:
            score += 60

            # Add points for advanced degrees
            for edu in top_uni_degrees:
                if edu.degree:
                    if 'PhD' in edu.degree or 'Ph.D' in edu.degree:
                        score += 30
                    elif 'Master' in edu.degree or 'MS' in edu.degree or 'M.S' in edu.degree:
                        score += 20
                    elif 'Bachelor' in edu.degree or 'BS' in edu.degree or 'B.S' in edu.degree:
                        score += 10

        else:
            # Any degree gets base points
            score += 30
            # Advanced degree bonus
            advanced_degrees = [
                edu for edu in education
                if edu.degree and ('PhD' in edu.degree or 'Master' in edu.degree)
            ]
            if advanced_degrees:
                score += 20

        return min(score, 100)

    def _score_years_experience(self, years: float) -> float:
        """Score years of experience (0-100)."""
        if years <= 0:
            return 0.0

        # Sweet spot is 5-15 years
        if years < 2:
            return years * 25  # 0-50 points for <2 years
        elif years < 5:
            return 50 + (years - 2) * 10  # 50-80 points for 2-5 years
        elif years < 15:
            return 80 + (years - 5) * 2  # 80-100 points for 5-15 years
        else:
            return 100  # 100 points for 15+ years

    def _score_open_source(self, github: GitHubStats) -> float:
        """Score open source contributions (0-100)."""
        score = 0.0

        # Public repos (max 30 points)
        score += min((github.public_repos / 30) * 30, 30)

        # Stars on projects (max 40 points)
        score += min((github.total_stars / 500) * 40, 40)

        # Notable projects (max 30 points)
        score += min(len(github.notable_projects) * 6, 30)

        return min(score, 100)

    def _score_leadership(self, experiences: List[Experience]) -> float:
        """Score leadership roles (0-100)."""
        if not experiences:
            return 0.0

        leadership_keywords = [
            'lead', 'principal', 'staff', 'senior', 'director',
            'manager', 'head', 'vp', 'chief', 'architect'
        ]

        leadership_roles = [
            exp for exp in experiences
            if any(keyword in exp.title.lower() for keyword in leadership_keywords)
        ]

        if not leadership_roles:
            return 0.0

        # Base score for leadership
        score = 40.0

        # Add points for seniority level
        for exp in leadership_roles:
            title_lower = exp.title.lower()
            if 'director' in title_lower or 'vp' in title_lower or 'chief' in title_lower:
                score += 30
            elif 'principal' in title_lower or 'staff' in title_lower:
                score += 20
            elif 'lead' in title_lower or 'senior' in title_lower:
                score += 10

        # Add points for duration in leadership
        total_months = sum(exp.duration_months for exp in leadership_roles)
        score += min((total_months / 36) * 20, 20)

        return min(score, 100)

    def _is_faang_company(self, company: str) -> bool:
        """Check if company is FAANG."""
        if not company:
            return False
        return any(faang.lower() in company.lower() for faang in self.faang_companies)

    def _is_frontier_lab(self, company: str) -> bool:
        """Check if company is a frontier AI lab."""
        if not company:
            return False
        return any(lab.lower() in company.lower() for lab in self.frontier_labs)

    def _is_top_tech_company(self, company: str) -> bool:
        """Check if company is a top tech company."""
        if not company:
            return False
        return any(tech.lower() in company.lower() for tech in self.top_tech_companies)

    def _is_top_university(self, institution: str) -> bool:
        """Check if institution is a top university."""
        if not institution:
            return False
        return any(uni.lower() in institution.lower() for uni in self.top_universities)

    def _is_senior_role(self, title: str) -> bool:
        """Check if title indicates a senior role."""
        if not title:
            return False
        senior_keywords = ['senior', 'staff', 'principal', 'lead', 'director', 'architect']
        return any(keyword in title.lower() for keyword in senior_keywords)
