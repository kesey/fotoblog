from django.db import models
from django.conf import settings
from PIL import Image

class Photo(models.Model):
    image = models.ImageField()
    caption = models.CharField(max_length=128, blank=True)
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    IMAGE_SIZE = (800, 800)

    def resize_image(self):
        image = Image.open(self.image)
        image.thumbnail(self.IMAGE_SIZE)
        image.save(self.image.path) # save resize image in /media/ not the same as the save method of the model (just below)

    def save(self, *args, **kwargs): # surcharge save method of the models.Model
        super().save(*args, **kwargs)
        self.resize_image()

class Blog(models.Model):
    photo = models.ForeignKey(Photo, null=True, on_delete=models.SET_NULL, blank=True)
    title = models.CharField(max_length=128)
    content = models.CharField(max_length=5000)
    # author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    contributors = models.ManyToManyField(settings.AUTH_USER_MODEL, through="BlogContributor", related_name="contributions") # without related_name there is a conflict between reverse accessor user.blog_set (to access every instance of Blog by this user)
    date_created = models.DateTimeField(auto_now=True)
    starred = models.BooleanField(default=False)
    word_count = models.IntegerField(null=True)

    def _get_word_count(self):
        return len(self.content.split())
        
    def save(self, *args, **kwargs): # surcharge save method of the models.Model
        self.word_count = self._get_word_count()
        super().save(*args, **kwargs)

    class Meta: # create a custom permission
        permissions = [
            ("change_blog_title", "Peut changer le titre d'un billet de blog")
        ]

class BlogContributor(models.Model):
    contributor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    contributions = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = ("contributor", "blog") # ensure that there is only one instance of BlogContributor for each contributor - blog pair