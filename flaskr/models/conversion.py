from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from ..dataContext.sqlAlchemyContext import db
from datetime import datetime
from sqlalchemy import DateTime,Enum
from sqlalchemy.sql import func
from enum import Enum as PythonEnum


class VideoFormats(PythonEnum):
    MP4 = 'MP4'
    WEBM = 'WEBM'
    AVI = 'AVI'
    MPEG = 'MPEG'
    WMV = 'WMV'

    def serialize(self):
        return self.value

class EnumVideoFormats(Enum):
    def __init__(self, enum_type):
        super(EnumVideoFormats, self).__init__(enum_type)

    def process_bind_param(self, value, dialect):
        return value.value

    def process_result_value(self, value, dialect):
        return VideoFormats(value)

class Conversion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(250))
    new_format = db.Column(EnumVideoFormats(VideoFormats))
    time_stamp = db.Column(DateTime, default=func.now())
    status = db.Column(db.String(100), default='uploaded')

class ConversionSchema(SQLAlchemyAutoSchema):

    class Meta:
        model = Conversion
        include_relationships = True
        load_instance = True
        