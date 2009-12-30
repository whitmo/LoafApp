from tg import request, response, expose, flash, redirect, config
from tg.controllers import CUSTOM_CONTENT_TYPE
from tgext.geo.featureserver.controller import FeatureServerController
from loafapp.model import DBSession, Spot
import geoalchemy as geo
import os


class LFC(FeatureServerController):
    """
    Loaf feature controller

    Adds extra behavior for handling special form style image posts
    """

    @staticmethod
    def dest_dir():
        return config.get('app_conf').get('upload_dest_dir')
    
    def get(self):
        response.content_type, resp = self.server.dispatchRequest(
            path_info=request.path_info, params=request.GET, base_path= "")
        return resp

    def handle_upload_and_post(self, relfile):
        vals = (x, request.POST.get(x)) for x in dir(Spot) if not x.startswith('_'))
        valmap = dict([x for x in vals if x[1]])
        valmap['geom'] = geo.WKTSpatialElement("POINT(%s, %s)" %(lon, lat))
        if relfile:
            upload = os.path.join(self.dest_dir(), relfile)
            assert os.path.exists(upload), "Uploaded file not found"
            valmap['image_path']=upload
        newspot = Spot(**valmap)
        DBSession.add(newspot)

    def post(self):
        image = request.params.get('image', None)

        # this is an image upload
        if image is not None:
            return self.handle_upload_and_post(image.file.read().strip())
            
        if request.POST.keys():
            data = request.POST.keys()[0]
        else:
            data = request.body
            request.content_type, resp = self.server.dispatchRequest(
                params=request.params, path_info=request.path_info,
                base_path="", post_data=data, request_method="POST")
            return resp
        
    def delete(self):
        response.content_type, resp = self.server.dispatchRequest(
            params=request.params, path_info=request.path_info,
            base_path="", post_data="", request_method="DELETE")
        return resp

    @expose(content_type=CUSTOM_CONTENT_TYPE)
    def default(self, *args, **kw):
        if request.method == 'GET':
            return self.get()
        elif request.method == 'POST':
            return self.post()
        elif request.method == 'DELETE':
            return self.delete()
        else:
            flash("Unsupported method type %s" % request.method)
            redirect(request.referer)

        
