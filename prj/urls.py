from django.urls import path
from .import views


urlpatterns = [
    path('' , views.MovieListView.as_view() , name = 'movie_list' ),
    path('detail/<int:pk>/' , views.MovieDetailView.as_view() , name = 'detail' ),
    path('profile/' , views.ProfileView.as_view() , name = 'profile' ),
    path('genre/<str:genre>/' , views.GenreMoviesView.as_view() , name = 'genre' ),
    #auth
    path('signup/', views.UserSignupView.as_view() , name = 'signup' ),
    path('login/', views.UserLoginView.as_view() , name = 'login' ),
    path('logout/', views.UserLogoutView.as_view() , name = 'logout' ),
]







