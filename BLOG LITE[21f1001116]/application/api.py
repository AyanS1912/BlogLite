from flask_restful import Resource,Api,fields,marshal_with,reqparse
from application.database import db
from application.models import User,Post
from application.validations import NotFoundError,ValidatonError


api=Api()


#-----------------------------------------------------USER---------------------------------------------------------------
newuser=reqparse.RequestParser()
newuser.add_argument('name')
newuser.add_argument('username')
newuser.add_argument('password')

user_input_data = {
  "id": fields.Integer,
  "name": fields.String,
  "username": fields.String,
  "password": fields.String,
}
#----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------POST------------------------------------------------------------------
newpost=reqparse.RequestParser()
newpost.add_argument('title')
newpost.add_argument('desc')
newpost.add_argument('img')
newpost.add_argument('mimetype')


post_input_data = {
  "id": fields.Integer,
  "title": fields.String,
  "desc": fields.String,
  "img": fields.String,
  "mimetype":fields.String,
}
#----------------------------------------------------------------------------------------------------------------------


#-----------------------------------------------------USER API---------------------------------------------------------------
class User_api(Resource):

#-----------------------------------------------------USER_GET_API---------------------------------------------------------------
  @marshal_with(user_input_data)
  def get(self,username=None):
    if (username == ''):
      raise ValidatonError(status_code=404,error_code="UGET01",error_message="Username should not be empty")
      user = User.query.filter_by(username=username).first()
      if (user == ''):
        raise ValidatonError(status_code=404,error_code="UGET02",error_message="User not Available!,Provide Valid User.")
        return user

#-----------------------------------------------------USER_POST_API---------------------------------------------------------------
  @marshal_with(user_input_data)
  def post(self,username=None):
    user_post = newuser.parse_args()
    name = user_post.get('name',None)
    username = user_post.get('username',None)
    password = user_post.get('password',None)
    user = User.query.filter_by(username=username).first()
    
    if user:
      raise ValidatonError(status_code=404,error_code="UPOST01",error_message="Username already exists,Try Another Username")
    if name == '':
      raise ValidatonError(status_code=404,error_code="UPOST02",error_message="Name should not be empty")
    if username == '':
      raise ValidatonError(status_code=404,error_code="UPOST03",error_message="Username should not be empty")
    if password == '':
      raise ValidatonError(status_code=404,error_code="UPOST04",error_message="Password should not be empty")
        
    user = User(name=name,username=username,password=password)
    db.session.add(user)
    db.session.commit()
    return user

#-----------------------------------------------------USER_PUT_API---------------------------------------------------------------
  @marshal_with(user_input_data)
  def put(self,username=None):
    user = User.query.filter_by(username=username).first()
    user_put = user.parse_args()
    name = user_put.get('name',None)
    username = user_put.get('username',None)
    if user is None:
      raise ValidatonError(status_code=404,error_code="UPUT01",error_message="User not Available!")
    if name:
      user.name = name
    if username:
      user.username = username
      
    db.session.commit()
    return user

#-----------------------------------------------------USER_DELETE_API--------------------------------------------------------------------------
  @marshal_with(user_input_data)   
  def delete(self,username=None):
    user = User.query.filter_by(username=username).first()
    if user:
      db.session.delete(user)
      db.session.commit()
      return '',200
    raise ValidatonError(status_code=404,error_code="UDEL01",error_message="User not Found")



    
#-----------------------------------------------------POST API---------------------------------------------------------------
class Post_api(Resource):
#---------------------------------------------------POST_GET_API-------------------------------------------------------------------
  @marshal_with(post_input_data)
  def get(self,title=None):
    post = Post.query.filter_by(title=title).first()
    if post == '':
      raise ValidatonError(status_code=404,error_code="PGET01",error_message="Post not found")
    return post

#---------------------------------------------------POST_POST_API-------------------------------------------------------------------
  @marshal_with(post_input_data)
  def post(self,title=None):
    input = newpost.parse_args()
    title = input.get('title',None)
    desc = input.get('desc',None)
    img = input.get('img',None)
    mimetype = input.get('mimetype',None)
    uid = input.get('uid',None)
    post = Post.query.filter_by(title=title).first()
    
    if post:
      raise ValidatonError(status_code=404,error_code="PPOST01",error_message="Post already exists,Try Another Username")
    if (title==""):
      raise ValidatonError(status_code=404,error_code="PPOST02",error_message="Title should not be empty")
    if (title ==" "):
      raise ValidatonError(status_code=404,error_code="PPOST03",error_message="Description is required")
      new_post = Post(title=title,desc=desc,img=img,mimetype=mimetype,uid=uid)
      db.session.add(new_post)
      db.session.commit()
      return new_post

#---------------------------------------------------POST_PUT_API-------------------------------------------------------------------
  @marshal_with(post_input_data)
  def put(self,title=None):
    post = Post.query.filter_by(title=title).first()
    if post is None:
      raise ValidatonError(status_code=404,error_code="VE200",error_message="Post not found")
    input = newpost.parse_args()
    title = input.get('title',None)
    desc = input.get('desc',None)
    img = input.get('img',None)
    mimetype = input.get('mimetype',None)
    if title:
      post.title = title
    if desc:
      post.description = desc
    if img:
      post.img = img
    if mimetype:
      post.mimetype = mimetype
      
    db.session.commit()
    return post


#---------------------------------------------------POST_DELEE_API-------------------------------------------------------------------
  @marshal_with(post_input_data)   
  def delete(self,title=None):
    post = Post.query.filter_by(title=title).first()
    if post:
      db.session.delete(post)
      db.session.commit()
      return ('',200)
    
    raise ValidatonError(status_code=404,error_code="VE200",error_message="Post not found")

api.add_resource(User_api,"/user/api","/user/api/<string:username>")
api.add_resource(Post_api,"/post/api","/post/api/<string:title>")
        