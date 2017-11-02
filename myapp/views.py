from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.db import connection
from django.template import loader
from django.template import RequestContext
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
import datetime
# Create your views here.
def index(request):
    return render(request,'myapp/homepage.html',{})

def contactus(request):
    return render(request,'myapp/contactus.html',{})

def submitcontactus(request):
    print ("submit contact us")
    if request.method=='POST':
        data=request.POST
        print (data['email'],data['fname'],data['mobile'])
        cursor=connection.cursor()
        cursor.execute('''INSERT INTO contactus(fname,email,mobile,subject,query) VALUES(%s,%s,%s,%s,%s)''',(data['fname'].encode('utf-8'),data['email'].encode('utf-8'),data['mobile'].encode('utf-8'),data['subject'].encode('utf-8'),data['query'].encode('utf-8')))
        cursor.close()
        return HttpResponse("""<p style="font-size:50px;" >Form successfully submitted<br/>We will reach you soon :)</p>""")
def login_page(request):
    return render(request,'myapp/Login.html',{})
def login_handler(request):
    email = request.POST.get('uname', None)
    password = request.POST.get('psw', None)
    template = loader.get_template('myapp/Login.html')
    if email and password:
        user = authenticate(username=email, password=password)
        if user:
              login(request,user)
              return HttpResponseRedirect('/')
        else:
              context = {'notloggedin':1}
              return HttpResponse(template.render(context,request))
    else:
         context = {'notloggedin':1}
         return HttpResponse(template.render(context,request))

def logout_handler(request):
      logout(request)
      return HttpResponseRedirect('/')
def new_user(request):
      return render(request,'myapp/add_new_user.html',{})
def new_ctm(request):
      return render(request,'myapp/add_new_ctm.html',{})
def help_p(request):
      return render(request,'myapp/help.html',{})
def database(request):
      return render(request,'myapp/database.html',{})
def gallery(request):
      return render(request,'myapp/gallery.html',{})
def forum(request):
      query = """ select * from post"""
      template = loader.get_template('myapp/forum.html')
      cursor=connection.cursor() 
      cursor.execute(query)
      entries = []
      class post_db:
        def __init__(self,pid,aid,date,cont):
            self.pid = pid
            self.aid = aid
            self.date = date
            self.cont = cont
      for row in cursor:
            entries.append(post_db(row[0],row[1],row[2],row[3]))
      context = {'loggedin':0}
      context['products']=entries
      return HttpResponse(template.render(context,request))
def sponsor(request):
      return render(request,'myapp/sponsor.html',{})
def quiz(request):
      return render(request,'myapp/quiz.html',{})
def scores(request):
      return render(request,'myapp/Scorecard.html',{})
def create_user(request):
    username = request.POST.get('email', None)
    password = request.POST.get('psw', None)
    name = request.POST.get('name', None)
    email = request.POST.get('email', None)
    contact = request.POST.get('mobile', None)
    gender = request.POST.get('gender', None)
    Dept = request.POST.get('dpt', None)
    year = request.POST.get('year', None)
    Interest = request.POST.get('Interest', None)
    Team = request.POST.get('t_id', None)
    template = loader.get_template('myapp/add_new_user.html')
    context = {'usercreated':0}
    if username and password:
        user, created = User.objects.get_or_create(username=username, email=username)
        if created:
              user.set_password(password)
              user.save()
              cursor=connection.cursor()
              print(type(user.id))
              cursor.execute("""insert into  user (user_id, Team_id,name,gender,department,year,email,contact,interest)VALUES(%s,%s,%s, %s, %s,%s,%s,%s,%s)""",(user.id, int(Team), name, gender, Dept, int(year), email, int(contact), Interest ))
              context = {
                  'usercreated': 1,
                  }
              return HttpResponse(template.render(context,request))
        else:
               return HttpResponse(template.render(context,request))
def remove_user1(request):
    username = request.POST.get('uname', None)
    if username:
        user, created = User.objects.get_or_create(username=username, email=username)
        if created:
              cursor=connection.cursor() 
              cursor.execute("""delete from auth_user where username=%s""",[username])
              return HttpResponse("""<p style="font-size:50px;" >No username Associated</p>""")
        else:
              cursor=connection.cursor() 
              cursor.execute("""delete from auth_user where username=%s""",[username])
              return HttpResponseRedirect('/new_ctm/')            
