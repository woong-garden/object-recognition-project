from django.db import models
from user.models import User
from recipe.models import Recipe

class Dessert(models.Model):
    ingred = models.CharField(max_length=20, blank=True)
    dessert_name = models.TextField(blank=True)
    image = models.ImageField(upload_to="dessert_pics", blank=True)

    recipe = models.ForeignKey(Recipe, on_delete=models.PROTECT, related_name='recipe_dessert')  

    def __str__(self):
        return self.dessert_name

class TempImg(models.Model):
    class Meta():
        db_table = 'db_tempimg'
    
    image = models.ImageField(upload_to="post_pics", blank=True)

class Post(models.Model):
    title = models.CharField(max_length=30, blank=True)
    image = models.ImageField(upload_to="post_pics", blank=True)
    ingred = models.CharField(max_length=20, blank=True)        
    dessert = models.ForeignKey(Dessert, on_delete=models.PROTECT, related_name='dessert_post')   

    content = models.TextField(max_length=100,null=True,blank=True )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    like_authors = models.ManyToManyField(User, related_name='like_posts')

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post')
    
    def __str__(self):
        return self.title
    
class Comment(models.Model):
    content = models.TextField(max_length=50, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE,  related_name='comments')

    def __str__(self):
        return self.content
    
    class Meta:
        ordering = ['-created_at']