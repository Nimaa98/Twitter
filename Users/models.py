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
     
    class Meta:
            
        verbose_name = _('User')
        verbose_name_plural = _('Users')


    def count_followers(self):
        return self.Follower.count()

    def count_following(self):
        return self.Following.count()
    



    def get_absolute_url(self):
        
        return reverse("Users:detail-user", args=[self.pk])
    
    


class Follow(BaseModel):
     
    following_user = models.ForeignKey(User , on_delete= models.CASCADE ,
                                         related_name='Following' )
     
    follower_user = models.ForeignKey(User, on_delete=models.CASCADE ,
                                        related_name='Follower')
     
    class Meta:
                
        verbose_name = _('Follow')
        verbose_name_plural = _('Follows')