from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Movie(models.Model):
    title= models.CharField(max_length=200)
    release_year=models.IntegerField()
    genre=models.CharField(max_length=100)
    description=models.TextField(blank=True)
    poster= models.ImageField( upload_to='prj/posters/',null=True, blank=True)
    director=models.CharField(max_length=200,default="Unknown")
    def __str__(self):
        return self.title
    
    
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE , related_name='movie_reviews')
    text=models.TextField()
    rating=models.IntegerField(choices=[(i,i) for i in range(1,6)])
    created_at= models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.username} 's review for {self.movie.title}"
    
    
class Comment(models.Model):
    review=models.ForeignKey(Review, on_delete=models.CASCADE,related_name='comments_review')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text=models.TextField()
    rating=models.IntegerField(choices=[(i,i) for i in range(1,6)] , default=3)
    created_at= models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.username} 's comment on {self.review}"
    
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    added_at= models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together= ('user','movie')
    def __str__(self):
        return f"{self.user.username} 's favorite: {self.movie.title}"
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #another profile fields
    bio = models.TextField( max_length=500,blank=True)
    cover = models.ImageField(upload_to='profile_covers/', blank=True, null=True)
    avatar=models.ImageField(upload_to='avatars/', blank=True, null=True)
    birth_date=models.DateField(null=True,blank=True)
    def __str__(self):
        return f"{self.user.username} Profile"  
    
    
@receiver(post_save,sender=User)    
def user_profile_signals( sender, instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)
# @receiver(post_save,sender=User)       
    else:
      instance.profile.save()        
    