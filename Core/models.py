from django.db import models 
from django.utils.translation import gettext_lazy as _
import uuid



# Create your models here.

class BaseModel(models.Model):

    id = models.UUIDField(primary_key=True , default=uuid.uuid4 , editable= False)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:

        abstract = True


    

class Image(BaseModel):

    name = models.CharField(_('Name'), max_length=200)
    alt_text = models.CharField(_('Alternative Text'), max_length=50 , blank=True)
    model_name = models.CharField(max_length=50)
    Image = models.ImageField(_('Image'), upload_to='images/%(model_name)s/')
    is_default = models.BooleanField(default=False)


    class Meta:

        verbose_name = _('Image')
        verbose_name_plural = _('Images')