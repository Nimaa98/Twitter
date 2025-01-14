from django.db import models
from Core.models import BaseModel
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from Users.models import User
from Core.models import Image
from django.urls import reverse

# Create your models here.


class Post(BaseModel):
    title = models.CharField(_('Title'),max_length=100)
    text = models.TextField(_('Text'))
    user = models.ForeignKey(User,verbose_name=_('User'),
                             on_delete=models.CASCADE,
                             related_name='user_post')
    
    tags = models.ManyToManyField('Tag',related_name='tag_post',
                             verbose_name=_('Tag'),
                             through='PostTag',
                             )
    
    images = models.ManyToManyField(Image,
                                           related_name='image_post',
                                           verbose_name=_('Image'),
                                           through='PostImage',
                                           )
    
                             
    def __str__(self):
        return self.title
    
    class Meta:
        
        verbose_name= _('Post')
        verbose_name_plural = _('Posts')


    def like(self,by_user,post):
        Like.objects.create(post = post , user=by_user)

    def dislike(self,by_user,post):
        Like.objects.filter(post = post , user=by_user).delete()



    def count_likes(self):
        return self.post_like.count()
    
    def count_comments(self):
        return self.post_comment.count()
    
    def is_liked(self,by_user,post):
        return Like.objects.filter(user=by_user, post=post).exists()
    


class PostImage(BaseModel):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    image = models.ForeignKey(Image,on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)
    

    
class Tag(BaseModel):
    text = models.CharField(_('Text'), max_length= 100)
    slug = models.SlugField(unique=True,db_index=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.text)
        super().save(*args,**kwargs)
        

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')


class PostTag(BaseModel):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag,on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)




class Comment(BaseModel):

    text = models.TextField(_('Text'))
    post = models.ForeignKey(Post,on_delete=models.CASCADE , related_name='post_comment')
    user = models.ForeignKey(User , on_delete=models.CASCADE , related_name='user_comment')

    parent = models.ForeignKey('self',verbose_name=_('Parent Comment'),
                               null=True,blank=True,
                               on_delete=models.CASCADE ,
                               related_name='comment')

    def __str__(self):
        return self.text
    
    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')

class Like(BaseModel):
    
    post = models.ForeignKey(Post,on_delete=models.CASCADE , related_name='post_like')
    user = models.ForeignKey(User , on_delete=models.CASCADE , related_name='user_like')


    def __str__(self):
        return f"Liked by {self.user.username} on {self.post.title}"
    
    class Meta:
        verbose_name = _('Like')
        verbose_name_plural = _('Likes')

    
