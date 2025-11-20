import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration."""

    # Grok API
    XAI_API_KEY = os.getenv('XAI_API_KEY')
    GROK_API_BASE = 'https://api.x.ai/v1'

    # Supabase
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY')

    # Twitter/X API
    TWITTER_BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')

    # GitHub API
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')

    # Scoring weights for candidate evaluation
    SCORING_WEIGHTS = {
        'faang_experience': 30,
        'frontier_labs_experience': 35,
        'top_tech_companies': 25,
        'github_activity': 15,
        'x_engagement': 10,
        'research_publications': 20,
        'education_tier': 15,
        'years_experience': 10,
        'open_source_contributions': 12,
        'leadership_roles': 8
    }

    # Company categories
    FAANG_COMPANIES = ['Facebook', 'Meta', 'Apple', 'Amazon', 'Netflix', 'Google', 'Microsoft']
    FRONTIER_LABS = ['OpenAI', 'Anthropic', 'DeepMind', 'Google DeepMind', 'Cohere', 'Stability AI',
                     'Midjourney', 'Character.AI', 'Inflection AI', 'xAI', 'Adept']
    TOP_TECH_COMPANIES = ['Tesla', 'SpaceX', 'Stripe', 'Databricks', 'Airbnb', 'Uber', 'Lyft',
                         'Snap', 'Twitter', 'X', 'Pinterest', 'Reddit', 'Dropbox', 'Square',
                         'Block', 'Salesforce', 'Oracle', 'Adobe', 'NVIDIA', 'Intel', 'AMD']

    # Top universities
    TOP_UNIVERSITIES = ['MIT', 'Stanford', 'Harvard', 'Carnegie Mellon', 'UC Berkeley',
                       'Caltech', 'Princeton', 'Yale', 'Columbia', 'Cornell', 'University of Washington',
                       'Georgia Tech', 'University of Michigan', 'UT Austin', 'UIUC',
                       'University of Illinois Urbana-Champaign', 'Cambridge', 'Oxford',
                       'ETH Zurich', 'Tsinghua', 'Peking University', 'IIT']