def create_ctm(request):
      username = request.POST.get('uname', None)
      if username:
        user, created = User.objects.get_or_create(username=username, email=username)
        if created:
              cursor=connection.cursor() 
              cursor.execute("""delete from auth_user where username=%s""",[username])
              return HttpResponse("""<p style="font-size:50px;" >No username Associated</p>""")
        else:
              user.is_staff = True
              user.save()
              return HttpResponseRedirect('/new_ctm/')
def remove_ctm1(request):
      username = request.POST.get('uname', None)
      if username:
        user, created = User.objects.get_or_create(username=username, email=username)
        if created:
              cursor=connection.cursor() 
              cursor.execute("""delete from auth_user where username=%s""",[username])
              return HttpResponse("""<p style="font-size:50px;" >No username Associated</p>""")
        else:
              print("Debug")
              user.is_staff = False
              user.save()
              return HttpResponseRedirect('/new_ctm/')
def tools(request):
      query = """select a.tool_id,name,status,price,log_id,issued_by,issued_to,date_of_issue,date_of_return from tools as a left outer join issue_log as b on a.tool_id = b.Tool_id;"""
      template = loader.get_template('myapp/tools.html')
      cursor=connection.cursor() 
      cursor.execute(query)
      entries = []
      class tool_db:
        def __init__(self,tid,name,stat,price,lid,iby,ito,doi,dor):
            self.tid = tid
            self.name = name
            self.stat = stat
            self.price = price
            self.lid = lid
            self.iby = iby
            self.ito = ito
            self.doi = doi
            self.dor = dor
      for row in cursor:
            entries.append(tool_db(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8]))
      context = {'loggedin':0}
      if request.user.is_authenticated():
            context = {
                  'loggedin': 1,
                  'name': request.user.first_name,
            }
      context['products']=entries
      return HttpResponse(template.render(context,request))
def orders(request):
      query = """select * from orders"""
      template = loader.get_template('myapp/orders.html')
      cursor=connection.cursor() 
      cursor.execute(query)
      entries = []
      class orders_db:
        def __init__(self,name,status,price,rqst,dop):
            self.name = name
            self.status = status
            self.price = price
            self.rqst = rqst
            self.dop = dop
      for row in cursor:
            entries.append(orders_db(row[0],row[1],row[2],row[3],row[4]))
      context = {'loggedin':0}
      if request.user.is_authenticated():
            context = {
                  'loggedin': 1,
                  'name': request.user.first_name,
            }
      context['products']=entries
      return HttpResponse(template.render(context,request))
def contacts(request):
      query = """select * from contacts"""
      template = loader.get_template('myapp/contact.html')
      cursor=connection.cursor() 
      cursor.execute(query)
      entries = []
      class contacts_db:
        def __init__(self,name,contact,email,post,Inst):
            self.name = name
            self.contact = contact
            self.email = email
            self.post = post
            self.Inst = Inst
      for row in cursor:
            entries.append(contacts_db(row[0],row[1],row[2],row[3],row[4]))
      context = {'loggedin':0}
      if request.user.is_authenticated():
            context = {
                  'loggedin': 1,
            }
      context['products']=entries
      return HttpResponse(template.render(context,request))
def users(request):
      query = """ select user_id,b.name,a.name,gender,department,year,email,a.contact,interest from user as a, team as b where a.Team_id =b.team_id"""
      template = loader.get_template('myapp/users.html')
      cursor=connection.cursor() 
      cursor.execute(query)
      entries = []
      class users_db:
        def __init__(self,uid,name,team,gender,depart,year,cont,email,inter):
            self.uid = uid
            self.name = name
            self.username = email
            self.team = team
            self.gender = gender
            self.depart = depart
            self.year = year
            self.cont = cont
            self.email = email
            self.inter = inter
      for row in cursor:
            entries.append(users_db(row[0],row[2],row[1],row[3],row[4],row[5],row[7],row[6],row[8]))
      context = {'loggedin':0}
      if request.user.is_authenticated():
            context = {
                  'loggedin': 1,
                  'name': request.user.first_name,
            }
      context['products']=entries
      return HttpResponse(template.render(context,request))
      return render(request,'myapp/users.html',{})
