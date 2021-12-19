from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
import random
import datetime
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///testdb.sqlite3" 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class user (db.Model):
  user_name = db.Column(db.String, primary_key = True ,nullable= False, unique=True)
  first_name = db.Column(db.String, nullable = False)
  last_name = db.Column(db.String)

class deck (db.Model):
  word_id=db. Column(db.Integer, primary_key = True, autoincrement = True)
  deck_name = db. Column(db.String, nullable = False)
  Word = db.Column(db.String, nullable= False, unique=True)
  Meaning = db.Column(db.String, nullable = False)
  last_access = db.Column(db.String, nullable = False)
  score = db.Column(db.Integer, nullable = False)
  user_id = db. Column(db.String, nullable=False)


db.create_all()

def datecalc():
  x = str(datetime.datetime.now())
  l=x.split(" ")
  return l[0]

def scorecalc(user,lang):
  data=deck.query.all()
  total=0
  count=0
  for i in data:
    if i.deck_name==lang and i.user_id==user:
      total+=i.score
      count+=1
  avg=total/count
  x = str(datetime.datetime.now())
  l=x.split(" ")
  x=l[0]
  if avg>=1 and avg<1.6:
    return "Low"
  elif avg>=1.5 and avg<2.5:
    return "Medium"
  elif avg>=2.5 and avg<=3:
    return "High"
  else:
    return "Scores Can't be calculated"
      

@app.route("/",methods =['GET','POST'])
def login():
  if request.method=="GET":
    return render_template("login.html")
  elif request.method=="POST":
    username = request.form['Username']
    data=user.query.all()
    l=[]
    for i in data:
      l.append(i.user_name)  
    if username not in l:
      return render_template("userdexist.html")
    returl="/dashboard/"+str(username)  
    return redirect(returl)

@app.route("/signup",methods =['GET','POST'])
def newacc():
  if request.method=="GET":
    return render_template("createacc.html")
  elif request.method=="POST":
    username = request.form['Username']   
    fname = request.form['f_name']
    lname = request.form['l_name']
    data=user.query.all()
    l=[]
    for i in data:
      l.append(i.user_name)  
    if username in l:
      return render_template("userexists.html")
    a = user(user_name=username,first_name=fname,last_name=lname)
    db.session.add(a)
    db.session.commit()
    return redirect("/")

@app.route("/dashboard/<string:userid>",methods =['GET','POST'])
def dashboard(userid):
  data=deck.query.all()
  data2=user.query.filter_by(user_name=userid).first()
  d=[]
  score=[]
  for i in data:
    if i.user_id==userid:
      a=scorecalc(userid,i.deck_name)
      x=[i.deck_name,i.last_access,a]
      if x in d:
        pass
      else:
        d.append(x)
  d.sort(key = lambda x: x[0])

  return render_template("dashboard.html",urladd=userid,first=data2.first_name,data=d)


@app.route("/profile/<string:userid>",methods =['GET','POST'])
def profile(userid):
  data=user.query.all()
  first=""
  last=""
  for i in data:
    if i.user_name==userid:
      useri=userid
      first=i.first_name
      last=i.last_name

  return render_template("profile.html",user=useri,first=first,last=last)


@app.route("/<string:userid>/card/<string:lang>",methods =['GET','POST'])
def card(userid,lang):
  scoredict={"Easy":3,"Medium":2,"Hard":1}
  data=deck.query.all()
  length=len(data)
  
  dict={}
  dlist=[]
  date=datecalc()
  for i in range(length):
    if data[i].deck_name==lang and data[i].user_id==userid:
      dict[i]=data[i]
      dlist.append(i)
      data[i].last_access=date

  db.session.commit()    
  a=random.randint(0,len(dlist)-1)
  x=dlist[a]
  word=dict[x].Word
  meaning=dict[x].Meaning
  if request.method=="GET":
    return render_template("card.html",urladd=userid,word=word,meaning=meaning,lang=lang)
  elif request.method=="POST":
    review = request.form['Review']
    new = deck.query.filter_by(Word=word).first()
    new.score = scoredict[review]
    db.session.commit()
    reurl="/"+str(userid)+"/card/"+str(lang)
    return redirect(reurl)

@app.route("/<string:userid>/crud/", methods = ['GET','POST'] )
def crud(userid):
  return render_template("crud.html",urladd=userid)

