from django.db.models.functions import ExtractMonth
from django.db.models import F,Q
from .models import Category,Post
from .forms import SearchForm
import calendar





def extra(request ):
        categories=Category.objects.all()

      ##archive
        postmonth_list=[]
        postmonth_uniquelist=[]
        month_year_slug=[]
        posts=Post.objects.all().annotate(post_month=ExtractMonth('date'))
        

        for post in posts:
            post_months=calendar.month_name[post.post_month]
            postmonth_list.append(f'{post_months}-{post.date.year}')
        
        for x in postmonth_list:
                if x not in postmonth_uniquelist:
                     postmonth_uniquelist.append(x)

        



    ##search
        searchform=SearchForm()
        queryset=[]
        if 'query' in request.GET:
            searchform=SearchForm(request.GET)
            if searchform.is_valid():
                query_data=searchform.cleaned_data['query']
                print(query_data)
                querysets=Post.objects.filter(Q(category__title__contains=query_data) | 
                                                Q(tags__title__contains=query_data) | 
                                                Q(title__contains=query_data))

                queryset=querysets
                context=dict(
                     postss=queryset,
                     searchform=searchform
                     ) 
        
        context=dict(categories=categories,
                      months_years=postmonth_uniquelist,
                      searchform=searchform,
                       month_year_slug= month_year_slug
                     
                      )
        
        return context


