import os
import socket
import datetime
import copy
import gluon.contenttype
import gluon.fileutils

# ## critical --- make a copy of the environment

global_env = copy.copy(globals())
global_env['datetime'] = datetime

http_host = request.env.http_host.split(':')[0]
remote_addr = request.env.remote_addr
try:
    hosts = (http_host, socket.gethostname(),
             socket.gethostbyname(http_host),
             '::1','127.0.0.1','::ffff:127.0.0.1')   
except:
    hosts = (http_host, )

if request.env.http_x_forwarded_for or request.env.wsgi_url_scheme\
     in ['https', 'HTTPS']:
    session.secure()
elif remote_addr not in hosts:
    raise HTTP(200, T('appadmin is disabled because insecure channel'))
if not gluon.fileutils.check_credentials(request):
    redirect('/admin')
    
def index():
    plugin = request.controller
    import os, shutil
    src = os.path.join(request.folder,'views','layout.html')
    dst = os.path.join(request.folder,'private',plugin+'.layout.html')
    original = os.path.exists(dst)
    if request.vars.apply:
        if not original:
           shutil.copyfile(src, dst)
        open(src,'w').write('{{extend "%s/layouts/%s.html"}}{{include}}' \
                                % (plugin,request.vars.apply)) 
        response.flash="plugin applied"
    elif request.vars.revert:
        shutil.copyfile(dst, src)
        response.flash="reverted to original"
    layouts = os.listdir(os.path.join(request.folder,'views',plugin,'layouts'))
    layouts = [layout[:-5] for layout in layouts if layout.endswith('.html')]
    return dict(layouts=layouts, original=original)
