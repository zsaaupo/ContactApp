import secrets
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


# Create your models here.
class AppUser(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.full_name)
            person_exists = AppUser.objects.filter(slug=slug).exists()
            if person_exists:
                hexa = secrets.token_hex(10)
                self.slug = slug + "-AmRjZe798653-" + hexa
            else:
                self.slug = slug
            super(AppUser, self).save(*args, **kwargs)
        else:
            super(AppUser, self).save(*args, **kwargs)
