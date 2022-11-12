# coding: utf-8
from sqlalchemy import BigInteger, CheckConstraint, Column, Integer, String, text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Experiment(Base):
    __tablename__ = 'experiments'
    __table_args__ = (
        CheckConstraint("(lifecycle_stage)::text = ANY ((ARRAY['active'::character varying, 'deleted'::character "
                        "varying])::text[])"),
        {'schema': 'mlflow'})

    experiment_id = Column(Integer, primary_key=True, server_default=text("nextval('experiments_experiment_id_seq"
                                                                          "'::regclass)"))
    name = Column(String(256), nullable=False, unique=True)
    artifact_location = Column(String(256))
    lifecycle_stage = Column(String(32))
    creation_time = Column(BigInteger)
    last_update_time = Column(BigInteger)
