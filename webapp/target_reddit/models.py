from django.db import models


class Author(models.Model):
    updated_at = models.DateTimeField(verbose_name='updated at', auto_now=True)
    name = models.CharField(verbose_name='User name', max_length=50, primary_key=True, unique=True)
    uri = models.URLField(verbose_name='User URI', unique=True)

    class Meta:
        managed = True
        verbose_name = 'Reddit Author'
        verbose_name_plural = 'Reddit Authors'

    def __str__(self):
        return self.name


class Category(models.Model):
    label = models.CharField(verbose_name='Label', max_length=25, primary_key=True)
    term = models.CharField(verbose_name='Term', max_length=25)

    class Meta:
        managed = True
        verbose_name = 'Reddit Category'
        verbose_name_plural = 'Reddit Categories'

    def __str__(self):
        return self.term


class Post(models.Model):
    updated_at = models.DateTimeField(verbose_name='Updated at')
    id = models.CharField(verbose_name='reddit id', max_length=9, primary_key=True)
    link = models.URLField(verbose_name='URL', max_length=300)
    author = models.ForeignKey(Author, verbose_name='Post author', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, verbose_name='Post category', on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Title', max_length=300)

    class Meta:
        managed = True
        verbose_name = 'Reddit Post'
        verbose_name_plural = 'Reddit Posts'

    def __str__(self):
        return '[{}] {} - {}'.format(self.id, self.author.name, self.title)
