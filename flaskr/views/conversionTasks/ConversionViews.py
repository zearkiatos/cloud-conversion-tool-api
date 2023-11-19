import json
import asyncio
import os
from flask_restful import Resource
from flask import jsonify, request,send_file
import requests
from http import HTTPStatus
from  config import Config
from ...dataContext import db
from ...producer.pubsub.queueProducerByApi import publish_message
from ...models.conversion import Conversion,VideoFormats,ConversionSchema
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from enum import Enum
from google.cloud import storage
from config import Config


config = Config()

conversion_schema=ConversionSchema()
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
        
        user_id = get_jwt_identity()


        if str(newFormat)==extension.upper().replace('.',''):
            return {"message": "The destination format is equal to source format"}, HTTPStatus.BAD_REQUEST

        conversion=Conversion(
            file_name=file.filename,
            new_format=destination,
            user = user_id
        )

        db.session.add(conversion)
        db.session.commit()

        #storing file
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(config.CONVERSION_BUCKET)
        blob = bucket.blob('input/'+str(conversion.id)+file.filename)
        blob.upload_from_file(file)

        try:
            message = {
                "id":str(conversion.id),
                "fileName":file.filename,
                "newFormat":str(newFormat),
                "userId":conversion.user
            }
            publish_message(config.GOOGLE_PROJECT_ID, config.TOPICS['TASK_POSTED'],message)

        except Exception as ex:
            return {
                "message": f'error: {str(ex)}' 
            }, HTTPStatus.INTERNAL_SERVER_ERROR
        return {"id":str(conversion.id), "message": "Conversion task in progress, please check in some minutes"}, HTTPStatus.OK
    



class RecoveryTaskView(Resource):
    @jwt_required()
    def get(self,id_task):
        user_id = get_jwt_identity()
        conversion_task=Conversion.query.filter_by(id=id_task, user=user_id).one_or_none()
        if conversion_task is not None:
            object_to_return={
                'id':conversion_task.id,
                'file_name':conversion_task.file_name,
                'new_format':conversion_task.new_format.serialize(),
                'time_stamp':conversion_task.time_stamp.strftime('%Y-%m-%d %H:%M:%S'),
                'status':conversion_task.status,
                'link_original_file': config.BUCKET_URL+ 'input/'+str(conversion_task.id)+conversion_task.file_name,
                'link_converted_file':config.BUCKET_URL+'output/'+str(conversion_task.id)+conversion_task.file_name+'.'+str(conversion_task.new_format.serialize()).lower()
            }
            return object_to_return, HTTPStatus.OK
        else:
            return {"message": "The id provided doesn't exist in the system "}, HTTPStatus.NOT_FOUND
       
class ConversionsView(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        conversions_task=Conversion.query.filter_by(user=user_id).all()
        list_conversions=[]
        for conversion_task in conversions_task:
            converted_file_url = config.BUCKET_URL+'output/'+str(conversion_task.id)+conversion_task.file_name+'.'+str(conversion_task.new_format.serialize()).lower() if conversion_task.status=='processed' else ''
            conversion={
                    'id':conversion_task.id,
                    'file_name':conversion_task.file_name,
                    'new_format':conversion_task.new_format.serialize(),
                    'time_stamp':conversion_task.time_stamp.strftime('%Y-%m-%d %H:%M:%S'),
                    'status':conversion_task.status,
                    'link_original_file': config.BUCKET_URL+ 'input/'+str(conversion_task.id)+conversion_task.file_name,
                    'link_converted_file':converted_file_url
            }
           
            list_conversions.append(conversion)
        return jsonify(list_conversions)

class RemoveTaskView(Resource):
    @jwt_required()
    def delete(self,id_task):
        user_id = get_jwt_identity()
        conversion_task=Conversion.query.filter_by(id=id_task, user=user_id).one_or_none()
        if conversion_task is not None:
            #processed
            if conversion_task.status=='uploaded':
                db.session.delete(conversion_task)
                db.session.commit()
                #deleting files
                try:
                    storage_client = storage.Client()
                    bucket = storage_client.get_bucket(config.CONVERSION_BUCKET)
                    #borrando archivo origen
                    blob = bucket.blob('input/'+str(conversion_task.id)+conversion_task.file_name)
                    blob.delete()
                    #borrando archivo destino
                    blob = bucket.blob('output/'+str(conversion_task.id)+conversion_task.file_name+'.'+str(conversion_task.new_format.serialize()).lower())
                    blob.delete()
                except Exception as ex:
                    pass
                
                return {
                        'message': 'Conversion task deleted successfully'
                    }, HTTPStatus.NO_CONTENT
            else:
                return {"message": "The id provided doesn't available in this moment"}, HTTPStatus.NOT_FOUND
        else:
            return {"message": "The id provided doesn't exist in the system "}, HTTPStatus.NOT_FOUND
