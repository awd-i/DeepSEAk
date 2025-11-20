"""
Profile Enrichment Service
Cross-references GitHub, X/Twitter, and LinkedIn profiles to build complete candidate profiles
"""

import re
from typing import Dict, Optional, List
from .github_analyzer import GitHubAnalyzer
from .x_analyzer import XAnalyzer
from .linkedin_scraper import LinkedInScraper
from .grok_client import GrokClient


class ProfileEnrichment:
    """Service to enrich candidate profiles by cross-referencing multiple platforms."""

    def __init__(self):
        self.github = GitHubAnalyzer()
        self.x_analyzer = XAnalyzer()
        self.linkedin = LinkedInScraper()
        self.grok = GrokClient()

    def enrich_from_github(self, github_username: str) -> Dict:
        """
        Start from GitHub username and enrich with X and LinkedIn data.

        Args:
            github_username: GitHub username

        Returns:
            Complete enriched profile
        """
        print(f"🔍 Enriching profile for GitHub user: {github_username}")

        # Get GitHub profile
        github_profile = self.github.get_user_profile(github_username)
        if not github_profile:
            print(f"❌ Could not fetch GitHub profile for {github_username}")
            return {}

        enriched_profile = {
            'name': github_profile.get('name') or github_username,
            'email': github_profile.get('email'),
            'github_profile': self.github.calculate_github_stats(github_username),
            'sources': ['github']
        }

        # Try to find X profile
        twitter_username = github_profile.get('twitter_username')
        if twitter_username:
            print(f"🐦 Found X username from GitHub: @{twitter_username}")
            x_profile = self._enrich_from_x(twitter_username)
            if x_profile:
                enriched_profile['x_profile'] = x_profile
                enriched_profile['sources'].append('x')

        # Try to find LinkedIn from GitHub bio or blog
        linkedin_url = self._find_linkedin_in_text(
            github_profile.get('bio', '') + ' ' + github_profile.get('blog', '')
        )

        if linkedin_url:
            print(f"💼 Found LinkedIn from GitHub: {linkedin_url}")
            enriched_profile['linkedin_url'] = linkedin_url
            enriched_profile['sources'].append('linkedin')

        # Use Grok to extract additional insights
        if github_profile.get('bio'):
            insights = self._extract_career_insights(github_profile['bio'], enriched_profile)
            enriched_profile.update(insights)

        return enriched_profile

    def enrich_from_x(self, x_username: str) -> Dict:
        """
        Start from X username and enrich with GitHub and LinkedIn data.

        Args:
            x_username: X/Twitter username

        Returns:
            Complete enriched profile
        """
        print(f"🔍 Enriching profile for X user: @{x_username}")

        # Get X profile
        x_profile = self.x_analyzer.get_user_profile(x_username)
        if not x_profile:
            print(f"❌ Could not fetch X profile for @{x_username}")
            return {}

        enriched_profile = {
            'name': x_profile.get('name') or x_username,
            'x_profile': {
                'username': x_profile['username'],
                'bio': x_profile.get('bio'),
                'followers': x_profile.get('followers', 0),
                'url': f"https://x.com/{x_username}"
            },
            'sources': ['x']
        }

        # Try to find GitHub username from bio or URL
        bio_text = x_profile.get('bio', '') + ' ' + x_profile.get('url', '')
        github_username = self._extract_github_username(bio_text)

        if github_username:
            print(f"💻 Found GitHub from X bio: {github_username}")
            github_stats = self.github.calculate_github_stats(github_username)
            if github_stats:
                enriched_profile['github_profile'] = github_stats
                enriched_profile['sources'].append('github')

                # Update email if available from GitHub
                github_profile = self.github.get_user_profile(github_username)
                if github_profile and github_profile.get('email'):
                    enriched_profile['email'] = github_profile['email']

        # Try to find LinkedIn
        linkedin_url = self._find_linkedin_in_text(bio_text)
        if linkedin_url:
            print(f"💼 Found LinkedIn from X: {linkedin_url}")
            enriched_profile['linkedin_url'] = linkedin_url
            enriched_profile['sources'].append('linkedin')

        # Extract career insights from bio
        if x_profile.get('bio'):
            insights = self._extract_career_insights(x_profile['bio'], enriched_profile)
            enriched_profile.update(insights)

        return enriched_profile

    def cross_reference_profiles(self, candidates: List[Dict]) -> List[Dict]:
        """
        Take a list of candidates and enrich each with cross-referenced profile data.

        Args:
            candidates: List of candidate dictionaries with at least one profile source

        Returns:
            List of enriched candidates
        """
        enriched_candidates = []

        for candidate in candidates:
            enriched = None

            # Start with GitHub if available
            if candidate.get('github_username'):
                enriched = self.enrich_from_github(candidate['github_username'])

            # Try X if GitHub didn't work or wasn't available
            elif candidate.get('x_username'):
                enriched = self.enrich_from_x(candidate['x_username'])

            if enriched:
                # Merge with original candidate data
                enriched.update({k: v for k, v in candidate.items() if k not in enriched})
                enriched_candidates.append(enriched)

        return enriched_candidates

    def _enrich_from_x(self, x_username: str) -> Optional[Dict]:
        """Helper to get X profile data."""
        x_profile = self.x_analyzer.get_user_profile(x_username)
        if x_profile:
            return {
                'username': x_profile['username'],
                'bio': x_profile.get('bio'),
                'followers': x_profile.get('followers', 0),
                'url': f"https://x.com/{x_username}"
            }
        return None

    def _extract_github_username(self, text: str) -> Optional[str]:
        """Extract GitHub username from text."""
        # Look for github.com/username patterns
        patterns = [
            r'github\.com/([a-zA-Z0-9-]+)',
            r'@([a-zA-Z0-9-]+)\s+(?:on|at)\s+GitHub',
            r'GitHub:\s+([a-zA-Z0-9-]+)'
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                username = match.group(1)
                # Filter out common non-username paths
                if username.lower() not in ['repos', 'issues', 'pulls', 'orgs', 'explore']:
                    return username

        return None

    def _find_linkedin_in_text(self, text: str) -> Optional[str]:
        """Extract LinkedIn profile URL from text."""
        patterns = [
            r'linkedin\.com/in/([a-zA-Z0-9-]+)',
            r'linkedin\.com/in/([a-zA-Z0-9-]+)/?'
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                username = match.group(1)
                return f"https://linkedin.com/in/{username}"

        return None

    def _extract_career_insights(self, bio: str, profile: Dict) -> Dict:
        """
        Use Grok to extract career insights from bio text.

        Args:
            bio: Biography text
            profile: Existing profile data

        Returns:
            Dictionary with current_title, current_company, etc.
        """
        prompt = f"""
        Analyze this professional bio and extract structured career information.

        Bio: {bio}

        Extract:
        1. Current job title (if mentioned)
        2. Current company (if mentioned)
        3. Previous notable companies (if mentioned)
        4. Education/degree (if mentioned)

        Return JSON format:
        {{
            "current_title": "...",
            "current_company": "...",
            "previous_companies": ["...", "..."],
            "education": "..."
        }}

        If any field is not mentioned, return null for that field.
        """

        try:
            response = self.grok.chat(prompt, temperature=0.1)
            # Parse response as JSON
            import json
            insights = json.loads(response)

            return {
                'current_title': insights.get('current_title'),
                'current_company': insights.get('current_company'),
                'previous_companies': insights.get('previous_companies', []),
                'education': insights.get('education')
            }
        except Exception as e:
            print(f"Error extracting career insights: {e}")
            return {}
