from sqlalchemy import Column, ForeignKey, Integer, String, engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.sql.expression import null
from sqlalchemy.sql.sqltypes import Boolean, Float, TIMESTAMP

# engine = create_engine("sqlite:///data/test.db")

Base = declarative_base()

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()


class Species(Base):
    __tablename__ = "Species"
    SpIndex = Column(Integer, primary_key=True)
    SpCode = Column(String(10), nullable=False)
    CommonName = Column(String(100), nullable=False)
    SciName = Column(String(100), nullable=False)

    def __repr__(self) -> str:
        return f"Species(Index = {self.SpIndex}, Name = {self.CommonName})"


class Hotspot(Base):
    __tablename__ = "Hotspots"
    LocId = Column(String(10), primary_key=True)
    Name = Column(String(100), nullable=False)
    Timestamp = Column(Float, nullable=False)

    def __repr__(self) -> str:
        return f"Hotspot(LocId = {self.LocId}, Name = {self.Name})"


class Period(Base):
    __tablename__ = "Periods"
    PeriodId = Column(Integer, primary_key=True)
    Description = Column(String(32), nullable=False)

    def __repr__(self) -> str:
        return f"Period(Id = {self.PeriodId}, Description = {self.Description})"


class User(Base):
    __tablename__ = "Users"
    UserId = Column(String(40), primary_key=True)
    Email = Column(String(100), nullable=False)
    LoginCount = Column(Integer)


class Observation(Base):
    __tablename__ = "Observations"
    LocId = Column(String(10), ForeignKey(Hotspot.LocId), primary_key=True)
    PeriodId = Column(Integer, ForeignKey(Period.PeriodId), primary_key=True)
    SpIndex = Column(Integer, ForeignKey(Species.SpIndex), primary_key=True)
    Obs = Column(Float, nullable=False)

    def __repr__(self):
        return f"Observation(loc_id = {self.LocId}, period = {self.PeriodId}, sp_index = {self.SpIndex}, obs = {self.Obs})"


class AnalysisConfig(Base):
    __tablename__ = "Analyses"
    UserId = Column(String(40), ForeignKey(User.UserId), primary_key=True)
    AnalysisId = Column(String(100), nullable=False, primary_key=True)
    AnalysisName = Column(String(100))
    PeriodId = Column(Integer, ForeignKey(Period.PeriodId))


class HotspotConfig(Base):
    __tablename__ = "HotspotConfigs"
    UserId = Column(String(40), ForeignKey(User.UserId), primary_key=True)
    AnalysisId = Column(
        Integer, ForeignKey(AnalysisConfig.AnalysisId), primary_key=True
    )
    LocId = Column(String(10), ForeignKey(Hotspot.LocId), primary_key=True)
    IsActive = Column(Integer, nullable=False)


class SeenBird(Base):
    __tablename__ = "SeenBirds"
    UserId = Column(String(40), ForeignKey(User.UserId), primary_key=True)
    AnalysisId = Column(
        Integer, ForeignKey(AnalysisConfig.AnalysisId), primary_key=True
    )
    SpIndex = Column(Integer, ForeignKey(Species.SpIndex), primary_key=True)


class KeyBird(Base):
    __tablename__="KeyBirds"
    UserId = Column(String(40), ForeignKey(User.UserId), primary_key=True)
    AnalysisId = Column(Integer, ForeignKey(AnalysisConfig.AnalysisId), primary_key=True)
    SpIndex = Column(Integer, ForeignKey(Species.SpIndex), primary_key=True)

class DBInterface:
    def __init__(self) -> None:
        pass

    def sp_name_from_index(sp_index: int) -> str:
        pass

    def hs_name_from_loc_id(loc_id: str) -> str:
        pass

    def collect_observations(loc_id: str, period: int) -> dict:
        pass


# Base.metadata.create_all(engine)
# Base.metadata.bind = engine
