from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models.functions import ExtractMonth
from django.db.models import F,Value,Q
from django.template.defaultfilters import slugify
from django.http import Http404
from .models import Post,   Comment,Category
from .forms import CommentForm,UserForm,WritePostForm,SearchForm
import calendar


def error_404_view(request,exception):
    return render(request,'blog/404.html')

def starting_page(request):
        queryset=Post.objects.all().order_by('-date')[ :3]

        context=dict(
                     post=queryset
                     ) 

        return render(request,'blog/index.html',context)


def archive(request,month_years):
     
     posts=Post.objects.annotate(month=ExtractMonth('date') ,year=F('date'))
    
     for post in posts:
          post.month=calendar.month_name[post.month]
          post.year=post.date.year
          post.month_year=f'{post.month}-{post.year}'
          
          print(f'{post.month}{post.year}')
          
     for post in posts:
          print(post.month_year)
    #  posts_all=Post.objects.filter(month_year=month_years)

     queryset=[]
     for post in posts:
         if post.month_year==month_years:
              queryset.append(post)
          
        
     context=dict(posts=queryset,
                  month_year=month_years)             
     return render(request,'blog/archive.html',context)
     
        

def posts(request):
    queryset=Post.objects.all()
    paginator=Paginator(queryset,3) 
    page_number=request.GET.get('page')
    subqueryset=paginator.get_page(page_number)
    totalpages=paginator.num_pages

    totalpage=[ n+1 for n in range(totalpages)]
    
    context=dict(totalpages=totalpage,
                 post=subqueryset)

    return render(request,'blog/all-posts.html' ,context)



def signup_function(request):
    if request.method=='POST':
        form=UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'signup successful')
            return redirect('login')
        else:
            print(form.errors)
            context=dict(errors=form.errors,
                         form=form)
            return render(request ,'blog/signupform.html' ,context)


    else:
        signupform=UserForm()
        return render(request ,'blog/signupform.html',{'form':signupform})      




@login_required
def write_post(request):
    if request.method=='POST':
        postform=WritePostForm(request.POST, request.FILES)
        
        print(postform.__dict__)

        if postform.is_valid():
            title=postform.cleaned_data['title']
            form=postform.save(commit=False)
            form.author=request.user
            form.slug=slugify(title)
            
            print( form.__dict__)

            print(form.author)

            form.save()
            return redirect('posts-page')
        
        else:
             
            print(postform.errors)
            print('not saved') 
            # return redirect('write-post') 
            context=dict(form=postform)
            return render(request,'blog/writepost.html',context) 

    else:    
        postform=WritePostForm()
        context=dict(form=postform)
        return render(request,'blog/writepost.html',context)   
    




@login_required
def author_all_posts(request ,author):
    try:
        # post=Post.objects.get(pk=pk)
        # author=post.author
        queryset=Post.objects.filter(author__username=author)
    except Exception:
                return render(request,'blog/404.html')
    
    context=dict(queryset=queryset,
                    author=author)

    return render(request,'blog/author_all_post_beautiful.html' , context)
   

 
def post_detail(request,slugs):   
        if request.method=='POST':
            commentform=CommentForm(request.POST)
            
            print(commentform.__dict__)

            if commentform.is_valid():
                comment=commentform.save(commit=False)
                try:
                 
                   comment.post=Post.objects.get(slug=slugs)
                except Exception:
                  return render(request,'blog/404.html')
                
                if request.user.is_authenticated:
                   comment.email=request.user.email

                print(comment.__dict__)
                comment.save()
                return HttpResponseRedirect(reverse('post_detail', args=[slugs]))
            
            else:
                print(commentform.errors)
                return HttpResponse("error")    
            

        else:
            try:         
                post =Post.objects.get(slug=slugs)
                related_post=Post.objects.filter(category=post.category)  
                commentform=CommentForm()
                comment=Comment.objects.filter(post=post).order_by('-pk')
            
            except Exception:
                return render(request,'blog/404.html')
            context=dict(
                        post=post ,
                        form=commentform,
                        comments=comment,
                        related_post=related_post
                        )

            return render(request, 'blog/post_detail_beautiful.html' ,context)
    




def search(request):
        form=SearchForm()
        queryset=[]
        if 'query' in request.GET:
            form=SearchForm(request.GET)
            if form.is_valid():
                query_data=form.cleaned_data['query']
                print(query_data)
                querysets=Post.objects.filter(Q(category__title__contains=query_data) | 
                                                Q(tags__title__contains=query_data) | 
                                                Q(title__contains=query_data))

                queryset=querysets
                context=dict(
                     postss=queryset,
                     form=form
                     ) 
                return render(request,'blog/search_v2.html',context)

        

def category(request,category ):
   category=category
   posts=Post.objects.filter(category__title=category)

   context=dict(posts=posts,
                category=category)
   return render(request , 'blog/categorypost.html',context)


def basev2(request):
        queryset=Post.objects.all().order_by('-date')[ :5]

        context=dict(
                     post=queryset
                     ) 
      
        return render(request,'blog/home.html',context)
        




  
    
     


