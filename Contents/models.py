from django.db import models
from Core.models import BaseModel
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from Users.models import User
from Core.models import Image
from django.urls import reverse

# Create your models here.


class Post(BaseModel):
    title = models.CharField(_('عنوان'),max_length=100)
    text = models.TextField(_('متن'))
    user = models.ForeignKey(User,verbose_name=_('User'),
                             on_delete=models.CASCADE,
                             related_name='user_post')

    
    tags = models.ManyToManyField('Tag',related_name='tag_post',
                             verbose_name=_('تگ'),
                             blank=True,
                             through='PostTag',
                             )
    
    images = models.ManyToManyField(Image,
                                           related_name='image_post',
                                           verbose_name=_('Image'),
                                           blank=True,
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
    
    def get_absolute_url(self):
        
        return reverse("Contents:comment-list", args=[self.pk])
    


class PostImage(BaseModel):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    image = models.ForeignKey(Image,on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)
    

    
class Tag(BaseModel):
    text = models.CharField(_('Text'), max_length= 100)
    slug = models.SlugField(unique=True,db_index=True)

        

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')


    def get_absolute_url(self):
        
        return reverse("Contents:tag", args=[self.pk])


    @classmethod
    def make_tag(cls,tags,post):
        tags_list = [tag.strip() for tag in tags.split(',')  if tag.strip()]

        for tag in tags_list:
 
            tag, created = cls.objects.get_or_create(
                text=tag,
                defaults={'slug': tag},
            )
            post.tags.add(tag)



class Follow_Tag(BaseModel):
     
    following_tag = models.ForeignKey(Tag , on_delete= models.CASCADE ,
                                         related_name='Following_Tag' )
     
    follower_user = models.ForeignKey(User, on_delete=models.CASCADE ,
                                        related_name='Follower_user')
     
    class Meta:
        unique_together = ('following_tag', 'follower_user')
        verbose_name = _('Follow Tag')
        verbose_name_plural = _('Follow Tags')


    @staticmethod
    def follow(from_user,tag):
        Follow_Tag.objects.create(follower_user = from_user , following_tag=tag)

    @staticmethod
    def unfollow(from_user,tag):
        Follow_Tag.objects.filter(follower_user = from_user , following_tag=tag).delete()

    @staticmethod
    def is_following(this_user,tag):
        return Follow_Tag.objects.filter(following_tag=tag, follower_user=this_user).exists()


    
    

class PostTag(BaseModel):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag,on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)


    




class Comment(BaseModel):

    text = models.TextField(_('متن نظر'))
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

    
    

class Archive(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="archive")
    archiver_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_archive", null=True
    )



    


    @staticmethod
    def add_post(user, post):
        Archive.objects.create(
            archiver_user=user, post=post
        )


    @staticmethod
    def remove_post(user,post):
        Archive.objects.filter(archiver_user=user,post=post).delete()

    @staticmethod
    def is_save(user,post):
        return Archive.objects.filter(archiver_user=user , post=post).exists()

    @staticmethod
    def take_posts(user):
        
        Archives =  Archive.objects.filter(archiver_user=user)

        post_list = [archive.post for archive in Archives]
        return post_list

