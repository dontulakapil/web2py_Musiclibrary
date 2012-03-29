# -*- coding: utf-8 -*- 

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################
import os  
def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html
    """
    response.files.append("http://ajax.googleapis.com/ajax/libs/jqueryui/1.7.2/jquery-ui.min.js")
    response.files.append(URL(r=request,c='static/jqueryui/css/ui-darkness',f='jquery-ui-1.7.2.custom.css'))
    response.files.append(URL(r=request,c='static/jquery.jqGrid/src/i18n',f='grid.locale-en.js'))
    response.files.append(URL(r=request,c='static/jquery.jqGrid/js',f='jquery.jqGrid.min.js'))
    response.files.append(URL(r=request,c='static/jquery.jqGrid/css',f='ui.jqgrid.css'))
    response.flash = T('Welcome to Your Music Library')
    file1=db(db.uploadpic.userid>0).select()
    form=db(db.playlist.userid==auth.user_id).select()
    firstname=db().select(db.auth_user.ALL)
    #lastname=auth.user_last_name
    form1=db().select(db.songs.ALL)
    return dict(firstname=firstname,message=T('Hello World'),file1=file1,form=form,form1=form1)


def user():
    """
    exposes:
    http://..../[app]/default/user/login 
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    session.forget()
    return service()



def myplaylist():
    form=db(db.playlist.userid==auth.user_id).select()
    form1=db().select(db.songs.ALL)
    return(dict(form=form,form1=form1))
def playlistsongs():
    k=request.args(0)
    song=db(db.like.plylist==k).select()
    #row=db().select(db.like.ALL, db.songs.ALL, left=db.like.on(db.songs.id==db.like.songid))
    song1=db().select(db.songs.ALL)
    return(dict(row=song,song1=song1,k=k))
def rating():
    k=request.args(0)
    k2=request.args(1)
    k1=request.args(2)
#    form=SQLFORM(db.ratings)
    form=db((db.ratings.userid==auth.user_id)&(db.ratings.songid==k)).select()
    if(len(form)!=0):
       form1=db(db.rating.songid==k).select()
       if(len(form1)!=0):           
           total=((form1[0].rating*form1[0].noofusersrated)-form[0].rating+int(k2))/form1[0].noofusersrated
           form1[0].update_record(rating=total)
       else:
           db.rating.insert(songid=k,rating=k2,noofusersrated='1')
       form[0].update_record(rating=k2)
    else:
       db.ratings.insert(userid=auth.user_id,rating=k2,songid=k)
       db.rating.insert(rating=k2,noofusersrated='1',songid=k)
    session.flash = 'rated'
    redirect(URL(r=request,f="playlistsongs",args=k1))
    return(dict(form=form))
def upload():
    form=SQLFORM(db.songs)
    form.vars.userid=auth.user_id
    path1=os.getcwd()
    if form.accepts(request.vars,session):
        k=form.vars.id
        form=db(db.songs.id==k).select()
        from mutagen.mp3 import MP3
        from mutagen.easyid3 import EasyID3
        path1=os.getcwd()
        #path2=os.path.join(path,form.vars.file)
        form3=db().select(db.songs.ALL)
        path2=str(path1)+'/applications/Musiclibrary/uploads/'+str(form3[-1].file)
        m = MP3(path2, ID3=EasyID3)
        form[0].update_record(artist=m['artist'][0])
        form[0].update_record(name= m['title'][0])
        form[0].update_record(datetime1=m['date'][0])
        form[0].update_record(duration= m.info.length)
        #redirect(URL(r=request,f="test1",args=k))
        k1=str(m['album'][0])
        form1=db(db.album.name==k).select()
        #redirect(URL(r=request,f="test3",args=[k1]))
        if(len(form1)!=0):
            form[0].update_record(album=form1[0].id)
        else:
            db.album.insert(name=k1,language=form[0].language)
            k=(db().select(db.album.ALL))[-1].id
            form[0].update_record(album=k)            
            redirect(URL(r=request,f="test3",args=[k]))      
    return(dict(form=form,path1=path1))
def test1():
    form1=SQLFORM(db.album)
    form1.vars.album=request.args(1)
    if form1.accepts(request.vars,session):
        form=db(db.songs.id==request.args(0)).select()
        k=request.vars.id
        form[0].update_record(album=k)
       # redirect(URL(r=request,f="test2",args=[request.args(0)]))
    return(dict(k=request.args(0),form1=form1,k1=request.args(1)))
