from sqlalchemy import Column, ForeignKey, Integer, String, engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.sql.expression import null
from sqlalchemy.sql.sqltypes import Boolean, Float, TIMESTAMP

# engine = create_engine("sqlite:///data/test.db")

Base = declarative_base()


class Species(Base):
    __tablename__ = "Species"
    SpIndex = Column(Integer, primary_key=True)
    SpCode = Column(String(10), nullable=False)
    CommonName = Column(String(100), nullable=False)
    SciName = Column(String(100), nullable=False)


class Hotstpot(Base):
    __tablename__ = "Hotspots"
    LocId = Column(String(10), primary_key=True)
    Name = Column(String(100), nullable=False)
    Timestamp = Column(Float, nullable=False)


class Period(Base):
    __tablename__ = "Periods"
    PeriodId = Column(Integer, primary_key=True)
    Description = Column(String(32), nullable=False)


class User(Base):
    __tablename__ = "Users"
    UserId = Column(Integer, primary_key=True)
    Email = Column(String(100), nullable=False)
    LoginCount = Column(Integer)


class Observation(Base):
    __tablename__ = "Observations"
    LocId = Column(String(10), ForeignKey(Hotstpot.LocId), primary_key=True)
    PeriodId = Column(Integer, ForeignKey(Period.PeriodId), primary_key=True)
    SpIndex = Column(Integer, ForeignKey(Species.SpIndex), primary_key=True)
    Obs = Column(Float, nullable=False)


class Analysis(Base):
    __tablename__ = "Analyses"
    UserId = Column(Integer, ForeignKey(User.UserId), primary_key=True)
    AnalysisId = Column(Integer, nullable=False, primary_key=True)
    AnalysisName = Column(String(100))
    PeriodId = Column(Integer, ForeignKey(Period.PeriodId))


class HotspotConfig(Base):
    __tablename__ = "HotspotConfigs"
    UserId = Column(Integer, ForeignKey(User.UserId), primary_key=True)
    AnalysisId = Column(Integer, ForeignKey(Analysis.AnalysisId), primary_key=True)
    LocId = Column(String(10), ForeignKey(Hotstpot.LocId))
    IsActive = Column(Integer, nullable=False)


class SeenBird(Base):
    __tablename__ = "SeenBirds"
    UserId = Column(Integer, ForeignKey(User.UserId), primary_key=True)
    AnalysisId = Column(Integer, ForeignKey(Analysis.AnalysisId), primary_key=True)
    SpIndex = Column(Integer, ForeignKey(Species.SpIndex))


# Base.metadata.create_all(engine)
# Base.metadata.bind = engine
