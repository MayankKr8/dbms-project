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
    context = {'expired':1}
    if request.user.is_authenticated:
        return HttpResponse(template.render(context,request))
    else:
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
      query = """ select * from help"""
      template = loader.get_template('myapp/help.html')
      cursor=connection.cursor() 
      cursor.execute(query)
      entries = []
      class help_db:
        def __init__(self,hid,aid,name,cont,email,stat,cntn):
            self.hid = hid
            self.aid = aid
            self.name = name
            self.cont = cont
            self.email = email
            self.stat = stat
            self.cntn = cntn
      for row in cursor:
            entries.append(help_db(row[0],row[1],row[2],row[3],row[4],row[5],row[6]))
      context = {'loggedin':0}
      context['products']=entries
      return HttpResponse(template.render(context,request))
def database(request):
      return render(request,'myapp/database.html',{})
def gallery(request):
      return render(request,'myapp/gallery.html',{})
def forum(request):
      query = """  select post_id,name,date,contents from post as a, admin as b where a.admin_id= b.admin_id;"""
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
      print(type(entries))
      entries.reverse()
      context = {'loggedin':0}
      context['products']=entries
      return HttpResponse(template.render(context,request))
def sponsor(request):
      return render(request,'myapp/sponsor.html',{})
def quiz(request):
      query = """ select * from quiz"""
      template = loader.get_template('myapp/quiz.html')
      cursor=connection.cursor() 
      cursor.execute(query)
      entries = []
      class quiz_db:
        def __init__(self,quid,marks,date,cmnts):
            self.quid = quid
            self.marks = marks
            self.date = date
            self.cmnts = cmnts
      for row in cursor:
            entries.append(quiz_db(row[0],row[1],row[2],row[3]))
      context = {'loggedin':0}
      context['products']=entries
      return HttpResponse(template.render(context,request))
def scores(request):
      template = loader.get_template('myapp/Scorecard.html')
      cursor=connection.cursor() 
      cursor.execute(""" select b.quiz_id, a.marks,a.date,b.marks,b.rank,a.comments from quiz as a right outer join evaluation as b on a.quiz_id=b.quiz_id where b.user_id=%s""",[request.user.id])
      entries = []
      class scores_db:
        def __init__(self,quid,marks,date,mark,rank,cmnts):
            self.quid = quid
            self.marks = marks
            self.date = date
            self.mark = mark
            self.rank = rank
            self.cmnts = cmnts
      for row in cursor:
            entries.append(scores_db(row[0],row[1],row[2],row[3],row[4],row[5]))
      context= {'loggedin':0}
      context['products']=entries
      return HttpResponse(template.render(context,request))
def create_user(request):
    username = request.POST.get('email', None)
    password = request.POST.get('psw', None)
    name = request.POST.get('name', None)
    email = request.POST.get('email', None)
    contact = request.POST.get('mobile', None)
    gender = request.POST.get('gender', None)
    Dept = request.POST.get('dpt', None)
    cursor=connection.cursor()
    cursor.execute("""select d_id from depart where name = %s""",[Dept])
    for row in cursor:
            d_id=row[0]
    year = request.POST.get('year', None)
    Interest = request.POST.get('Interest', None)
    Team = request.POST.get('t_id', None)
    template = loader.get_template('myapp/add_new_user.html')
    context = {'usercreated':0}
    context = {'usercreatedf':0}
    if username and password:
        user, created = User.objects.get_or_create(username=username, email=username)
        if created:
              user.set_password(password)
              user.save()
              cursor=connection.cursor()
              print(type(user.id))
              cursor.execute("""insert into  user (user_id, Team_id,name,gender,department,year,email,contact,interest)VALUES(%s,%s,%s, %s, %s,%s,%s,%s,%s)""",(user.id, int(Team), name, gender, d_id, int(year), email, int(contact), Interest ))
              context = {
                  'usercreated': 1,
                  }
              return HttpResponse(template.render(context,request))
        else:
              context = {
                  'usercreatedf': 1,
                  }
              
              return HttpResponse(template.render(context,request))
def remove_user1(request):
    username = request.POST.get('uname', None)
    template = loader.get_template('myapp/add_new_ctm.html')
    context = {'inserted':0}
    if username:
        user, created = User.objects.get_or_create(username=username, email=username)
        if created:
              cursor=connection.cursor() 
              cursor.execute("""delete from auth_user where username=%s""",[username])
              return HttpResponse("""<p style="font-size:50px;" >No username Associated</p>""")
        else:
              cursor=connection.cursor() 
              cursor.execute("""delete from auth_user where username=%s""",[username])
              context = {'inserted':1}
              return HttpResponse(template.render(context,request))            
