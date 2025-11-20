import os
import requests
from typing import Dict, List, Optional
import json


class GrokClient:
    """Client for interacting with Grok API (xAI)."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('XAI_API_KEY')
        self.base_url = 'https://api.x.ai/v1'
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

    def chat_completion(self, messages: List[Dict], model: str = "grok-beta", temperature: float = 0.7) -> Dict:
        """
        Send a chat completion request to Grok.

        Args:
            messages: List of message dictionaries with 'role' and 'content'
            model: Model to use (default: grok-beta)
            temperature: Sampling temperature (0-1)

        Returns:
            Response dictionary from Grok API
        """
        url = f"{self.base_url}/chat/completions"
        payload = {
            "messages": messages,
            "model": model,
            "temperature": temperature,
            "stream": False
        }

        try:
            response = requests.post(url, headers=self.headers, json=payload, timeout=60)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error calling Grok API: {e}")
            return {"error": str(e)}

    def analyze_x_post(self, post_content: str, post_metadata: Dict) -> Dict:
        """
        Use Grok to analyze an X/Twitter post and extract candidate information.

        Args:
            post_content: The text content of the post
            post_metadata: Additional metadata (likes, retweets, etc.)

        Returns:
            Analysis results including candidate potential and keywords
        """
        messages = [
            {
                "role": "system",
                "content": "You are an expert technical recruiter. Analyze social media posts to identify potential engineering candidates. Look for: technical skills, company affiliations, educational background, projects, and indicators of high-caliber engineering talent."
            },
            {
                "role": "user",
                "content": f"""Analyze this X/Twitter post for potential engineering talent:

Post: {post_content}

Engagement: {post_metadata.get('likes', 0)} likes, {post_metadata.get('retweets', 0)} retweets, {post_metadata.get('replies', 0)} replies

Extract:
1. Is this likely from an engineer? (yes/no/maybe)
2. Technical skills or domains mentioned
3. Company or affiliation mentioned
4. Educational background mentioned
5. GitHub profile or projects mentioned
6. Overall talent score (0-100)
7. Key search terms for finding their other profiles

Return as JSON."""
            }
        ]

        response = self.chat_completion(messages, temperature=0.3)

        if 'error' not in response:
            try:
                content = response['choices'][0]['message']['content']
                # Try to parse JSON from response
                return json.loads(content)
            except (json.JSONDecodeError, KeyError, IndexError):
                return {"raw_response": response}
        return response

    def extract_candidate_info(self, profile_data: Dict) -> Dict:
        """
        Use Grok to extract and structure candidate information from various sources.

        Args:
            profile_data: Combined data from X, GitHub, LinkedIn, etc.

        Returns:
            Structured candidate information
        """
        messages = [
            {
                "role": "system",
                "content": "You are an expert at extracting and structuring professional information. Parse raw profile data and extract: name, email, current role, companies worked at, education, technical skills, and research."
            },
            {
                "role": "user",
                "content": f"""Extract structured information from this candidate profile data:

{json.dumps(profile_data, indent=2)}

Return JSON with fields:
- name
- email (if found)
- current_title
- current_company
- companies (list of previous companies)
- education (list with institution, degree, field)
- skills (list of technical skills)
- github_username
- linkedin_url
- notable_achievements"""
            }
        ]

        response = self.chat_completion(messages, temperature=0.1)

        if 'error' not in response:
            try:
                content = response['choices'][0]['message']['content']
                return json.loads(content)
            except (json.JSONDecodeError, KeyError, IndexError):
                return {"raw_response": response}
        return response

    def search_x_for_engineers(self, search_query: str, min_engagement: int = 100) -> Dict:
        """
        Use Grok to suggest X/Twitter search strategies for finding engineers.

        Args:
            search_query: Base search query
            min_engagement: Minimum engagement threshold

        Returns:
            Search suggestions and strategies
        """
        messages = [
            {
                "role": "system",
                "content": "You are an expert at finding talented engineers on X/Twitter. Suggest effective search queries and patterns."
            },
            {
                "role": "user",
                "content": f"""Suggest effective X/Twitter search strategies to find:

{search_query}

Minimum engagement: {min_engagement} interactions

Provide:
1. 5 specific search queries to use
2. Keywords that indicate high-caliber engineers
3. Red flags to watch for
4. Engagement patterns that suggest real talent vs. spam

Return as JSON."""
            }
        ]

        response = self.chat_completion(messages, temperature=0.5)

        if 'error' not in response:
            try:
                content = response['choices'][0]['message']['content']
                return json.loads(content)
            except (json.JSONDecodeError, KeyError, IndexError):
                return {"raw_response": response}
        return response
