import json
import os
from flask_restful import Resource
from flask import jsonify, request
import requests
from http import HTTPStatus
from  config import Config
from ...dataContext import db
from ...producer.queueProducer import task_posted
from ...models.conversion import Conversion,VideoFormats
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity


config = Config()


class ConversionView(Resource):
    @jwt_required()
    def post(self):
        file = request.files['fileName']
        json_data=request.form.get('data')
        data = json.loads(json_data)
        newFormat=data['newFormat']
        
        extension = os.path.splitext(file.filename)[1]

        destination=VideoFormats.AVI
        if str(newFormat)=='AVI':
            destination=VideoFormats.AVI
        elif str(newFormat)=='WMV':
            destination=VideoFormats.WMV
        elif str(newFormat)=='WEBM':
            destination=VideoFormats.WEBM
        elif str(newFormat)=='MP4':
            destination=VideoFormats.MP4
        elif str(newFormat)=='MPEG':
            destination=VideoFormats.MPEG
        else:
            return {"message": "The format is not supported"}, HTTPStatus.BAD_REQUEST


        if str(newFormat)==extension.upper().replace('.',''):
            return {"message": "The destination format is equal to source format"}, HTTPStatus.BAD_REQUEST

        conversion=Conversion(
            file_name=file.filename,
            new_format=destination
        )

        db.session.add(conversion)
        db.session.commit()

        #storing file
        file.save(config.PATH_STORAGE+'input/'+str(conversion.id)+file.filename)

        args = ({
            "id":str(conversion.id),
            "fileName":file.filename,
            "newFormat":str(newFormat)
        },)
        task_posted.apply_async(args)
        return {"message": "Conversion task in progress, please check in some minutes"}, HTTPStatus.OK