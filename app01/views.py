from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template.context import RequestContext
from django.contrib import comments
from django.contrib.contenttypes.models import ContentType

import models


# Create your views here.
def index(request,category_id=None):
    bbs_list = models.BBS.objects.all()
    category = models.Category.objects.all()
    if category_id:
        category_bbs_list = models.BBS.objects.filter(category__id=category_id)
#       Take care here.Why we use filter() and not get()?
#       Because the get() function can only get one BBS, which means that
#       it well raise error once the return BBS more than one.So, we use filter.
        return render_to_response('index.html',
                              {
                               'bbs_list':category_bbs_list,
                               'user':request.user,
                               'bbs_category':category,
                               'request_category_id':int(category_id)
                               }
                                  )
        
    return render_to_response('index.html',
                              {
                               'bbs_list':bbs_list,
                               'user':request.user,
                               'bbs_category':category
                               }
    )

def bbs_detial(request,bbs_id):
    bbs = models.BBS.objects.get(id=bbs_id)
    category = models.Category.objects.all()
    return render_to_response(
                              'bbs_detail.html',
                              {'bbs_obj':bbs,
                               'bbs_category':category,
                               'user':request.user},
                              context_instance=RequestContext(request)
    )

@login_required
def sub_comment(request):
    print request.POST
    bbs_id = request.POST.get('bbs_id')
    content_type_obj = ContentType.objects.get(id=7) 
#     Get the instance of the commented table,here is the BBS table.
#     To understant this, you must know that the comments table 
#     use the ContentType table to relate the BBS table, 
#     so that the comment cat add comment for many table. 
#     I suggest that you should enter the database to make youself understant it.
    print type(request.user)
    comment = request.POST.get('comment_content')
    comments.models.Comment.objects.create(
                           content_type=content_type_obj, 
                           #The foreign key of the content-type table.
                           #And this must be a models instance.
                           site_id = 1,    #This must be added to soove the version problem.
                           user = request.user, #The foreign key of the user table.
                           comment = comment, #The comemnt added by the user.
                           object_pk = bbs_id,
#                            object_pk is the bbs tiezi id, and it is bbs_id,this is very important,
#                            or the comment is just for the bbs table, but not for any tiezi.
#                            So it won't be showed on any tiezi on our bbs.Adding it!
#                            I suggest you to read the source code ot the comments models.
    )
    return HttpResponseRedirect('/detail/%s' % bbs_id)

@login_required
def bbs_sub(request):
    content = request.POST.get('content')
    author = models.BBS_user.objects.get(user__username=request.user)
    #To get from foreign key table, you must use it like user__username.
    models.BBS.objects.create(
            title = 'TEST TITLE',
            summary = 'HAHA',
            content = content,
            author = author,
            view_count = 1,
            ranking = 1,
    ) 
    return HttpResponse('yes.')

@login_required
def bbs_pub(request):
    category = models.Category.objects.all()
    return render_to_response('bbs_pub.html',
                              {'bbs_category':category},
                              context_instance=RequestContext(request))


@login_required
def Home_page(request):
    Login_user = request.user
    return render_to_response('home.html',{'user':Login_user})

@login_required
def logout_view(request):
    Login_user = request.user
    auth.logout(request)
    return HttpResponseRedirect('/')

def Login(request):
    category = models.Category.objects.all()
    #request.user will return the user's name who has logined in the system.
    #In the Django, it means the the function of "auth.login(request,user)" has been run.
    #Or request.user will return AnonymousUser.You will see this at the debug follow.
    Login_user = request.user
    if request.method == 'POST':
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        check_user = request.user.is_authenticated()
        user = auth.authenticate(username=username,password=password)
        print username,password
        if user is not None:
            Login_user = request.user
            auth.login(request, user)
            Login_user = request.user
            return HttpResponseRedirect('/')
        else:
            return render_to_response('login.html', 
                                      {
                                       'login_err':'Wrong username or password.',
                                       'bbs_category':category
                                       },
                                      context_instance=RequestContext(request))
    return render_to_response('login.html',
                              {
                               'login_err':'',
                               'bbs_category':category,
                               },
                              context_instance=RequestContext(request))
    
