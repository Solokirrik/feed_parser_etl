from django.db import models


class Category(models.Model):
    created_at = models.DateTimeField(verbose_name='created at', auto_now=True)
    label = models.CharField(verbose_name='Label', primary_key=True, max_length=50)

    class Meta:
        managed = True
        verbose_name = 'Habr Category'
        verbose_name_plural = 'Habr Categories'

    def __str__(self):
        return self.label

class Creator(models.Model):
    created_at = models.DateTimeField(verbose_name='created at', auto_now=True)
    name = models.CharField(verbose_name='User name', max_length=50, primary_key=True, unique=True)

    class Meta:
        managed = True
        verbose_name = 'Habr Author'
        verbose_name_plural = 'Habr Authors'

    def __str__(self):
        return self.name



class Post(models.Model):
    id = models.CharField(verbose_name='harb id', max_length=9)
    title = models.CharField(verbose_name='Post title', max_length=255)
    guid = models.URLField(verbose_name='Post guid link', primary_key=True, max_length=64)
    link = models.URLField(verbose_name='Post link', max_length=255)
    description = models.TextField(verbose_name='Description', max_length=2000)
    pub_date = models.DateTimeField(verbose_name='published at')
    creator = models.ForeignKey(to=Creator, verbose_name='Creator', on_delete=models.CASCADE)
    category = models.ManyToManyField(to=Category, verbose_name='Category')

    class Meta:
        managed = True
        verbose_name = 'Habr Post'
        verbose_name_plural = 'Habr Posts'

    def __str__(self):
        return '[{}] {} - {}'.format(self.id, self.creator.name, self.title)
