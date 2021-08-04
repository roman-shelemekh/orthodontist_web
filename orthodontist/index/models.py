import datetime
from django.core.cache import cache
from django.db import models
from django.contrib.auth.models import User
from orthodontist import settings
from .tasks import image_resizing


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='profile_pics/default.png', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(Profile, self).save()
        image_resizing.delay(self.image.path)

    def last_seen(self):
        return cache.get(f'seen_{self.user.username}')

    def online(self):
        if self.last_seen():
            now = datetime.datetime.now()
            if now > self.last_seen() + datetime.timedelta(seconds=settings.USER_ONLINE_TIMEOUT):
                return False
            else:
                return True
        else:
            return False
