from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Movie(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, unique=True, index=True)
    title = Column(String(500), index=True)
    genres = Column(String(500))
    recommendations = relationship("Recommendation", back_populates="movie")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    recommendations = relationship("Recommendation", back_populates="user")

class Recommendation(Base):
    __tablename__ = "recommendations"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), index=True)
    movie_id = Column(Integer, ForeignKey("movies.movie_id"), index=True)
    score = Column(Float)
    algorithm = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    user = relationship("User", back_populates="recommendations")
    movie = relationship("Movie", back_populates="recommendations")
    __table_args__ = (Index('idx_user_movie', 'user_id', 'movie_id'),)

class RecommendationHistory(Base):
    __tablename__ = "recommendation_history"
    id = Column(Integer, primary_key=True)
    query = Column(String(500))
    algorithm = Column(String(50))
    results_count = Column(Integer)
    generation_time_ms = Column(Float)
    cache_hit = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