def create_ctm(request):
      username = request.POST.get('uname', None)
      pos = request.POST.get('pos', None)
      template = loader.get_template('myapp/add_new_ctm.html')
      context = {'inserted':0}
      if username:
        user, created = User.objects.get_or_create(username=username, email=username)
        if created:
              cursor=connection.cursor() 
              cursor.execute("""delete from auth_user where username=%s""",[username])
              return HttpResponse("""<p style="font-size:50px;" >No username Associated</p>""")
        else:
              user.is_staff = True
              user.save()
              cursor=connection.cursor()
              cursor.execute("""select Team_id from user where user_id  = %s""",[user.id])
              for row in cursor:
                  tid  =  row[0]              
              cursor.execute("""insert into core_team(User_id,Team_id,position)VALUES(%s,%s,%s)""",(user.id,tid,pos))
              context = {'inserted':1}
              return HttpResponse(template.render(context,request))
def remove_ctm1(request):
      username = request.POST.get('uname', None)
      template = loader.get_template('myapp/add_new_ctm.html')
      context = {'inserted':0}
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
              cursor=connection.cursor() 
              cursor.execute("""delete from core_team where User_id  = %s""",[user.id])
              context = {'inserted':1}
              return HttpResponse(template.render(context,request))
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
      query = """ select user_id,b.name,a.name,gender,d.name,year,email,a.contact,interest from user as a, team as b, depart as d where a.Team_id =b.team_id and a.department = d.d_id"""
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
      comment = request.POST.get('cmmts', None)
      cursor=connection.cursor() 
      cursor.execute("""insert into  quiz (marks,date, comments)VALUES(%s, %s, %s)""",(marks,date,comment))
      return HttpResponseRedirect('/quiz/')

def add_eval(request):
      quiz_id = request.POST.get('qid', None)
      user_id = request.POST.get('u_id', None)
      marks = request.POST.get('marks', None)
      rank = request.POST.get('rank', None)
      template = loader.get_template('myapp/Scorecard.html')
      cursor=connection.cursor()
      context = {'inserted':1}
      cursor.execute("""insert into  evaluation (Quiz_id, User_id,marks, rank)VALUES(%s, %s, %s, %s)""",(quiz_id,user_id,marks,rank))
      return HttpResponse(template.render(context,request))
def submit_query(request):
      name = request.POST.get('name', None)
      email = request.POST.get('email', None)
      contact = request.POST.get('contact', None)
      query = request.POST.get('query', None)
      template = loader.get_template('myapp/contactus.html')
      cursor=connection.cursor() 
      cursor.execute("""insert into  help (name,contact,email,content)VALUES(%s, %s, %s, %s)""",(name,contact,email,query))
      context = {'inserted':1}
      return HttpResponse(template.render(context,request))
def update_help(request):
      hid = request.POST.get('id', None)
      stat = request.POST.get('status', None)
      aid = request.user.id
      print(stat)
      cursor=connection.cursor() 
      cursor.execute("""update help set status = %s, Admin_id = %s where help_id =%s""",(stat,aid,int(hid)))
      return HttpResponseRedirect('/help_portal/')
def create_post(request):
      pid = request.user.id
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
      rqst = request.user.id
      dop = request.POST.get('date', None)
      cursor=connection.cursor() 
      cursor.execute("""insert into orders(name,status,price,request,dop)VALUES( %s,%s,%s,%s,%s)""",(name,stat,int(price),rqst,dop))
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
      stat = "issued"
      iby = request.user.id
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
def pro(request):
      query = """select * from projects"""
      template = loader.get_template('myapp/Projects.html')
      cursor=connection.cursor() 
      cursor.execute(query)
      entries = []
      class contacts_db:
        def __init__(self,uid,name,team,price):
            self.uid = uid
            self.name = name
            self.team = team
            self.price = price
      for row in cursor:
            if(row[4]==0):
                  entries.append(contacts_db(row[0],row[1],row[2],row[3]))
      context = {'loggedin':0}
      if request.user.is_authenticated():
            context = {
                  'loggedin': 1,
            }
      context['products']=entries
      return HttpResponse(template.render(context,request))
