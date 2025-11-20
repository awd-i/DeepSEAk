from flask import Blueprint, request, jsonify
from services.database import Database
from services.x_analyzer import XAnalyzer
from services.github_analyzer import GitHubAnalyzer
from services.linkedin_scraper import LinkedInScraper
from services.scoring_service import ScoringService
from services.grok_client import GrokClient
from services.profile_enrichment import ProfileEnrichment
from models.candidate import Candidate, Experience, Education, GitHubStats, SocialProfile
from typing import Dict

candidates_bp = Blueprint('candidates', __name__, url_prefix='/api/candidates')

# Initialize services
db = Database()
x_analyzer = XAnalyzer()
github_analyzer = GitHubAnalyzer()
linkedin_scraper = LinkedInScraper()
scoring_service = ScoringService()
grok_client = GrokClient()
profile_enrichment = ProfileEnrichment()


@candidates_bp.route('/', methods=['GET'])
def get_all_candidates():
    """Get all candidates with optional filtering."""
    try:
        priority_tier = request.args.get('tier')
        min_score = request.args.get('min_score', type=float)
        company = request.args.get('company')
        limit = request.args.get('limit', 50, type=int)
        offset = request.args.get('offset', 0, type=int)

        candidates = db.search_candidates(
            priority_tier=priority_tier,
            min_score=min_score,
            company=company,
            limit=limit,
            offset=offset
        )

        return jsonify({
            'success': True,
            'count': len(candidates),
            'candidates': [c.dict() for c in candidates]
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@candidates_bp.route('/<candidate_id>', methods=['GET'])
def get_candidate(candidate_id):
    """Get a specific candidate by ID."""
    try:
        candidate = db.get_candidate(candidate_id)

        if not candidate:
            return jsonify({'success': False, 'error': 'Candidate not found'}), 404

        return jsonify({
            'success': True,
            'candidate': candidate.dict()
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@candidates_bp.route('/', methods=['POST'])
def create_candidate():
    """Create a new candidate from provided data."""
    try:
        data = request.json

        # Create candidate object
        candidate = Candidate(
            name=data.get('name', 'Unknown'),
            email=data.get('email'),
            current_title=data.get('current_title'),
            current_company=data.get('current_company'),
            linkedin_url=data.get('linkedin_url'),
            discovered_from=data.get('discovered_from', 'manual')
        )

        # Score the candidate
        candidate.score = scoring_service.score_candidate(candidate)
        candidate.priority_tier = scoring_service.determine_priority_tier(candidate.score)

        # Save to database
        candidate_id = db.add_candidate(candidate)

        if not candidate_id:
            return jsonify({'success': False, 'error': 'Failed to create candidate'}), 500

        return jsonify({
            'success': True,
            'candidate_id': candidate_id,
            'message': 'Candidate created successfully'
        }), 201

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@candidates_bp.route('/<candidate_id>', methods=['PUT'])
def update_candidate(candidate_id):
    """Update a candidate's information."""
    try:
        data = request.json

        # Update candidate
        success = db.update_candidate(candidate_id, data)

        if not success:
            return jsonify({'success': False, 'error': 'Failed to update candidate'}), 500

        return jsonify({
            'success': True,
            'message': 'Candidate updated successfully'
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@candidates_bp.route('/<candidate_id>', methods=['DELETE'])
def delete_candidate(candidate_id):
    """Delete a candidate."""
    try:
        success = db.delete_candidate(candidate_id)

        if not success:
            return jsonify({'success': False, 'error': 'Failed to delete candidate'}), 500

        return jsonify({
            'success': True,
            'message': 'Candidate deleted successfully'
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@candidates_bp.route('/top', methods=['GET'])
def get_top_candidates():
    """Get top-ranked candidates."""
    try:
        limit = request.args.get('limit', 20, type=int)
        candidates = db.get_top_candidates(limit=limit)

        return jsonify({
            'success': True,
            'count': len(candidates),
            'candidates': [c.dict() for c in candidates]
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@candidates_bp.route('/discover/x', methods=['POST'])
def discover_from_x():
    """Discover candidates from X/Twitter posts."""
    try:
        data = request.json
        query = data.get('query', 'software engineer')
        min_likes = data.get('min_likes', 100)
        min_retweets = data.get('min_retweets', 20)

        # Search for high-engagement posts
        posts = x_analyzer.search_high_engagement_posts(query, min_likes, min_retweets)

        discovered_candidates = []

        for post in posts:
            # Analyze post for candidate potential
            analysis = x_analyzer.analyze_post_for_candidates(post)

            if analysis.get('is_engineer') in ['yes', 'maybe']:
                # Get user profile
                user_profile = x_analyzer.get_user_profile(post.get('username'))

                if user_profile:
                    # Create candidate
                    candidate = _create_candidate_from_x_post(post, user_profile, analysis)

                    # Save to database
                    candidate_id = db.add_candidate(candidate)

                    if candidate_id:
                        discovered_candidates.append({
                            'id': candidate_id,
                            'name': candidate.name,
                            'score': candidate.score.total_score,
                            'tier': candidate.priority_tier
                        })

        return jsonify({
            'success': True,
            'discovered_count': len(discovered_candidates),
            'candidates': discovered_candidates
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@candidates_bp.route('/discover/github', methods=['POST'])
def discover_from_github():
    """Discover candidates from GitHub."""
    try:
        data = request.json
        query = data.get('query', 'machine learning')
        min_followers = data.get('min_followers', 100)

        # Search for GitHub users
        users = github_analyzer.search_users(query, min_followers)

        discovered_candidates = []

        for user in users[:20]:  # Limit to 20 to avoid rate limits
            # Get detailed stats
            stats = github_analyzer.calculate_github_stats(user['username'])

            if stats.get('total_stars', 0) > 50:  # Filter for quality
                # Create candidate
                candidate = _create_candidate_from_github(user, stats)

                # Save to database
                candidate_id = db.add_candidate(candidate)

                if candidate_id:
                    discovered_candidates.append({
                        'id': candidate_id,
                        'name': candidate.name,
                        'score': candidate.score.total_score,
                        'tier': candidate.priority_tier
                    })

        return jsonify({
            'success': True,
            'discovered_count': len(discovered_candidates),
            'candidates': discovered_candidates
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


def _create_candidate_from_x_post(post: Dict, user_profile: Dict, analysis: Dict) -> Candidate:
    """Helper function to create a Candidate from X/Twitter data with profile enrichment."""

    # Use profile enrichment to get complete profile
    x_username = post.get('username', '')
    enriched_profile = profile_enrichment.enrich_from_x(x_username)

    candidate = Candidate(
        name=enriched_profile.get('name', post.get('name', 'Unknown')),
        email=enriched_profile.get('email'),
        current_title=enriched_profile.get('current_title'),
        current_company=enriched_profile.get('current_company'),
        linkedin_url=enriched_profile.get('linkedin_url'),
        discovered_from='x_post'
    )

    # Add X profile
    candidate.x_profile = SocialProfile(
        platform='X/Twitter',
        username=x_username,
        url=f"https://x.com/{x_username}",
        followers=user_profile.get('followers', 0),
        engagement_score=analysis.get('engagement_score', 0)
    )

    # Add GitHub profile if found
    if enriched_profile.get('github_profile'):
        candidate.github_profile = GitHubStats(**enriched_profile['github_profile'])

    # Score the candidate
    candidate.score = scoring_service.score_candidate(candidate)
    candidate.priority_tier = scoring_service.determine_priority_tier(candidate.score)

    return candidate


def _create_candidate_from_github(user: Dict, stats: Dict) -> Candidate:
    """Helper function to create a Candidate from GitHub data with profile enrichment."""

    # Use profile enrichment to get complete profile
    enriched_profile = profile_enrichment.enrich_from_github(user['username'])

    candidate = Candidate(
        name=enriched_profile.get('name', stats.get('username', 'Unknown')),
        email=enriched_profile.get('email'),
        current_title=enriched_profile.get('current_title'),
        current_company=enriched_profile.get('current_company'),
        linkedin_url=enriched_profile.get('linkedin_url'),
        discovered_from='github_search'
    )

    # Add GitHub profile
    candidate.github_profile = GitHubStats(**stats)

    # Add X profile if found
    if enriched_profile.get('x_profile'):
        x_data = enriched_profile['x_profile']
        candidate.x_profile = SocialProfile(
            platform='X/Twitter',
            username=x_data.get('username', ''),
            url=x_data.get('url', ''),
            followers=x_data.get('followers', 0)
        )

    # Score the candidate
    candidate.score = scoring_service.score_candidate(candidate)
    candidate.priority_tier = scoring_service.determine_priority_tier(candidate.score)

    return candidate