def test2():
    k=request.args(0)
    l='%'+str(k)+'%'
    if(request.args[1]=='Songs'):
        return (dict(row=db(db.songs.name.upper().like(l)).select(),k=request.args(0)))
    if(request.args[1]=='Album'):
        return (dict(row=db(db.album.name.upper().like(l)).select(),k=request.args(0)))
    if(request.args[1]=='Artist'):
        return (dict(row=db(db.songs.artist.upper().like(l)).select(),k=request.args(0)))
    if(request.args[1]=='User'):
        return (dict(row=db(db.auth_user.first_name.upper().like(l)).select(),k=request.args(0)))
def test3():
    #return(dict(form=db(db.album.id=request.args(0)).select()))
     return dict(form=crud.update(db.album, request.args(0),next=URL(r=request,f="index")))
def albums():
    k=request.args(0)
    form=db(db.album.id==k).select()
    form1=db(db.songs.album==k).select()
    form2=db().select(db.songs.ALL)
    return(dict(form=form,form1=form1,form2=form2))

def search():
    form = SQLFORM.factory(
        Field('search', requires=IS_NOT_EMPTY()),
        Field('field',requires=IS_IN_SET(['Album','Songs','Artist','User']),default='Male',widget=SQLFORM.widgets.radio.widget)
        )
    if form.accepts(request.vars, session):
       redirect(URL(r=request,f="test2",args=[form.vars.search,form.vars.field]))     
    return(dict(form=form))
def feedback():
    form=SQLFORM(db.feedback)
    form.vars.userid=auth.user_id
    if form.accepts(request.vars, session):
        session.flash = 'Feedback Submited'
        redirect(URL(r=request,f="index"))
    return(dict(form=form))
def reportabuse():
    form=SQLFORM(db.reportabuse)
    form.vars.userid=auth.user_id
    if form.accepts(request.vars, session):
        session.flash = 'Submited'
        redirect(URL(r=request,f="index"))
    return(dict(form=form))
def comments():
    k=request.args(0)
    form=SQLFORM(db.comments)
    form.vars.userid=auth.user_id
    form.vars.songid=k
    rows=db(db.comments.songid==k).select(db.comments.ALL, db.auth_user.ALL, left=db.comments.on(db.auth_user.id==db.comments.userid))
    form1=db(db.comments.songid==k).select()
    if form.accepts(request.vars,session):
        response.flash=T('Comment Added')
        redirect(URL(r=request,f="comments",args=k))
    return dict(form=form,k=k,form1=rows)
def others():
    k=request.args(0)
    response.flash = T('Welcome to Your Music Library')
    file1=db().select(db.uploadpic.ALL)
    form=db(db.playlist.userid==k).select()
    firstname=db(db.auth_user.id==k).select()
    users=db().select(db.auth_user.ALL)
    #lastname=auth.user_last_name
    return dict(users=users,firstname=firstname,message=T('Hello World'),file1=file1,form=form)
def delete():
    db(db.songs.id>0).delete()
def album():
    form=db(db.album.language=='1').select()
    form1=db(db.album.language=='2').select()
    form2=db(db.album.language=='3').select()
    return(dict(form=form,form1=form1,form2=form2))
def test4():
    return(dict(k=request.args(0)))
@service.json
def get_rows():
    db.songs.category.represent = lambda v: v.name
    fields = ['id','name','artist','duration']
    rows = []
    page = int(request.vars.page)
    pagesize = int(request.vars.rows)    
    limitby = (page * pagesize - pagesize,page * pagesize)
    orderby = db.songs[request.vars.sidx]
    if request.vars.sord == 'desc': orderby = ~orderby
    for r in db(db.songs.id>0).select(limitby=limitby,orderby=orderby):
        vals = []
        for f in fields:
            rep = db.songs[f].represent
            if rep:
                vals.append(rep(r[f]))
            else:
                vals.append(r[f])
        rows.append(dict(id=r.id,cell=vals))
    total = db(db.songs.id>0).count()       
    pages = int(total/pagesize)
    #if total % pagesize == 0: pages -= 1 
    data = dict(total=pages,page=page,rows=rows)
    return data
