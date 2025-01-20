from django.db import models 
from django.utils.translation import gettext_lazy as _
import uuid , os



# Create your models here.

class BaseModel(models.Model):

    id = models.UUIDField(primary_key=True , default=uuid.uuid4 , editable= False)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:

        abstract = True






def upload_to(instance,filename):
    model_name = instance.model_name.lower()
    return os.path.join(model_name , filename)

    

class Image(BaseModel):

    name = models.CharField(_('Name'), max_length=200,blank=True, null=True)
    alt_text = models.CharField(_('Alternative Text'), max_length=50 , blank=True, null=True)
    model_name = models.CharField(max_length=50)
    Image = models.ImageField(_('Image'), upload_to= upload_to)
    is_default = models.BooleanField(default=False)
    

    class Meta:

        verbose_name = _('Image')
        verbose_name_plural = _('Images')


    @classmethod
    def make_iamge(cls,images,post):

        for image in images:
                
            img = cls.objects.create(
                name=image.name,
                Image=image,
                model_name="post"
            )
            post.images.add(img)





