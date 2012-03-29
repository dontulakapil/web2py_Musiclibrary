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