def add_quizs(request):
      marks = request.POST.get('marks', None)
      date = request.POST.get('date', None)
      comment = request.POST.get('cmmnts', None)
      cursor=connection.cursor() 
      cursor.execute("""insert into  quiz (marks,date, comments)VALUES(%s, %s, %s)""",(marks,date,comment))
      return HttpResponseRedirect('/quiz/')

def add_eval(request):
      quiz_id = request.POST.get('qid', None)
      user_id = request.POST.get('u_id', None)
      marks = request.POST.get('marks', None)
      rank = request.POST.get('rank', None)
      cursor=connection.cursor() 
      cursor.execute("""insert into  evaluation (Quiz_id, User_id,marks, rank)VALUES(%s, %s, %s, %s)""",(quiz_id,user_id,marks,rank))
      return HttpResponseRedirect('/quiz/')
def submit_query(request):
      name = request.POST.get('name', None)
      email = request.POST.get('email', None)
      contact = request.POST.get('contact', None)
      query = request.POST.get('query', None)
      cursor=connection.cursor() 
      cursor.execute("""insert into  help (name,contact,email,content)VALUES(%s, %s, %s, %s)""",(name,contact,email,query))
      return HttpResponseRedirect('/contactus/')
def update_help(request):
      hid = request.POST.get('id', None)
      stat = request.POST.get('Status', None)
      aid = request.POST.get('aid', None)
      cursor=connection.cursor() 
      cursor.execute("""update help set status = %s, Admin_id = %s""",(stat,int(aid)))
      return HttpResponseRedirect('/help_portal/')
def create_post(request):
      pid = request.POST.get('Id', None)
      date = request.POST.get('date', None)
      post = request.POST.get('pst', None)
      cursor=connection.cursor() 
      cursor.execute("""insert into post(Admin_id,date,contents)VALUES( %s,%s,%s)""",(int(pid),date,post))
      return HttpResponseRedirect('/forum/')
def add_contact(request):
      name = request.POST.get('name', None)
      cnt = request.POST.get('cont', None)
      email = request.POST.get('email', None)
      pos = request.POST.get('pos', None)
      inst = request.POST.get('inst', None)
      cursor=connection.cursor() 
      cursor.execute("""insert into contacts(name,contact,email,position,institute)VALUES( %s,%s,%s,%s,%s)""",(name,int(cnt),email,pos,inst))
      return HttpResponseRedirect('/contacts/')
def add_order(request):
      name = request.POST.get('name', None)
      stat = request.POST.get('stat', None)
      price = request.POST.get('price', None)
      rqst = request.POST.get('r_id', None)
      dop = request.POST.get('date', None)
      cursor=connection.cursor() 
      cursor.execute("""insert into orders(name,status,price,request,dop)VALUES( %s,%s,%s,%s,%s)""",(name,stat,int(price),int(rqst),dop))
      return HttpResponseRedirect('/orders/')
def add_tool(request):
      name = request.POST.get('name', None)
      stat = request.POST.get('stat', None)
      price = request.POST.get('price', None)
      cursor=connection.cursor() 
      cursor.execute("""insert into tools(name,status,price)VALUES( %s,%s,%s)""",(name,stat,int(price)))
      return HttpResponseRedirect('/tools/')
def issue_tool(request):
      tid = request.POST.get('id', None)
      stat = request.POST.get('stat', None)
      iby = request.POST.get('iby', None)
      ito = request.POST.get('ito', None)
      date = request.POST.get('date', None)
      cursor=connection.cursor() 
      cursor.execute("""insert into issue_log(Tool_id,issued_by,issued_to,date_of_issue)VALUES( %s,%s,%s,%s)""",(tid,int(iby),int(ito),date))
      cursor.execute("""update tools set status = %s where tool_id = %s""",(stat,int(tid)))
      return HttpResponseRedirect('/tools/')
def return_tool(request):
      lid = request.POST.get('name', None)
      stat = request.POST.get('stat', None)
      date = request.POST.get('date', None)
      cursor=connection.cursor() 
      cursor.execute("""update issue_log set date_of_return = %s where log_id = %s""",(date,int(lid)))
      return HttpResponseRedirect('/tools/')

              
              
