import json
import os
from flask_restful import Resource
from flask import jsonify, request,send_file
import requests
from http import HTTPStatus
from  config import Config
from ...dataContext import db
from ...producer.queueProducer import task_posted
from ...models.conversion import Conversion,VideoFormats,ConversionSchema
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from enum import Enum


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
        return {"id":str(conversion.id), "message": "Conversion task in progress, please check in some minutes"}, HTTPStatus.OK
    



class RecoveryTaskView(Resource):
    @jwt_required()
    def get(self,id_task):
        conversion_task=Conversion.query.filter_by(id=id_task).one_or_none()
        if conversion_task is not None:
            object_to_return={
                'id':conversion_task.id,
                'file_name':conversion_task.file_name,
                'new_format':conversion_task.new_format.serialize(),
                'time_stamp':conversion_task.time_stamp.strftime('%Y-%m-%d %H:%M:%S'),
                'status':conversion_task.status,
                'link_original_file': config.APP_URL+ 'api/downloadoriginalfile/'+str(conversion_task.id),
                'link_converted_file':config.APP_URL+'api/downloadconvertedfile/'+str(conversion_task.id)
            }
            return object_to_return, HTTPStatus.OK
        else:
            return {"message": "The id provided doesn't exist in the system "}, HTTPStatus.NOT_FOUND
       

class DownloadOriginalFile(Resource):
    def get(self,id_task):
        conversion_task=Conversion.query.filter_by(id=id_task).one_or_none()
        if conversion_task is not None:
            nombre_archivo = config.PATH_STORAGE+'input/'+str(conversion_task.id)+conversion_task.file_name
            if os.path.exists(nombre_archivo):
                return send_file(nombre_archivo, as_attachment=True)
            else:
                return 'File not found', 404
        else:
            return 'File not found', 404
        

class DownloadConvertedFile(Resource):
    def get(self,id_task):
        conversion_task=Conversion.query.filter_by(id=id_task).one_or_none()
        if conversion_task is not None:
            nombre_archivo = config.PATH_STORAGE+'output/'+str(conversion_task.id)+conversion_task.file_name+'.'+str(conversion_task.new_format.serialize()).lower()
            if os.path.exists(nombre_archivo):
                return send_file(nombre_archivo, as_attachment=True)
            else:
                return 'File not found', 404
        else:
            return 'File not found', 404
        
class ConversionsView(Resource):
    @jwt_required()
    def get(self):
        conversions_task=Conversion.query.all()
        list_conversions=[]
        for conversion_task in conversions_task:
            conversion={
                'id':conversion_task.id,
                'file_name':conversion_task.file_name,
                'new_format':conversion_task.new_format.serialize(),
                'time_stamp':conversion_task.time_stamp.strftime('%Y-%m-%d %H:%M:%S'),
                'status':conversion_task.status,
                'link_original_file': config.APP_URL+ 'api/downloadoriginalfile/'+str(conversion_task.id),
                'link_converted_file':config.APP_URL+'api/downloadconvertedfile/'+str(conversion_task.id)
            }
            list_conversions.append(conversion)
        return jsonify(list_conversions)

class RemoveTaskView(Resource):
    @jwt_required()
    def delete(self,id_task):
        conversion_task=Conversion.query.filter_by(id=id_task).one_or_none()
        if conversion_task is not None:
            if conversion_task.status=='processed':
                db.session.delete(conversion_task)
                db.session.commit()
                #deleting files
                nombre_archivo = config.PATH_STORAGE+'input/'+str(conversion_task.id)+conversion_task.file_name
                if os.path.exists(nombre_archivo):
                    try:
                        os.remove(nombre_archivo)
                    except Exception as ex:
                        pass
                nombre_archivo = config.PATH_STORAGE+'output/'+str(conversion_task.id)+conversion_task.file_name+'.'+str(conversion_task.new_format.serialize()).lower()
                if os.path.exists(nombre_archivo):
                    try:
                        os.remove(nombre_archivo)
                    except Exception as ex:
                        pass
                return {
                        'message': 'Conversion task deleted successfully'
                    }, HTTPStatus.NO_CONTENT
            else:
                return {"message": "The id provided doesn't available in this moment"}, HTTPStatus.NOT_FOUND
        else:
            return {"message": "The id provided doesn't exist in the system "}, HTTPStatus.NOT_FOUND