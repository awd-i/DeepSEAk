import os
import requests
from typing import Dict, List, Optional
from bs4 import BeautifulSoup
import re
from .grok_client import GrokClient


class XAnalyzer:
    """Analyzer for X/Twitter profiles and posts."""

    def __init__(self, bearer_token: Optional[str] = None, grok_client: Optional[GrokClient] = None):
        self.bearer_token = bearer_token or os.getenv('TWITTER_BEARER_TOKEN')
        self.grok = grok_client or GrokClient()

    def search_high_engagement_posts(self, query: str, min_likes: int = 100, min_retweets: int = 20) -> List[Dict]:
        """
        Search for high-engagement posts on X/Twitter.

        Note: This is a placeholder. In production, you would either:
        1. Use Twitter API v2 with elevated access
        2. Use a third-party service like Apify, ScraperAPI, etc.
        3. Implement custom scraping (subject to ToS)

        Args:
            query: Search query (e.g., "software engineer" "ML researcher")
            min_likes: Minimum likes threshold
            min_retweets: Minimum retweets threshold

        Returns:
            List of high-engagement posts with metadata
        """
        if not self.bearer_token:
            print("Warning: No Twitter bearer token provided. Using mock data.")
            return self._get_mock_posts()

        # Twitter API v2 endpoint
        url = "https://api.twitter.com/2/tweets/search/recent"
        headers = {
            "Authorization": f"Bearer {self.bearer_token}"
        }
        params = {
            "query": query,
            "max_results": 100,
            "tweet.fields": "public_metrics,created_at,author_id",
            "user.fields": "username,name,description,public_metrics",
            "expansions": "author_id"
        }

        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()

            # Filter by engagement
            high_engagement_posts = []
            for tweet in data.get('data', []):
                metrics = tweet.get('public_metrics', {})
                if metrics.get('like_count', 0) >= min_likes or metrics.get('retweet_count', 0) >= min_retweets:
                    high_engagement_posts.append({
                        'id': tweet['id'],
                        'text': tweet['text'],
                        'author_id': tweet['author_id'],
                        'created_at': tweet['created_at'],
                        'likes': metrics.get('like_count', 0),
                        'retweets': metrics.get('retweet_count', 0),
                        'replies': metrics.get('reply_count', 0),
                        'quotes': metrics.get('quote_count', 0)
                    })

            # Add user information
            users = {user['id']: user for user in data.get('includes', {}).get('users', [])}
            for post in high_engagement_posts:
                user = users.get(post['author_id'], {})
                post['username'] = user.get('username')
                post['name'] = user.get('name')
                post['bio'] = user.get('description')
                post['follower_count'] = user.get('public_metrics', {}).get('followers_count', 0)

            return high_engagement_posts

        except requests.exceptions.RequestException as e:
            print(f"Error fetching tweets: {e}")
            return self._get_mock_posts()

    def analyze_post_for_candidates(self, post: Dict) -> Optional[Dict]:
        """
        Analyze a post to determine if author is a potential candidate.

        Args:
            post: Post dictionary with text and metadata

        Returns:
            Candidate analysis or None if not a good fit
        """
        # Use Grok to analyze the post
        analysis = self.grok.analyze_x_post(post['text'], post)

        # Extract GitHub username if mentioned
        github_username = self._extract_github_username(post.get('text', ''))
        if github_username:
            analysis['github_username'] = github_username

        # Calculate engagement score
        engagement_score = self._calculate_engagement_score(post)
        analysis['engagement_score'] = engagement_score

        return analysis

    def get_user_profile(self, username: str) -> Optional[Dict]:
        """
        Get detailed profile information for a Twitter/X user.

        Args:
            username: Twitter/X username (without @)

        Returns:
            User profile dictionary
        """
        if not self.bearer_token:
            print("Warning: No Twitter bearer token provided.")
            return None

        url = f"https://api.twitter.com/2/users/by/username/{username}"
        headers = {
            "Authorization": f"Bearer {self.bearer_token}"
        }
        params = {
            "user.fields": "description,created_at,public_metrics,url,location,verified"
        }

        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()

            user = data.get('data', {})
            return {
                'id': user.get('id'),
                'username': user.get('username'),
                'name': user.get('name'),
                'bio': user.get('description'),
                'location': user.get('location'),
                'url': user.get('url'),
                'verified': user.get('verified'),
                'created_at': user.get('created_at'),
                'followers': user.get('public_metrics', {}).get('followers_count', 0),
                'following': user.get('public_metrics', {}).get('following_count', 0),
                'tweet_count': user.get('public_metrics', {}).get('tweet_count', 0)
            }

        except requests.exceptions.RequestException as e:
            print(f"Error fetching user profile: {e}")
            return None

    def _extract_github_username(self, text: str) -> Optional[str]:
        """Extract GitHub username from text."""
        # Look for github.com/username patterns
        github_pattern = r'github\.com/([a-zA-Z0-9-]+)'
        match = re.search(github_pattern, text)
        if match:
            return match.group(1)
        return None

    def _calculate_engagement_score(self, post: Dict) -> float:
        """
        Calculate engagement score based on post metrics.

        Args:
            post: Post dictionary with engagement metrics

        Returns:
            Normalized engagement score (0-100)
        """
        likes = post.get('likes', 0)
        retweets = post.get('retweets', 0)
        replies = post.get('replies', 0)
        quotes = post.get('quotes', 0)
        follower_count = post.get('follower_count', 1)

        # Weighted engagement calculation
        raw_engagement = (
            likes * 1.0 +
            retweets * 2.0 +
            replies * 1.5 +
            quotes * 2.5
        )

        # Normalize by follower count (engagement rate)
        engagement_rate = (raw_engagement / max(follower_count, 1)) * 100

        # Cap at 100
        return min(engagement_rate, 100)

    def _get_mock_posts(self) -> List[Dict]:
        """Return mock high-engagement posts for testing."""
        return [
            {
                'id': '1',
                'text': 'Just shipped a new ML model at @OpenAI. Reduced latency by 40% using custom CUDA kernels. Check out the research: github.com/example/ml-project',
                'author_id': 'user1',
                'username': 'ml_engineer_1',
                'name': 'Alice Chen',
                'bio': 'ML Engineer @OpenAI | PhD MIT | Previously Google Brain',
                'likes': 2500,
                'retweets': 450,
                'replies': 120,
                'quotes': 80,
                'follower_count': 15000,
                'created_at': '2025-11-15T10:00:00Z'
            },
            {
                'id': '2',
                'text': 'Excited to share our latest paper on multi-modal transformers! 3 years at @DeepMind working on this. Stanford CS alum.',
                'author_id': 'user2',
                'username': 'researcher_bob',
                'name': 'Bob Kumar',
                'bio': 'Research Scientist @DeepMind | Stanford CS PhD',
                'likes': 1800,
                'retweets': 320,
                'replies': 95,
                'quotes': 60,
                'follower_count': 12000,
                'created_at': '2025-11-14T14:30:00Z'
            }
        ]
