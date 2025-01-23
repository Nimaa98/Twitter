from django.db import models 
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from Core.models import BaseModel 
from django.urls import reverse

# Create your models here.

class User(BaseModel , AbstractUser):
     
    phone_number = models.CharField(_('Phone Number'), max_length=20, blank=True )
    birthday = models.DateField(_('Birthday') , null=True , blank=True)
    bio = models.CharField(_('Biography') , max_length=300 , blank=True)
    profile_image = models.ForeignKey('Core.Image' , on_delete= models.SET_DEFAULT ,
                                        null=True , blank=True ,
                                        related_name= 'user_images',
                                        default= None)
   

   
    soft_delete = models.BooleanField(_('Delete User'), default=False)


    class Meta:
            
        verbose_name = _('User')
        verbose_name_plural = _('Users')


    def count_followers(self):
        return self.Follower.count()

    def count_following(self):
        return self.Following.count()
    
    def follow(self,from_user,to_user):
        Follow.objects.create(follower_user = from_user , following_user=to_user)

    def unfollow(self,from_user,to_user):
        Follow.objects.filter(follower_user = from_user , following_user=to_user).delete()


    def is_following(self,this_user,user):
        return Follow.objects.filter(following_user=user, follower_user=this_user).exists()


    def get_absolute_url(self):
        
        return reverse("Users:detail-user", args=[self.pk])

    
    


class Follow(BaseModel):
     
    following_user = models.ForeignKey(User , on_delete= models.CASCADE ,
                                         related_name='Following' )
     
    follower_user = models.ForeignKey(User, on_delete=models.CASCADE ,
                                        related_name='Follower')
     
    class Meta:
        unique_together = ('following_user', 'follower_user')
        verbose_name = _('Follow')
        verbose_name_plural = _('Follows')
        

