from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
from django.contrib import messages
from .models import Comment, Movie , Review , Favorite
from .models import Profile 
from django.views.generic import ListView,DetailView,CreateView
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.views import LogoutView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ReviewForm,CommentForm
from django.db.models import Avg


class MovieListView(ListView):
    model = Movie
    template_name = "prj/movie_list.html"  
    context_object_name = "movies"         
    ordering_by=['-release_year']
    paginate_by= 3

    def get_queryset(self):
        movies = Movie.objects.all()       
        search_title = self.request.GET.get('q')
        search_genre = self.request.GET.get('genre')
        if search_title:
         movies = movies.filter(title__icontains=search_title)
        
        if search_genre:
         movies = movies.filter(genre__icontains=search_genre)

        return movies
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_title'] = self.request.GET.get('q', '')
        return context

    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       context['search_genre'] = self.request.GET.get('genre', '')
       return context
    
    
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        return context
   
class GenreMoviesView(ListView):
    template_name = "prj/genre.html"  
    context_object_name = "movies"
    paginate_by = 3

    def get_queryset(self):
        genre_name = self.kwargs['genre']
        return Movie.objects.filter(genre__icontains=genre_name)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genre'] = self.kwargs['genre']
        return context

class MovieDetailView(DetailView): 
    model = Movie
    template_name = "prj/detail.html" 
    context_object_name = "movie"

    #reviews for movies
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if hasattr(self, 'object') and self.object is not None:
            context['reviews'] = self.object.movie_reviews.all()
            context['comments'] = Comment.objects.filter(review__in=self.object.movie_reviews.all())
            context['average_rating'] = self.object.movie_reviews.aggregate(Avg('rating'))['rating__avg'] or 0
        else:
            context['reviews'] = []
            context['comments'] = []
            context['average_rating'] = 0
        context['review_form'] = ReviewForm()
        context['comment_form'] = CommentForm()
    
        if self.request.user.is_authenticated:
            context['is_favorite']= Favorite.objects.filter(user=self.request.user,movie=self.object).exists()
        else:
            context['is_favorite'] =False  
        return context 

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()  
        if 'review_submit' in request.POST:
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.movie = self.object
                review.user = request.user
                review.save()
                messages.success(request, 'Review added!')
        elif 'comment_submit' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                review_pk = request.POST.get('review_pk')
                comment.review = Review.objects.get(pk=review_pk)
                comment.user = request.user
                comment.save()
                messages.success(request, 'Comment added!')
            return redirect('detail', pk=self.kwargs['pk'])
        
        #favorite movies
        if 'favorite_submit' in request.POST:
              if request.user.is_authenticated:
                 favorite, created = Favorite.objects.get_or_create(user=request.user, movie=self.object)
                 if not created:
                    favorite.delete()
                    messages.success(request, 'Removed from favorites!')
                 else:
                    messages.success(request, 'Added to favorites!')
                    
                 return redirect('detail',pk=self.object.pk)   
        return redirect('detail', pk=self.object.pk)
    
class ProfileView(LoginRequiredMixin,TemplateView):
    
    model=Profile
    template_name='prj/profile.html'          
    def get_context_data(self, **kwargs):
     context = super().get_context_data(**kwargs)
     user= self.request.user
     context['username'] = user.username      
     context['favorites'] = Favorite.objects.filter(user=user)
     context['favorites_count'] =context['favorites'].count()
     return context 
                

    #auth
class UserSignupView(CreateView): 
    form_class= UserCreationForm
    template_name='prj/signup.html'
    success_url=reverse_lazy('movie_list') 

    def form_valid(self, form ):
        user=form.save()
        login(self.request,user)
        messages.success(self.request,'signed up successfully!')  
        return redirect('movie_list')  


class UserLoginView(LoginView): 
    template_name=('prj/login.html')
    # redirect_authenticated_user=True
    def get_success_url(self):
        messages.success(self.request,'Welcome!')
        return reverse_lazy('movie_list')
    

class UserLogoutView(LogoutView): 
    next_page= reverse_lazy('movie_list') 
   
    
    