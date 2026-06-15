from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
import time
from src.data.data_loader import DataLoader
from src.recommenders.content_based import ContentBasedRecommender
from src.recommenders.popularity import PopularityRecommender
from src.recommenders.hybrid import HybridRecommender
from src.cache.redis_cache import cache
from src.database.db import get_db
from src.database.models import RecommendationHistory
from src.utils.logger import logger

router = APIRouter(prefix="/api", tags=["recommendations"])

# Load and initialize models
try:
    loader = DataLoader("data/raw")
    movies = loader.load_movies()
    ratings = loader.load_ratings()
    
    content = ContentBasedRecommender()
    content.fit(movies)
    logger.info("✓ Content-based fitted")
    
    pop = PopularityRecommender()
    pop.fit(ratings)
    logger.info("✓ Popularity fitted")
    
    hybrid = HybridRecommender(content, pop, movies)
    logger.info("✓ Hybrid initialized")

except Exception as e:
    logger.error(f"Error initializing models: {e}")
    raise

@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "models": {
            "content_based": "loaded",
            "popularity": "loaded",
            "hybrid": "loaded"
        },
        "data": {
            "movies": len(movies),
            "ratings": len(ratings),
            "users": len(set(ratings['userId'])) if len(ratings) > 0 else 0
        }
    }

@router.get("/recommend/movie/{movie_name}")
def recommend_by_movie(
    movie_name: str,
    top_n: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    start_time = time.time()
    
    # Check cache first
    cache_key = f"movie:{movie_name}:{top_n}"
    cached_result = cache.get(cache_key)
    
    if cached_result:
        logger.info(f"Cache hit: {cache_key}")
        history = RecommendationHistory(
            query=f"movie:{movie_name}",
            algorithm="hybrid",
            results_count=len(cached_result),
            generation_time_ms=1,
            cache_hit=1
        )
        db.add(history)
        db.commit()
        return {
            "query": movie_name,
            "method": "hybrid",
            "count": len(cached_result),
            "recommendations": cached_result,
            "cached": True
        }
    
    try:
        # Generate recommendations
        result = hybrid.recommend(movie_name, top_n=top_n)
        
        if len(result) == 0:
            raise HTTPException(status_code=404, detail=f"Movie '{movie_name}' not found")
        
        recommendations = result.to_dict('records')
        
        # Cache the result (24 hour TTL)
        cache.set(cache_key, recommendations, ttl=86400)
        
        # Save to database
        generation_time = (time.time() - start_time) * 1000
        history = RecommendationHistory(
            query=f"movie:{movie_name}",
            algorithm="hybrid",
            results_count=len(recommendations),
            generation_time_ms=generation_time,
            cache_hit=0
        )
        db.add(history)
        db.commit()
        
        logger.info(f"Generated {len(recommendations)} recommendations for '{movie_name}' in {generation_time:.2f}ms")
        
        return {
            "query": movie_name,
            "method": "hybrid",
            "count": len(recommendations),
            "recommendations": recommendations,
            "cached": False
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/cache/clear")
def clear_cache():
    cache.clear()
    return {"status": "cache cleared"}

@router.get("/analytics")
def analytics(db: Session = Depends(get_db)):
    from sqlalchemy import func
    
    total_queries = db.query(func.count(RecommendationHistory.id)).scalar() or 0
    cache_hits = db.query(func.count(RecommendationHistory.id)).filter(RecommendationHistory.cache_hit == 1).scalar() or 0
    avg_time = db.query(func.avg(RecommendationHistory.generation_time_ms)).scalar() or 0
    
    return {
        "total_queries": total_queries,
        "cache_hits": cache_hits,
        "cache_hit_rate": (cache_hits / total_queries * 100) if total_queries > 0 else 0,
        "avg_generation_time_ms": float(avg_time) if avg_time else 0,
        "cache_type": "Redis" if cache.client else "In-Memory"
    }