def rec_fund(request):
      return render(request,'myapp/Fund_Record.html',{})
def add_fund(request):
      template = loader.get_template('myapp/Fund_Record.html')
      sid = request.POST.get('sid', None)
      pid = request.POST.get('pid', None)
      tid = request.POST.get('tid', None)
      cursor=connection.cursor() 
      cursor.execute(""" insert into transactions(sponser_id,status,ref_no,project_id)VALUES(%s,%s,%s,%s);""",(int(sid),2,int(tid),int(pid)))
      context = {'inserted':1}
      return HttpResponse(template.render(context,request))
def show_id(request):
      template = loader.get_template('myapp/profile.html')
      cursor=connection.cursor() 
      cursor.execute(""" select user_id,b.name,a.name,gender,d.name,year,email,a.contact,interest from user as a, team as b, depart as d where a.Team_id =b.team_id and a.department  = d.d_id and user_id=%s""",[request.user.id])
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

def profunds(request):
      query = """select trans_id,Sponser_id,stat,ref_no,Project_id from transactions,status_fund where status=stat_id"""
      template = loader.get_template('myapp/manage.html')
      cursor=connection.cursor() 
      cursor.execute(query)
      entries = []
      class contacts_db:
        def __init__(self,tid,sid,stat,ref,pro):
            self.tid = tid
            self.sid = sid
            self.stat = stat
            self.ref = ref
            self.pid = pro
      for row in cursor:
            entries.append(contacts_db(row[0],row[1],row[2],row[3],row[4]))
      context = {'loggedin':0}
      context['products']=entries
      return HttpResponse(template.render(context,request))
def add_proj1(request):
      name = request.POST.get('uname', None)
      tid = request.POST.get('pos', None)
      fund = request.POST.get('fund', None)
      template = loader.get_template('myapp/manage.html')
      cursor=connection.cursor() 
      cursor.execute(""" insert into projects(name,Team_id,fund,is_funded)VALUES(%s,%s,%s,0)""",(name,int(tid),int(fund)))
      context = {'inserted':1}
      return HttpResponse(template.render(context,request))
def remove_proj1(request):
      pid = request.POST.get('uname', None)
      template = loader.get_template('myapp/manage.html')
      cursor=connection.cursor() 
      cursor.execute(""" delete from projects where pro_id = %s""",[int(pid)])
      context = {'inserted':1}
      return HttpResponse(template.render(context,request))
def verfunds1(request):
      tid = request.POST.get('uname', None)
      template = loader.get_template('myapp/manage.html')
      cursor=connection.cursor()
      cursor.execute("""select Project_id from transactions where trans_id = %s""",[int(tid)])
      for row in cursor:
          pid = row[0]
      cursor.execute(""" update transactions set status = 3 where Project_id =%s""",[pid])
      cursor.execute(""" update transactions set status =1  where trans_id = %s""",[int(tid)])
      cursor.execute(""" update projects set is_funded = 1 where pro_id =%s""",[pid])
      context = {'inserted':1}
      query = """select trans_id,Sponser_id,stat,ref_no,Project_id from transactions,status_fund where status=stat_id"""
      cursor.execute(query)
      entries = []
      class contacts_db:
        def __init__(self,tid,sid,stat,ref,pro):
            self.tid = tid
            self.sid = sid
            self.stat = stat
            self.ref = ref
            self.pid = pro
      for row in cursor:
            entries.append(contacts_db(row[0],row[1],row[2],row[3],row[4]))
      context = {'loggedin':0}
      context['products']=entries
      return HttpResponse(template.render(context,request))
def reg_spo(request):
      return render(request,'myapp/Sponsor_registeration.html',{})
def add_sponsor(request):
      name = request.POST.get('uname', None)
      email = request.POST.get('email', None)
      des = request.POST.get('des', None)
      cont = request.POST.get('cont', None)
      template = loader.get_template('myapp/Sponsor_registeration.html')
      cursor=connection.cursor() 
      cursor.execute(""" insert into sponsor(name,description,contact,email)VALUES(%s,%s,%s,%s)""",(name,des,int(cont),email))
      context = {'logged':1}
      cursor.execute("""SELECT sponsor_id FROM sponsor ORDER BY sponsor_id DESC LIMIT 1""")
      for row in cursor:
            context = {'id':row[0]}
      return HttpResponse(template.render(context,request))
              
