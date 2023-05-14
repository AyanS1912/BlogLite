from flask import request,render_template
from flask import current_app as app
from flask import url_for,redirect,flash,Response
from flask_login import LoginManager,login_required,login_user
from flask_login import current_user,logout_user

from application.database import db
from application.models import User,Post,Comment,Like,Follow

login_manager = LoginManager()
login_manager.init_app(app)
  
@login_manager.user_loader
def load_user(id):
  return User.query.get(id)

###=------------------------------------------------------------------------LOGIN/SIGNUP-----------------------------------------------------------------------------------------------------------
  
@app.route("/")
def login():
  return render_template("/auth/login.html")


@app.route("/register")
def register():
  return render_template("/auth/register.html")

@app.route("/register/successful",methods=["GET","POST"])
def registration_done_successfully():
  if request.method == "POST":
    new_name = request.form.get('name')
    new_username = request.form.get('username')
    new_password = request.form.get('password')
    image = open('static/default.png','rb').read()
      
    uname_available = db.session.query(User).filter(User.username == new_username).first()
      
    if uname_available:
      flash("Username already exist",category='error')
 
    else:
      user = User(name= new_name,username= new_username, password=new_password,profile_pic=image,mimetype='image/png')
      db.session.add(user)      
      db.session.commit()
      flash("Registration Successful")
        
  return render_template("/auth/register.html")


@app.route("/login/success", methods=["GET", "POST"])
def login_success():
  if request.method == "POST":
    username = request.form.get('username')
    password = request.form.get('password')
    checkuser = User.query.filter_by(username=username).first()
    

    if checkuser:
      if (checkuser.password == password):
        login_user(checkuser,remember=True)
        return redirect(url_for('home_page'))
      else:
        flash('Wrong Password.Try Again!', category='error')
      
    else:
      flash("User Doesn't exist", category='error')
      
    
  return redirect(url_for("login"))

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
  logout_user()
  return redirect(url_for("login"))


###=------------------------------------------------------------------------LOGIN/SIGNUP-----------------------------------------------------------------------------------------------------------

  
###------------------------------------------------------------------------POST--------------------------------------------------------------------------------------------------------------------

@app.route('/post/create' ,methods=["GET", "POST"])
@login_required
def new_post():
  if request.method =='POST':
    form =request.form
    post_title = form.get('title')
    post_desc = form.get('desc')
    post_img = request.files['img']
    mimetype = post_img.mimetype
    posts = Post(title=post_title,desc=post_desc,img=post_img.read(),mimetype=mimetype,uid=current_user.id)
    db.session.add(posts)
    db.session.commit()
    flash("New Post Uploaded",category='success')

  return render_template("add_post.html")


###------------------------------------------------------------------------POSTImage--------------------------------------------------------------------------------------------------------------------
@app.route('/post/get_image/<int:id>')
@login_required
def get_post(id):
  post=db.session.query(Post).filter(Post.id ==id).first()
  return  Response(post.img,mimetype=post.mimetype)

###------------------------------------------------------------------------POST_update--------------------------------------------------------------------------------------------------------------------
@app.route('/post/update/<int:id>',methods=['GET','POST'])
@login_required
def update_post(id):
  post = Post.query.filter_by(id=id).first()

  if request.method == 'POST':
    title = request.form.get('title')
    desc = request.form.get('desc')
    img = request.files['img']
    mimetype = img.mimetype
    
    post.title = title
    post.desc = desc
    post.img = img.read()
    post.mimetype = mimetype
    db.session.commit()
    flash('Post has Been Update Successfully',category='success')
  return render_template('updatepost.html',post=post)
  


###------------------------------------------------------------------------POST_delete--------------------------------------------------------------------------------------------------------------------
@app.route('/post/delete/<int:id>')
@login_required
def delete_post(id):
  deletepost = Post.query.filter_by(id=id).first()

  if current_user.id == deletepost.user.id  :
    db.session.delete(deletepost)
    db.session.commit()
    flash("Post Was Deleted!",category='success')

  else:
    flash("You Aren't Authorized To Delete That Post")

  return redirect(url_for("home_page"))

###------------------------------------------------------------------------HOME--------------------------------------------------------------------------------------------------------------------

@app.route('/home' ,methods=["GET", "POST"])
@login_required
def home_page():
  posts = Post.query.order_by(Post.post_date)
  return render_template("home.html",posts=posts,user=current_user)

###------------------------------------------------------------------------Profile--------------------------------------------------------------------------------------------------------------------
@app.route('/home/profile/<string:username>' ,methods=["GET", "POST"])
@login_required
def my_profile(username):
  user = User.query.filter_by(username=username).first()
  posts = Post.query.filter_by(uid=user.id).all()
  followers = Follow.query.filter_by(follower_id=user.id).all()
  followings = Follow.query.filter_by(uid=user.id).all()
  return render_template("profilepage.html",user=user,posts=posts,following=followings,follower=followers)




