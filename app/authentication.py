from app import app
import os
import json
from authlib.integrations.flask_client import OAuth
from app.database import *
from app.temp import *
from flask_restful import Resource,Api
import pandas as pd
#from temp import 
class Token(Resource):
    def get(self):
        return {'session':session.get('email',None)},200

class Getting_data(Resource):
    def post(self):
        tt=None
        k=request.get_json()
        if f'{k["sess"]}.txt' in os.listdir('app'):
            with open(f'app/{k["sess"]}.txt','r') as f:
                tt=f.read()
        else:
            os.system(f'touch app/{k["sess"]}.txt');
            
        if tt is not None:
            linker=json.loads(tt)
        else:
            linker=[]
        HG=Drank.query.filter_by(email=k['sess']).first()
        hg=json.loads(HG.links)
        for i in json.loads(k['data']):
            if i not in hg:
                hg.append(i)

        HG.links=json.dumps(hg)
        db.session.add(HG)
        db.session.commit()

        linker.extend(json.loads(k['data']))
        with open(f'app/{k["sess"]}.txt','w') as f:
            f.write(json.dumps(linker))

        return {'ok':'done'},200
# OAuth registration 
@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

oauth=OAuth(app)
google = oauth.register(
    name='google',
    client_id='',
    client_secret='',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    redirect_uri='http://localhost:5000/google/register',
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo', 
    client_kwargs={'scope': 'openid email profile'},
)


@app.route('/login',methods=["GET","POST"])
def Login():
        if session.get('email',None)!=None:
                return redirect(url_for('home'))
        if request.method=="POST":
                user_auth=Drank.query.filter_by(email=request.form["email"]).first()
                if user_auth:
                        if request.form["password"]==user_auth.password:
                                session["email"]=user_auth.email
                                session["username"]=user_auth.username
                                A=user_auth.links
                                A=json.loads(A)
                                for i in A:
                                        print(i)
                                flash("You are successfully logged in")
                                return redirect(url_for("home"))
                        else:
                                flash("Wrong password")
                                return redirect(url_for('Login'))
                else:
                        flash("You have to sign in first")
                        return redirect(url_for('Register'))
                
                
                
        return render_template('Auth/login.html')
                

@app.route('/register', methods=["GET","POST"])
def Register():
        if request.method=="POST":
                data=request.form["username"]
                g=Drank.query.filter_by(email=request.form["email"]).first()
                k=Drank.query.filter_by(username=request.form["username"]).first()
                if g or k:
                        flash("Account already exists")
                        return redirect(url_for("Register"))
                
                ## Have to be removed while production ##
                Lists=[];
                ser=json.dumps(Lists)
                print(ser)
                
                user=Drank(username=request.form["username"],email=request.form["email"],password=request.form["password"],links=ser)
                db.session.add(user)
                db.session.commit()
                print(data)
                try:
                        return redirect(url_for("home"))
                except:
                        return redirect('/login')
        return render_template('Auth/register.html')
@app.route('/logout')
def Logout():
        session['email']=None
        session["username"]=None
        return redirect(url_for('Login'))
@app.route('/register_google')
def OauthG():
        gg=oauth.create_client('google')
        print(gg)
        redirect_uri=url_for('RegisterOauth',_external=True)
        return gg.authorize_redirect(redirect_uri)

@app.route('/google/register')
def RegisterOauth():
        gg=oauth.create_client('google')
        token=google.authorize_access_token()
        resp=google.get('userinfo')
        user_info=resp.json()
        user=oauth.google.userinfo()
        email=user_info["email"]
        username=user_info["name"]
        password=user_info["id"]
        b=Drank.query.filter_by(email=email).first()
        if b:
                session["email"]=email
                session['username']=username
                flash("You are successfully signed in")
                return redirect(url_for('home'))
        else:
                user=Drank(username=username,email=email,password=password,gid=password)
                db.session.add(user)
                db.session.commit()
                session["email"]=email
                session["username"]=username
                flash("You account is successfully created")
                return redirect(url_for('home'))
        
        
        return redirect('/')
        

@app.route('/plan')
def Plan():
        return '<h1><center> Payment Gateway Page </center></h1>'


@app.route('/getfirst')
def GFL():
    #ff=pd.read_excel(os.path.join(path,'A.xlsx'),engine='openpyxl')
    #master=pd.read_excel(os.path.join(path,'Newdata.xlsx'),engine='openpyxl')
    g=Drank.query.filter_by(email=session.get('email')).first()
    H=g.links
    #print(H)
    print(H)
    print('Reached')
    H=json.loads(H)
    A=[]
    B=[]
    #print(H)
    for i in H:
        A.append(i)
        print(i,checker(i))
        B.append(checker(i))
    
    frame=pd.DataFrame({'Links':A,'Lines':B})
    print("ok",frame)
    if 'A.xlsxx' not in os.listdir():
         os.system('touch A.xlsx')
    frame.to_excel('A.xlsx',index=False)
    return send_file('../A.xlsx',as_attachment=False)




@app.route('/add_links')
def Link():
    if session.get('email',None) ==  None:
        return redirect(url_for('Login'))
    else:
        b=Drank.query.filter_by(email=session.get('email')).first()
        with open(f'app/{session.get("email")}.txt','r') as g:
            tt=g.read()
       # print('Linker',tt)
        cond=json.loads(tt)
        #print(cond[-1])
        if checker(cond[-1]) == None:
            print(cond[-1])
           # return redirect(url_for('warn'))
        zulu= b.links
        zulu=json.loads(zulu)
        fop=True
        pppp=[]
        for i in cond:
            if i not in zulu:
                fop=False
                zulu.append(i)

        if fop == False:
            zulu=json.dumps(zulu)
            b.links=zulu;
        #print(b.email,b.links)
            db.session.add(b);
            db.session.commit();
            print('Link are added');
    return redirect(url_for('GFL'));

@app.route('/cond')
def warn():
    return '<h1> Your Lines have not finished yet come back later after an hour may be :)'
api=Api(app)
api.add_resource(Token,'/token')
api.add_resource(Getting_data,'/linker')
