from flask import Blueprint, request, jsonify
from services.database import Database
from services.grok_client import GrokClient

search_bp = Blueprint('search', __name__, url_prefix='/api/search')

db = Database()
grok_client = GrokClient()


@search_bp.route('/candidates', methods=['GET'])
def search_candidates():
    """
    Search candidates with various filters.

    Query params:
    - q: General search query
    - tier: Priority tier (top, high, medium, low)
    - min_score: Minimum total score
    - company: Company name (current or past)
    - skill: Technical skill
    - limit: Results limit (default 50)
    - offset: Pagination offset (default 0)
    """
    try:
        query = request.args.get('q')
        tier = request.args.get('tier')
        min_score = request.args.get('min_score', type=float)
        company = request.args.get('company')
        limit = request.args.get('limit', 50, type=int)
        offset = request.args.get('offset', 0, type=int)

        # Use database search
        candidates = db.search_candidates(
            priority_tier=tier,
            min_score=min_score,
            company=company,
            limit=limit,
            offset=offset
        )

        # If general query provided, filter results
        if query and candidates:
            query_lower = query.lower()
            candidates = [
                c for c in candidates
                if query_lower in c.name.lower()
                or (c.current_company and query_lower in c.current_company.lower())
                or (c.current_title and query_lower in c.current_title.lower())
            ]

        return jsonify({
            'success': True,
            'count': len(candidates),
            'query': {
                'q': query,
                'tier': tier,
                'min_score': min_score,
                'company': company
            },
            'results': [c.dict() for c in candidates]
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@search_bp.route('/by-tier', methods=['GET'])
def search_by_tier():
    """Get candidates grouped by priority tier."""
    try:
        tiers = {
            'top': db.get_candidates_by_tier('top'),
            'high': db.get_candidates_by_tier('high'),
            'medium': db.get_candidates_by_tier('medium'),
            'low': db.get_candidates_by_tier('low')
        }

        return jsonify({
            'success': True,
            'tiers': {
                tier: {
                    'count': len(candidates),
                    'candidates': [c.dict() for c in candidates]
                }
                for tier, candidates in tiers.items()
            }
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@search_bp.route('/stats', methods=['GET'])
def get_search_stats():
    """Get overall statistics about candidates."""
    try:
        all_candidates = db.get_all_candidates()

        # Calculate statistics
        total_count = len(all_candidates)
        tier_counts = {
            'top': len([c for c in all_candidates if c.priority_tier == 'top']),
            'high': len([c for c in all_candidates if c.priority_tier == 'high']),
            'medium': len([c for c in all_candidates if c.priority_tier == 'medium']),
            'low': len([c for c in all_candidates if c.priority_tier == 'low'])
        }

        # Average score
        avg_score = sum(c.score.total_score for c in all_candidates) / total_count if total_count > 0 else 0

        # Top companies
        companies = {}
        for c in all_candidates:
            if c.current_company:
                companies[c.current_company] = companies.get(c.current_company, 0) + 1

        top_companies = sorted(companies.items(), key=lambda x: x[1], reverse=True)[:10]

        return jsonify({
            'success': True,
            'stats': {
                'total_candidates': total_count,
                'tier_distribution': tier_counts,
                'average_score': round(avg_score, 2),
                'top_companies': [{'company': name, 'count': count} for name, count in top_companies]
            }
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@search_bp.route('/suggestions', methods=['POST'])
def get_search_suggestions():
    """Use Grok to suggest search strategies."""
    try:
        data = request.json
        query = data.get('query', 'talented software engineers')

        # Use Grok to generate search suggestions
        suggestions = grok_client.search_x_for_engineers(query)

        return jsonify({
            'success': True,
            'query': query,
            'suggestions': suggestions
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
