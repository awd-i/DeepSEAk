import os
import requests
from typing import Dict, List, Optional
from datetime import datetime, timedelta


class GitHubAnalyzer:
    """Analyzer for GitHub profiles and repositories."""

    def __init__(self, token: Optional[str] = None):
        self.token = token or os.getenv('GITHUB_TOKEN')
        self.headers = {
            'Accept': 'application/vnd.github.v3+json'
        }
        if self.token:
            self.headers['Authorization'] = f'token {self.token}'

    def get_user_profile(self, username: str) -> Optional[Dict]:
        """
        Get detailed GitHub user profile.

        Args:
            username: GitHub username

        Returns:
            User profile dictionary
        """
        url = f"https://api.github.com/users/{username}"

        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()

            return {
                'username': data.get('login'),
                'name': data.get('name'),
                'email': data.get('email'),
                'bio': data.get('bio'),
                'company': data.get('company'),
                'location': data.get('location'),
                'blog': data.get('blog'),
                'twitter_username': data.get('twitter_username'),
                'public_repos': data.get('public_repos', 0),
                'followers': data.get('followers', 0),
                'following': data.get('following', 0),
                'created_at': data.get('created_at'),
                'url': data.get('html_url')
            }

        except requests.exceptions.RequestException as e:
            print(f"Error fetching GitHub profile: {e}")
            return None

    def get_user_repositories(self, username: str, max_repos: int = 100) -> List[Dict]:
        """
        Get user's public repositories sorted by stars.

        Args:
            username: GitHub username
            max_repos: Maximum number of repos to fetch

        Returns:
            List of repository dictionaries
        """
        url = f"https://api.github.com/users/{username}/repos"
        params = {
            'sort': 'updated',
            'per_page': min(max_repos, 100)
        }

        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            repos = response.json()

            # Sort by stars
            repos.sort(key=lambda r: r.get('stargazers_count', 0), reverse=True)

            return [
                {
                    'name': repo.get('name'),
                    'description': repo.get('description'),
                    'url': repo.get('html_url'),
                    'stars': repo.get('stargazers_count', 0),
                    'forks': repo.get('forks_count', 0),
                    'language': repo.get('language'),
                    'created_at': repo.get('created_at'),
                    'updated_at': repo.get('updated_at'),
                    'topics': repo.get('topics', [])
                }
                for repo in repos
            ]

        except requests.exceptions.RequestException as e:
            print(f"Error fetching repositories: {e}")
            return []

    def calculate_github_stats(self, username: str) -> Dict:
        """
        Calculate comprehensive GitHub statistics for a user.

        Args:
            username: GitHub username

        Returns:
            Dictionary with calculated statistics
        """
        profile = self.get_user_profile(username)
        if not profile:
            return {}

        repos = self.get_user_repositories(username)

        # Calculate statistics
        total_stars = sum(repo['stars'] for repo in repos)
        total_forks = sum(repo['forks'] for repo in repos)
        languages = {}
        for repo in repos:
            lang = repo.get('language')
            if lang:
                languages[lang] = languages.get(lang, 0) + 1

        # Get top languages
        top_languages = sorted(languages.items(), key=lambda x: x[1], reverse=True)[:5]
        top_languages = [lang for lang, _ in top_languages]

        # Get notable projects (repos with >50 stars)
        notable_projects = [
            {
                'name': repo['name'],
                'stars': repo['stars'],
                'description': repo['description'],
                'url': repo['url']
            }
            for repo in repos if repo['stars'] >= 50
        ]

        # Get contribution activity (simplified - would need GraphQL for accurate data)
        contributions_last_year = self._estimate_contributions(username)

        return {
            'username': username,
            'url': profile['url'],
            'followers': profile['followers'],
            'public_repos': profile['public_repos'],
            'total_stars': total_stars,
            'total_forks': total_forks,
            'contributions_last_year': contributions_last_year,
            'top_languages': top_languages,
            'notable_projects': notable_projects,
            'account_age_days': self._calculate_account_age(profile['created_at'])
        }

    def search_users(self, query: str, min_followers: int = 100, max_results: int = 30) -> List[Dict]:
        """
        Search for GitHub users based on query.

        Args:
            query: Search query (e.g., "machine learning followers:>100")
            min_followers: Minimum followers threshold
            max_results: Maximum results to return

        Returns:
            List of user dictionaries
        """
        url = "https://api.github.com/search/users"
        params = {
            'q': f"{query} followers:>={min_followers}",
            'sort': 'followers',
            'order': 'desc',
            'per_page': min(max_results, 100)
        }

        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()

            return [
                {
                    'username': user['login'],
                    'url': user['html_url'],
                    'avatar': user['avatar_url']
                }
                for user in data.get('items', [])
            ]

        except requests.exceptions.RequestException as e:
            print(f"Error searching users: {e}")
            return []

    def get_trending_developers(self, language: Optional[str] = None) -> List[str]:
        """
        Get trending developers (uses GitHub's trending repositories as proxy).

        Args:
            language: Optional programming language filter

        Returns:
            List of developer usernames
        """
        # Note: GitHub doesn't have an official trending API
        # This is a simplified version using search
        query = "stars:>100 pushed:>2025-11-01"
        if language:
            query += f" language:{language}"

        url = "https://api.github.com/search/repositories"
        params = {
            'q': query,
            'sort': 'stars',
            'order': 'desc',
            'per_page': 30
        }

        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()

            # Extract unique owners
            developers = set()
            for repo in data.get('items', []):
                owner = repo.get('owner', {}).get('login')
                if owner:
                    developers.add(owner)

            return list(developers)[:20]

        except requests.exceptions.RequestException as e:
            print(f"Error fetching trending developers: {e}")
            return []

    def _estimate_contributions(self, username: str) -> int:
        """
        Estimate contributions in the last year.
        Note: This is approximate. For accurate data, use GitHub GraphQL API.

        Args:
            username: GitHub username

        Returns:
            Estimated contribution count
        """
        # Simplified: Use recent commits as proxy
        # In production, use GraphQL API for accurate contribution data
        url = f"https://api.github.com/users/{username}/events/public"

        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            events = response.json()

            # Count push events in last year
            one_year_ago = datetime.now() - timedelta(days=365)
            recent_events = [
                e for e in events
                if datetime.fromisoformat(e['created_at'].replace('Z', '+00:00')) > one_year_ago
            ]

            # Rough estimate based on event types
            contribution_count = 0
            for event in recent_events:
                if event['type'] == 'PushEvent':
                    contribution_count += len(event.get('payload', {}).get('commits', []))
                elif event['type'] in ['PullRequestEvent', 'IssuesEvent']:
                    contribution_count += 1

            return contribution_count

        except requests.exceptions.RequestException as e:
            print(f"Error estimating contributions: {e}")
            return 0

    def _calculate_account_age(self, created_at: str) -> int:
        """Calculate account age in days."""
        try:
            created_date = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            age = datetime.now(created_date.tzinfo) - created_date
            return age.days
        except (ValueError, AttributeError):
            return 0

    def calculate_github_score(self, stats: Dict) -> float:
        """
        Calculate a score for GitHub activity (0-100).

        Args:
            stats: GitHub statistics dictionary

        Returns:
            Normalized score (0-100)
        """
        score = 0.0

        # Followers score (max 20 points)
        followers = stats.get('followers', 0)
        score += min((followers / 500) * 20, 20)

        # Stars score (max 30 points)
        total_stars = stats.get('total_stars', 0)
        score += min((total_stars / 1000) * 30, 30)

        # Contributions score (max 25 points)
        contributions = stats.get('contributions_last_year', 0)
        score += min((contributions / 500) * 25, 25)

        # Notable projects score (max 15 points)
        notable_count = len(stats.get('notable_projects', []))
        score += min(notable_count * 3, 15)

        # Account age score (max 10 points)
        account_age = stats.get('account_age_days', 0)
        score += min((account_age / 1825) * 10, 10)  # 5 years = max

        return min(score, 100)
