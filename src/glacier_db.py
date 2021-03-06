#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: glacier_db

:Synopsis:
    A class to manage and store log information from successful archive uploads
    from PASTA to the AWS Glacier data storage.
:Author:
    servilla
  
:Created:
    1/15/17
"""

import os

import daiquiri
from sqlalchemy import Column, Integer, Float, String, Date, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
logger = daiquiri.getLogger("glacier_db.py: " + __name__)


class GlacierUploadLog(Base):

    __tablename__ = "glacier_upload_log"

    package = Column(String, primary_key=True)
    identifier = Column(String, nullable=False)
    location = Column(String, nullable=False)
    size = Column(Integer, nullable=False)
    checksum = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)


class GlacierDb(object):

    def __init__(self, db_name):
        from sqlalchemy import create_engine
        self.db_name = db_name
        engine = create_engine("sqlite:///" + self.db_name)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def add_upload_record(
        self,
        package=None,
        identifier=None,
        location=None,
        size=None,
        checksum=None,
        timestamp=None,
    ):

        record = GlacierUploadLog(
            package=package,
            identifier=identifier,
            location=location,
            size=size,
            checksum=checksum,
            timestamp=timestamp,
        )

        self.session.add(record)
        self.session.commit()

    def get_record_by_package(self, package):
        record = (
            self.session.query(GlacierUploadLog)
            .filter(GlacierUploadLog.package == package)
            .one_or_none()
        )
        return record

    def package_exists(self, package=None):
        record = (
            self.session.query(GlacierUploadLog)
            .filter(GlacierUploadLog.package == package)
            .one_or_none()
        )
        if record is not None:
            return True
        else:
            return False


def main():
    return 0


if __name__ == "__main__":
    main()