@app.route("/home/other_profile/<string:username>",methods=['GET','POST'])
@login_required
def other_profile(username):
  users = User.query.filter_by(username=username).first()
  posts = Post.query.filter_by(uid=users.id).all()
  followers = Follow.query.filter_by(follower_id=users.id).all()
  followings = Follow.query.filter_by(uid=users.id).all()
  return render_template("profile.html",users=users,posts=posts,following=followings,follower=followers)


###------------------------------------------------------------------------Profile_img--------------------------------------------------------------------------------------------------------------------
@app.route('/profile/get_image/<int:id>')
@login_required
def get_profile_pic(id):
  user =db.session.query(User).filter(User.id == id).first()
  return  Response(user.profile_pic,mimetype=user.mimetype)

###------------------------------------------------------------------------Profile_update------------------------------------------------------------------------------------------------------------
@app.route("/profile/update/<int:id>",methods=['GET','POST'])
@login_required
def updateuser(id):

  if request.method=='POST':
    new_name = request.form.get('name')
    new_username = request.form.get('username')
    new_profilepic= request.files['profile_pic']
    mimetype = new_profilepic.mimetype

    current_user.name= new_name
    current_user.username= new_username
    current_user.profile_pic=new_profilepic.read()
    current_user.mimetype =mimetype
    db.session.commit()
    flash('Profile has Been Update Successfully',category='success')
  return render_template('editprofile.html')

###------------------------------------------------------------------------Profile_delete-------------------------------------------------------------------------------------------------------------  
@app.route('/profile/delete/<int:id>')
@login_required
def deleteuser(id):
  
  if id == current_user.id:
    delete_user = User.query.get(id)
    db.session.delete(delete_user)
    db.session.commit()
    flash("User Deleted Successfully!!")
    return redirect(url_for('register'))
  
  else:
    flash("You're not authorised to delete the user ")
  
  return redirect(url_for('home_page'))
    
#---------------------------Follow/Unfollow-----------------------------------------------------###--------------------------------------------------------------------
    
@app.route("/follow/<int:id>",methods=['GET','POST'])
@login_required
def follow(id):
  user = User.query.filter(User.id==id).first()
  users = Follow(uid=current_user.id,follower_id=id)
  db.session.add(users)
  db.session.commit()
  return redirect(url_for('home_page'))

@app.route("/unfollow/<int:id>",methods=['GET','POST'])
@login_required
def unfollow(id):
  users = Follow.query.filter_by(uid=current_user.id,follower_id=id).first()
  db.session.delete(users)
  db.session.commit()
  return redirect(url_for('home_page'))
#---------------------------Like-----------------------------------------------------

@app.route('/post/like/<int:pid>',methods=['GET'])
@login_required
def like(pid):
  post = Post.query.filter_by(id=pid)
  likes = Like.query.filter_by(pid=pid,uid=current_user.id).first()

  if not post:
    flash("Post doesn't exist",category='error')
  else:
    if likes:
      db.session.delete(likes)
      db.session.commit()
    else:
      likes = Like(pid=pid,uid=current_user.id)
      db.session.add(likes)
      db.session.commit()

  return redirect(url_for('home_page'))

    


#---------------------------Comment-----------------------------------------------------#--------------------------------------------------------------------------------
    
@app.route('/post/comment/<int:pid>',methods=['POST'])
@login_required
def add_comment(pid):
  comment=request.form.get('comment')

  if comment is None:
    flash("Enter some comment",category='error')

  else :
    post = Post.query.filter_by(id=pid)
    if post:
      comments = Comment(uid=current_user.id,pid=pid,comment=comment)
      db.session.add(comments)
      db.session.commit()
      flash("Comment Posted Successfully",category='success')
    
    else:
      flash('Post does\'t exist',category='error')

  return redirect(url_for('home_page'))

#---------------------------Comment_delete-----------------------------------------------------#--------------------------------------------------------------------------------

@app.route('/comment/delete/<int:comm_id>')
@login_required
def delete_comment(comm_id):
  comment = Comment.query.filter_by(comm_id=comm_id).first()
  
  if comment is None:
    flash("Comment doesn't exist",category='error')
  else:
    if(current_user.id == comment.user.id or  current_user.id == comment.post.uid):
      db.session.delete(comment)
      db.session.commit()
    else:
      flash("You are not authorised to delete the comment",category='error')

  return redirect(url_for('home_page'))
      
#------------------------------------Search------------------------------------------------------------------------------------------------------------------------------------
@app.route("/search",methods=['GET','POST'])
@login_required
def search():
  users = User.query
  data = request.form.get('search')
  if data is None:
    flash("Enter Username to Search",category='error')
  users = users.filter(User.username.like('%' + data+ '%'))
  users = users.order_by(User.username).all()
  
  return render_template("search.html",users=users,search=data)

#----------------------------------------------------------------------------Unauthorised USer----#--------------------------------------------------------------------------------
@login_manager.unauthorized_handler
def unauthorized():
  flash("You're not authorised.Please login for further access to site.")
  return redirect(url_for('login'))

