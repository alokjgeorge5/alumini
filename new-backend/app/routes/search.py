from flask import Blueprint, jsonify, request
from ..models import get_engine
from sqlalchemy import text

bp = Blueprint("search", __name__)


@bp.get("/")
def unified_search():
    query = request.args.get("query", "").strip()

    if not query or len(query) < 2:
        return jsonify({"error": "Search query must be at least 2 characters"}), 400

    engine = get_engine()
    try:
        with engine.connect() as conn:
            search_term = f"%{query}%"

            result = conn.execute(text("""
                SELECT 'student' as type, id, name as title, bio as description, major, cgpa
                FROM users
                WHERE role = 'student' AND (name LIKE :search_term OR major LIKE :search_term OR bio LIKE :search_term)

                UNION

                SELECT 'alumni' as type, id, name as title, bio as description, company, NULL
                FROM users
                WHERE role = 'alumni' AND (name LIKE :search_term OR company LIKE :search_term OR position LIKE :search_term OR bio LIKE :search_term)

                UNION

                SELECT 'opportunity' as type, id, title, description, company, NULL
                FROM opportunities
                WHERE is_active = TRUE AND (title LIKE :search_term OR company LIKE :search_term OR description LIKE :search_term OR requirements LIKE :search_term)

                UNION

                SELECT 'mentorship' as type, id, subject as title, message as description, NULL, NULL
                FROM mentorship_requests
                WHERE subject LIKE :search_term OR message LIKE :search_term

                UNION

                SELECT 'scholarship' as type, id, title, description, NULL, cgpa_requirement
                FROM scholarships
                WHERE status = 'active' AND (title LIKE :search_term OR description LIKE :search_term OR eligibility_criteria LIKE :search_term)

                LIMIT 50
            """), {"search_term": search_term})

            results = []
            for row in result:
                result_item = {
                    "type": row.type,
                    "id": row.id,
                    "title": row.title,
                    "description": row.description[:200] if row.description else None
                }

                if row.type == "student":
                    result_item["major"] = row.major
                    result_item["cgpa"] = float(row.cgpa) if row.cgpa else None
                elif row.type == "alumni":
                    result_item["company"] = row.company
                elif row.type == "opportunity":
                    result_item["company"] = row.company
                elif row.type == "scholarship":
                    result_item["cgpa_requirement"] = float(row.cgpa_requirement) if row.cgpa_requirement else None

                results.append(result_item)

            return jsonify({
                "query": query,
                "count": len(results),
                "results": results
            }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
