from django.db import models
from django.conf import settings

class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                            db_column='created_by', null=True, related_name='created_%(class)s_set')
    updated_by = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                            db_column='updated_by', null=True, related_name='updated_%(class)s_set')
    
    class Meta:
        abstract = True