@app.route("/<string:userid>/crud/add", methods = ['GET','POST'] )
def add(userid):
  if request.method=="GET":
    return render_template("add.html",urladd=userid)
  elif request.method=="POST":
    Language = request.form['language']   
    Word = request.form['word']
    Meaning = request.form['meaning']
    data=deck.query.all()


    allwords=[]
    alllang=[]
    for i in data:
      tup=(i.deck_name,i.Word)
      allwords.append(tup)
      alllang.append(i.deck_name)
    if (Language,Word) in allwords:
      return render_template("exists.html",urladd=userid,data=Word)  
    else:
      if Language in alllang:
        newdata=deck.query.filter_by(deck_name=Language).first()
        a = deck(deck_name=Language,Word=Word,Meaning=Meaning, last_access=newdata.last_access, score=0,user_id=userid)
      else:
        a = deck(deck_name=Language,Word=Word,Meaning=Meaning, last_access="Never", score=0,user_id=userid)
      db.session.add(a)
      db.session.commit()

      return render_template("added.html",urladd=userid,data=Word)

### Debug update
@app.route("/<string:userid>/crud/<string:lang>/update/<string:word>", methods = ['GET','POST'] )
def update(userid,lang,word):
  data=deck.query.filter_by(user_id=userid,deck_name=lang,Word=word).first()
  if request.method=="GET": 
    return render_template("update.html",useri=userid, lang=lang, word=word, meaning=data.Meaning)  
  elif request.method=="POST":
    cword=request.form["cWord"]
    cmeaning=request.form["cMeaning"]
    data.Word=cword
    data.Meaning=cmeaning
    db.session.commit()
    redurl="/"+str(userid)+"/crud/delete_update"
    return redirect(redurl)

@app.route("/<string:userid>/added/<string:word>", methods = ['GET','POST'] )
def added(userid,word):
  return render_template("added.html",urladd=userid,data=word) 

@app.route("/<string:userid>/crud/delete_update", methods = ['GET','POST'] )
def delete_update(userid):
  d=deck.query.all()
  data=[]
  for i in d:
    a=[i.deck_name,i.Word,i.Meaning]
    data.append(a)

  data.sort(key = lambda x: x[0])  
  return render_template("deleteupdate.html",urladd=userid,data=data) 

@app.route("/<string:userid>/crud/<string:lang>/delete/<string:word>", methods = ['GET','POST'] )
def delete(userid,word,lang):
  a=deck.query.all()
  for i in a:
    if i.deck_name==lang and i.Word==word:
      db.session.delete(i)    #debug this later
      db.session.commit()
      break
  outstr="/"+str(userid)+"/crud/delete_update"
  return redirect(outstr)


@app.route("/<string:userid>/word_exists/<string:word>", methods = ['GET','POST'] )
def wordexist(userid,word):
  return render_template("exists.html",urladd=userid,data=word) 


@app.route("/profile/update/<string:userid>",methods = ['GET','POST'])
def update_profile(userid):
  d=user.query.filter_by(user_name=userid).first()
  if request.method=="GET": 
    return render_template("profileupdate.html",userid=userid, fn=d.first_name, ln=d.last_name)  
  elif request.method=="POST":
    fn=request.form["First_Name"]
    ln=request.form["Last_Name"]
    d.first_name=fn
    d.last_name=ln
    db.session.commit()
    print("debug")
    redurl="/profile/"+str(userid)
    print(redurl)
    return redirect(redurl)





#####  API  ####

api= Api(app) 


###parsers
login_parser=reqparse.RequestParser()
login_parser.add_argument('username')

signup_parser=reqparse.RequestParser()
signup_parser.add_argument('username')
signup_parser.add_argument('first_name')
signup_parser.add_argument('last_name')

card_parser=reqparse.RequestParser()
card_parser.add_argument('review')

add_parser=reqparse.RequestParser()
add_parser.add_argument('language')
add_parser.add_argument('word')
add_parser.add_argument('meaning')


class loginapi(Resource):
  def get(self):
    return {"Message": "Success"}, 200
  def post(self):
    args = login_parser.parse_args()
    username = args.get("username")
    data=user.query.all()
    l=[]
    for i in data:
      l.append(i.user_name)  
    if username not in l:
      return {"Message" :"User Doesn't Exist" }, 404
    return {"Message" : "Login Successful" }, 201

