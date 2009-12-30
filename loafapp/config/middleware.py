# -*- coding: utf-8 -*-
"""WSGI middleware initialization for the LoafApp application."""

from loafapp.config.app_cfg import base_config
from loafapp.config.environment import load_environment
import tempfile
import hashlib
import datetime
import os
#from repoze.who.config import make_middleware_with_config as with_who

from gp.fileupload import Storage

__all__ = ['make_app']

# Use base_config to setup the necessary PasteDeploy application factory. 
# make_base_app will wrap the TG2 app with all the middleware it needs.
make_base_app = base_config.setup_tg_wsgi_app(load_environment)


def make_app(global_conf, full_stack=True, **app_conf):
    """
    Set LoafApp up with the settings found in the PasteDeploy configuration
    file used.
    
    :param global_conf: The global settings for LoafApp (those
        defined under the ``[DEFAULT]`` section).
    :type global_conf: dict
    :param full_stack: Should the whole TG2 stack be set up?
    :type full_stack: str or bool
    :return: The LoafApp application with all the relevant middleware
        loaded.
    
    This is the PasteDeploy factory for the LoafApp application.
    
    ``app_conf`` contains all the application-specific settings (those defined
    under ``[app:main]``.
   
    """
    app = make_base_app(global_conf, full_stack=True, **app_conf)
    pm = global_conf.pop('postmortem', 'false')

    udd = app_conf.get('upload_dest_dir', None)
    max_size = app_conf.get('upload_max_size', 150000)
    if udd is not None:
        #hexd = hashlib.sha1(str(datetime.datetime.now())).hexdigest()
        tmpdir =  os.path.join(tempfile.gettempdir(), 'loaf')
        app = Storage(app, upload_to=udd, tempdir=tmpdir, max_size=max_size)
    if pm != 'false':
        from repoze.debug.pdbpm import PostMortemDebug
        app = PostMortemDebug(app)    
    return app

##     try:
##         app = with_who(app, global_conf,
##                        app_conf.get('who.config.file', 'who.ini'),
##                        app_conf.get('who.log_file', 'stdout'),
##                        app_conf.get('who.log_level', 'debug')
##                        )
##     except :
##         import pdb, sys; pdb.post_mortem(sys.exc_info()[2])
##         raise
