import os
import requests
from typing import Dict, List, Optional
from bs4 import BeautifulSoup
import re


class LinkedInScraper:
    """
    LinkedIn profile scraper.

    IMPORTANT NOTE:
    LinkedIn actively blocks scraping and it violates their Terms of Service.

    For production use, consider these alternatives:
    1. LinkedIn API (requires partnership/approval)
    2. Third-party services like:
       - Proxycurl API (https://nubela.co/proxycurl/)
       - ScraperAPI with LinkedIn support
       - RapidAPI LinkedIn scrapers
    3. Manual input by users
    4. Browser automation (Selenium/Playwright) with proper auth

    This implementation provides a basic structure and mock data.
    """

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })

    def get_profile_from_url(self, linkedin_url: str) -> Optional[Dict]:
        """
        Extract profile information from LinkedIn URL.

        Args:
            linkedin_url: Full LinkedIn profile URL

        Returns:
            Profile dictionary with extracted information
        """
        # Extract username from URL
        username_match = re.search(r'linkedin\.com/in/([^/]+)', linkedin_url)
        if not username_match:
            return None

        username = username_match.group(1)

        # In production, you would:
        # 1. Use Proxycurl or similar API
        # 2. Use authenticated scraping with rate limiting
        # 3. Use browser automation

        # For now, return a structure with placeholders
        print(f"Warning: LinkedIn scraping not implemented. Would fetch: {linkedin_url}")

        return {
            'url': linkedin_url,
            'username': username,
            'method': 'placeholder',
            'note': 'Implement using Proxycurl API or similar service'
        }

    def get_profile_via_api(self, linkedin_url: str, api_key: Optional[str] = None) -> Optional[Dict]:
        """
        Get LinkedIn profile using Proxycurl API (recommended method).

        To use this:
        1. Sign up at https://nubela.co/proxycurl/
        2. Get API key
        3. Set PROXYCURL_API_KEY environment variable

        Args:
            linkedin_url: LinkedIn profile URL
            api_key: Proxycurl API key (optional, reads from env)

        Returns:
            Structured profile data
        """
        api_key = api_key or os.getenv('PROXYCURL_API_KEY')

        if not api_key:
            print("No Proxycurl API key found. Using mock data.")
            return self._get_mock_profile(linkedin_url)

        url = "https://nubela.co/proxycurl/api/v2/linkedin"
        headers = {'Authorization': f'Bearer {api_key}'}
        params = {'url': linkedin_url}

        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()

            # Parse and structure the response
            return self._parse_proxycurl_response(data)

        except requests.exceptions.RequestException as e:
            print(f"Error fetching LinkedIn profile: {e}")
            return self._get_mock_profile(linkedin_url)

    def search_profile_by_name(self, name: str, company: Optional[str] = None) -> Optional[str]:
        """
        Search for LinkedIn profile URL by name and company.

        Args:
            name: Person's name
            company: Optional company name to narrow search

        Returns:
            LinkedIn profile URL if found
        """
        # This would use LinkedIn search or Google search
        # For now, return None as this requires proper implementation
        print(f"Searching LinkedIn for: {name}" + (f" at {company}" if company else ""))
        return None

    def extract_experience(self, profile_data: Dict) -> List[Dict]:
        """
        Extract and structure experience from profile data.

        Args:
            profile_data: Raw profile data

        Returns:
            List of experience dictionaries
        """
        experiences = profile_data.get('experiences', [])

        structured_experiences = []
        for exp in experiences:
            structured_experiences.append({
                'company': exp.get('company'),
                'title': exp.get('title'),
                'start_date': exp.get('starts_at'),
                'end_date': exp.get('ends_at'),
                'duration_months': self._calculate_duration(
                    exp.get('starts_at'),
                    exp.get('ends_at')
                ),
                'description': exp.get('description'),
                'location': exp.get('location')
            })

        return structured_experiences

    def extract_education(self, profile_data: Dict) -> List[Dict]:
        """
        Extract and structure education from profile data.

        Args:
            profile_data: Raw profile data

        Returns:
            List of education dictionaries
        """
        education = profile_data.get('education', [])

        structured_education = []
        for edu in education:
            structured_education.append({
                'institution': edu.get('school'),
                'degree': edu.get('degree_name'),
                'field': edu.get('field_of_study'),
                'start_year': edu.get('starts_at', {}).get('year'),
                'end_year': edu.get('ends_at', {}).get('year')
            })

        return structured_education

    def _parse_proxycurl_response(self, data: Dict) -> Dict:
        """Parse Proxycurl API response into our format."""
        return {
            'url': data.get('public_identifier'),
            'full_name': data.get('full_name'),
            'first_name': data.get('first_name'),
            'last_name': data.get('last_name'),
            'headline': data.get('headline'),
            'summary': data.get('summary'),
            'location': data.get('city'),
            'country': data.get('country'),
            'current_company': data.get('experiences', [{}])[0].get('company') if data.get('experiences') else None,
            'current_title': data.get('experiences', [{}])[0].get('title') if data.get('experiences') else None,
            'experiences': self.extract_experience(data),
            'education': self.extract_education(data),
            'skills': data.get('skills', [])
        }

    def _calculate_duration(self, start_date: Optional[Dict], end_date: Optional[Dict]) -> int:
        """Calculate duration in months between two dates."""
        if not start_date:
            return 0

        start_year = start_date.get('year', 0)
        start_month = start_date.get('month', 1)

        if end_date:
            end_year = end_date.get('year', 0)
            end_month = end_date.get('month', 12)
        else:
            # Current position
            from datetime import datetime
            now = datetime.now()
            end_year = now.year
            end_month = now.month

        if start_year and end_year:
            return (end_year - start_year) * 12 + (end_month - start_month)

        return 0

    def _get_mock_profile(self, linkedin_url: str) -> Dict:
        """Return mock LinkedIn profile for testing."""
        username = re.search(r'linkedin\.com/in/([^/]+)', linkedin_url)
        username = username.group(1) if username else 'unknown'

        return {
            'url': linkedin_url,
            'username': username,
            'full_name': 'Mock User',
            'headline': 'Senior Software Engineer',
            'current_company': 'Tech Company',
            'current_title': 'Senior Software Engineer',
            'experiences': [
                {
                    'company': 'Google',
                    'title': 'Software Engineer',
                    'start_date': '2020-01',
                    'end_date': '2023-06',
                    'duration_months': 42,
                    'description': 'Worked on distributed systems'
                },
                {
                    'company': 'OpenAI',
                    'title': 'Senior Software Engineer',
                    'start_date': '2023-07',
                    'end_date': None,
                    'duration_months': 16,
                    'description': 'Working on LLM infrastructure'
                }
            ],
            'education': [
                {
                    'institution': 'Stanford University',
                    'degree': 'BS',
                    'field': 'Computer Science',
                    'start_year': 2016,
                    'end_year': 2020
                }
            ],
            'note': 'Mock data - implement Proxycurl or similar API for real data'
        }