class signupapi(Resource):
  def get(self):
    return {"Message":"Success"},200
  def post(self):
    args = signup_parser.parse_args()
    username = args.get('username',None) 
    fname = args.get('first_name',None)
    lname = args.get('last_name',None)
    data=user.query.all()
    l=[]
    for i in data:
      l.append(i.user_name)  
    if username in l:
      return {"Message":"Username already exists"}
    a = user(user_name=username,first_name=fname,last_name=lname)
    db.session.add(a)
    db.session.commit()
    return {"username":username,"fname":fname,"lname":lname,"Message":"Successfully addded a new user"}, 201
  
class dashboardapi(Resource):
    def get(self,username):
        data=deck.query.all()
        d=[]
        score=[]
        for i in data:
            if i.user_id==username:
                a=scorecalc(username,i.deck_name)
                x=[i.deck_name,i.last_access,a]
                if x in d:
                    pass
                else:
                    d.append(x)
        d.sort(key = lambda x: x[0])
        l=[]
        for i in d:
          a="Language : "+str(i[0])+", Last Reviewed "+str(i[1])+", Score "+str(i[2])
          l.append(a)
        return {"urladd":username, "data":str(l)}    


class cardapi(Resource):
    def get(self,userid,lang):
        data=deck.query.all()
        length=len(data)
        
        dict={}
        dlist=[]
        date=datecalc()
        for i in range(length):
            if data[i].deck_name==lang and data[i].user_id==userid:
                dict[i]=data[i]
                dlist.append(i)
                data[i].last_access=date

        db.session.commit()    
        print(dlist)
        a=random.randint(0,len(dlist)-1)
        x=dlist[a]
        word=dict[x].Word
        meaning=dict[x].Meaning
        return {"urladd":userid,"word":word,"meaning":meaning,"lang":lang},200



class delete_updateapi(Resource):
    def get(self,userid):
        data=deck.query.filter_by(user_id=userid)     
        d={}
        for i in data: 
            d[i.user_id]=[i.deck_name,i.Word,i.Meaning,i.last_access,i.score]
        if d!={}:   
            return {"urladd":userid,"data":d}, 200
        else:
            return {"message": "No Word/deck Found"}, 404
    def delete(self,userid,lang,word):
      a=deck.query.all()
      for i in a:
        if i.deck_name==lang and i.Word==word:
          db.session.delete(i)    #debug this later
          db.session.commit()
          return  {"Message":"Successfully deleted"}, 200
      return {"Message":"word not found"},404
      


class profileapi(Resource):
    def get(self,userid):
        data=user.query.all()
        first=""
        last=""
        for i in data:
            if i.user_name==userid:
                useri=userid
                first=i.first_name
                last=i.last_name

        return {"user":useri,"first":first,"last":last}, 200


class updatewordapi(Resource):
    def get(self,userid,word,lang):
        data=deck.query.filter_by(Word=word, user_id=userid, deck_name=lang).first()
        return {"useri":userid, "lang":lang, "word":word, "meaning":data.Meaning},200

class updateprofileapi(Resource):
    def get(self,user_id):
        d=user.query.all()
        for data in d:
          if data.user_name==user_id:
            return {"useri":user_id, "f_name":data.first_name, "l_name":data.last_name},200

              
class addapi(Resource):
    def get(self,user_id):
      return {"urladd":user_id},200
    

 

####  API Resourse        
api.add_resource(loginapi, "/api/")
api.add_resource(signupapi, "/api/signup","/api/signup/<user>")
api.add_resource(dashboardapi,"/api/dashboard/<username>")
api.add_resource(cardapi,"/api/<userid>/card/<lang>")
api.add_resource(delete_updateapi,"/api/<userid>/crud/delete_update","/api/<userid>/crud/<lang>/delete/<word>")
api.add_resource(profileapi,"/api/profile/<userid>")
api.add_resource(updatewordapi,"/api/<userid>/crud/<lang>/update/<word>")
api.add_resource(updateprofileapi,"/api/profile/update/<user_id>")
api.add_resource(addapi,"/api/word/add/<user_id>")

if __name__ == '__main__':
  # Run the Flask app
  app.run(debug=True)  

