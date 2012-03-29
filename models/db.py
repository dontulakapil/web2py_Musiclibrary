# -*- coding: utf-8 -*- 

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
#########################################################################

if request.env.web2py_runtime_gae:            # if running on Google App Engine
    db = DAL('gae')                           # connect to Google BigTable
    session.connect(request, response, db=db) # and store sessions and tickets there
    ### or use the following lines to store sessions in Memcache
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db=MEMDB(Client())
else:                                         # else use a normal relational database
    db = DAL('sqlite://storage.sqlite')       # if not, use SQLite or other DB
## if no need for session
# session.forget()

#########################################################################
## Here is sample code if you need for 
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - crud actions
## comment/uncomment as needed

from gluon.tools import *
auth=Auth(globals(),db)                      # authentication/authorization
auth.settings.hmac_key='sha512:0b6b5e1d-4a77-41dd-8b4e-4f8a423334ed'
auth.define_tables()                         # creates all needed tables
crud=Crud(globals(),db)                      # for CRUD helpers using auth
service=Service(globals())                   # for json, xml, jsonrpc, xmlrpc, amfrpc

# crud.settings.auth=auth                      # enforces authorization on crud
# mail=Mail()                                  # mailer
# mail.settings.server='smtp.gmail.com:587'    # your SMTP server
# mail.settings.sender='you@gmail.com'         # your email
# mail.settings.login='username:password'      # your credentials or None
# auth.settings.mailer=mail                    # for user email verification
# auth.settings.registration_requires_verification = True
# auth.settings.registration_requires_approval = True
# auth.messages.verify_ = 'Click on the link http://'+request.env.http_host+URL(r=request,c='default',f='user',args=['verify_email'])+'/%(key)s to verify your email'
# auth.settings.reset_password_requires_verification = True
# auth.messages.reset_password = 'Click on the link http://'+request.env.http_host+URL(r=request,c='default',f='user',args=['reset_password'])+'/%(key)s to reset your password'
## more options discussed in gluon/tools.py
#########################################################################

#########################################################################
## Define your tables below, for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################
import datetime
#this table specifies album in which the song is being added. The user when adds the song the album name gets extracted from the song and is added to the album table. This gives us a clear division of songs based on albums ###
db.define_table('languages',
Field('name','string'))

db.define_table('album',
Field('name','string'),
Field('info','text'),
Field('image','upload'),
Field('language',db.languages)
)
db.album.language.requires = IS_IN_DB(db,'languages.id','languages.name')
## This table is for all the languages
db.define_table('songs',
    Field('name','string'),
    Field('file','upload'),
    Field('userid',db.auth_user),
    Field('album',db.album),
    Field('artist','string'),
    Field('duration','integer'),
    Field('datetime1','string'),
    Field('language',db.languages))
db.songs.language.requires = IS_IN_DB(db,'languages.id','languages.name')
db.songs.album.requires = IS_IN_DB(db,'album.id','album.name')
db.songs.userid.requires = IS_IN_DB(db,'auth_user.id','auth_user.first_name')
#This is for the comments
db.define_table('comments',
Field('userid',db.auth_user),
Field('songid',db.songs),
Field('comment','text'),
Field('language',db.languages)
)
db.album.language.requires = IS_IN_DB(db,'languages.id','languages.name')
db.comments.songid.requires = IS_IN_DB(db,'songs.id','songs.name')
db.comments.userid.requires = IS_IN_DB(db,'auth_user.id','auth_user.first_name')
#This is for average rating
db.define_table('rating',
    Field('songid',db.songs),
    Field('rating','integer'),
    Field('noofusersrated','integer'))
db.rating.songid.requires = IS_IN_DB(db,'songs.id','songs.name')
#This is for the various playlists which the user can add like favourites,language wise.....
db.define_table('playlist',
    Field('userid',db.auth_user),
    Field('name','string'))
#This is for the rating of the song the user can rate all the songs...
db.define_table('ratings',
    Field('userid',db.auth_user),
    Field('songid',db.songs),
    Field('rating','integer'))
#This is for the separation of songs into the various playlists for the specified user
db.define_table('like',
    Field('songid',db.songs),
    Field('userid',db.auth_user),
    Field('plylist',db.playlist))
db.like.songid.requires = IS_IN_DB(db,'songs.id','songs.name')
db.like.plylist.requires = IS_IN_DB(db,'playlist.id','playlist.name')
db.like.userid.requires = IS_IN_DB(db,'auth_user.id','auth_user.first_name')
#this is for portal feed back to improve technically
db.define_table('feedback',
    Field('userid',db.auth_user),
    Field('feedback','text',requires = [IS_NOT_EMPTY()]))
#This table is for requesting any songs from users to all and admin
db.define_table('requests',
    Field('userid',db.auth_user),
    Field('request','text',requires = [IS_NOT_EMPTY()]))
# this table is to report is any songs is against to rules to admin to del them from users
db.define_table('reportabuse',
    Field('userid',db.auth_user),
    Field('songid',db.songs))
#this table is for user to upload his profile pic
db.define_table('uploadpic',
    Field('userid',db.auth_user),
    Field('file','upload'))
db.ratings.userid.requires=IS_IN_DB(db,'auth_user.id','auth_user.first_name')
db.ratings.songid.requires=IS_IN_DB(db,'songs.id','songs.name')
db.uploadpic.userid.requires = IS_IN_DB(db,'auth_user.id','auth_user.first_name')
db.playlist.userid.requires = IS_IN_DB(db,'auth_user.id','auth_user.first_name')
db.reportabuse.songid.requires = IS_IN_DB(db,'songs.id','songs.name')
db.rating.songid.writable = db.rating.songid.readable = False
db.album.id.writable = db.album.id.readable = False
db.songs.id.writable = db.songs.id.readable = False
db.comments.id.writable = db.comments.id.readable = False
db.rating.id.writable = db.rating.id.readable = False
db.like.id.writable = db.like.id.readable = False
db.feedback.id.writable = db.feedback.id.readable = False
db.songs.userid.writable = db.songs.userid.readable = False
db.requests.userid.writable = db.requests.userid.readable = False
db.reportabuse.userid.writable = db.reportabuse.userid.readable = False
db.requests.id.writable = db.requests.id.readable = False
db.reportabuse.id.writable = db.reportabuse.id.readable = False
db.playlist.id.writable = db.playlist.id.readable = False
db.feedback.userid.writable = db.feedback.id.readable = False
db.comments.userid.writable = db.comments.userid.readable = False
db.comments.songid.writable = db.comments.songid.readable = False

