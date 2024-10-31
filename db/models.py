# Placeholder content for db/models.pyfrom sqlalchemy import Column, String, Integer, Float, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./database.db"  # or PostgreSQL for production

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Vulnerability(Base):
    __tablename__ = "vulnerabilities"
    id = Column(Integer, primary_key=True, index=True)
    cve_id = Column(String, unique=True, index=True)
    description = Column(String)
    cvss_score = Column(Float)
    exploitability = Column(Float)
    reachability = Column(Boolean)
    priority_score = Column(Float)
    remediation = Column(String, nullable=True)

class UserSettings(Base):
    __tablename__ = "user_settings"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=True)
    cvss_weight = Column(Float, default=1.0)
    exploitability_weight = Column(Float, default=1.0)
    reachability_weight = Column(Float, default=1.0)
