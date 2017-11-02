"""my_dbms_website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from myapp import views

urlpatterns = [
    url(r'^$',views.index, name='index'),
    url(r'contactus/$',views.contactus,name="contact"),
    url(r'login/$',views.login_page,name="log in page"),
    url(r'logout/$',views.logout_handler,name="logout"),
    url(r'login_handler/$',views.login_handler,name="login"),
    url(r'new_user/$',views.new_user,name="new_user"),
    url(r'new_ctm/$',views.new_ctm,name="new_ctm"),
    url(r'help_portal/$',views.help_p,name="help"),
    url(r'database/$',views.database,name="database"),
    url(r'gallery/$',views.gallery,name="gallery"),
    url(r'forum/$',views.forum,name="forum"),
    url(r'sponsor/$',views.sponsor,name="sponsor"),
    url(r'quiz/$',views.quiz,name="quiz"),
    url(r'scores/$',views.scores,name="scores"),
    url(r'create_user/$',views.create_user,name="new_user"),
    url(r'remove_user1/$',views.remove_user1,name="notuser"),
    url(r'create_ctm/$',views.create_ctm,name="ctm"),
    url(r'remove_ctm1/$',views.remove_ctm1,name="notctm"),
    url(r'tools/$',views.tools,name="tools"),
    url(r'orders/$',views.orders,name="orders"),
    url(r'contacts/$',views.contacts,name="contacts"),
    url(r'users/$',views.users,name="user_list"),
    url(r'add_quizs/$',views.add_quizs,name="new_quiz"),
    url(r'add_eval/$',views.add_eval,name="add_eval"),
    url(r'submit_query/$',views.submit_query,name="queries_submit"),
    url(r'update_help/$',views.update_help,name="update_help"),
    url(r'create_post/$',views.create_post,name="create_post"),
    url(r'add_contact/$',views.add_contact,name="add_contact"),
    url(r'add_orderse/$',views.add_order,name="add_order"),
    url(r'add_tool1/$',views.add_tool,name="add_tool"),
    url(r'tool_issue/$',views.issue_tool,name="tool issue"),
    url(r'reg_spo/$',views.reg_spo,name="refspo"),
    url(r'pro_jects/$',views.pro,name="projectx"),
    url(r'rec_fund/$',views.rec_fund,name="fund"),
    url(r'tool_return/$',views.return_tool,name="ool return"),
    url(r'add_funds/$',views.add_fund,name="add fund"),
    url(r'show_id/$',views.show_id,name="ds fund"),
    url(r'profunds/$',views.profunds,name="dsk fund"),
    url(r'add_proj1/$',views.add_proj1,name="add fund"),
    url(r'remove_proj1/$',views.remove_proj1,name="ds fund"),
    url(r'verfunds1/$',views.verfunds1,name="dsk fund"),
    url(r'add_sponsor1/$',views.add_sponsor,name="dsk5 fund"),
    
    
]
