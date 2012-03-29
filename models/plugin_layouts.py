if not response.menu: response.menu=[]
response.menu.append(('Change Layout',False,URL(request.application,'plugin_layouts','index')))
