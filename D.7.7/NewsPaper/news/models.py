from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

article = 'AR'
new = 'NE'

TYPEPOST = [
    (article, 'статья'),
    (new, 'новость'),
]

# 1 Модель Author
class Authors(models.Model):
    id_user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        # суммарный рейтинг постов
        sum_r_post = 0
        posts = Post.objects.filter(authors_id=self.id)
        for i in range(len(posts)):
            sum_r_post = sum_r_post + posts[i].rating_post

        #суммарный рейтинг комментариев
        sum_r_comments = 0
        сomments = Comment.objects.filter(id_user=self.id_user)
        for i in range(len(сomments)):
            sum_r_comments = sum_r_comments + сomments[i].rating_com

        sum_r_comments_post = 0
        for i in range(len(posts)):
            comments_post = Comment.objects.filter(id_post=posts[i].id)
            for j in range(len(comments_post)):
                sum_r_comments_post = sum_r_comments_post + comments_post[j].rating_com

        self.rating = 3 * sum_r_post + sum_r_comments + sum_r_comments_post
        self.save()

    #def __str__(self):
    #    return User.objects.filter(id=self.id)[0].last_name

# 2 Модель Category
class Category(models.Model):
    name_category = models.CharField(unique=True, max_length=30)

    def __str__(self):
        return self.name_category.title()

# 3 Модель  Post
class Post(models.Model):
    article = 'AR'
    new = 'NE'

    authors_id = models.ForeignKey(Authors, on_delete=models.CASCADE)
    type_post = models.CharField(max_length=2, choices=TYPEPOST)
    time_in = models.DateTimeField(auto_now_add=True)

    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=50)
    text_post = models.TextField()
    rating_post = models.IntegerField(default=0)

    def like(self):
        self.rating_post = self.rating_post + 1
        self.save()

    def dislike(self):
        if self.rating_post > 0:
            self.rating_post = self.rating_post - 1
            self.save()

#метод возвращает первые 40 символов новости
    def preview(self):
        return self.text_post[0:40] + ' ...'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])



# 4 Модель  PostCategory
class PostCategory(models.Model):
    id_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    id_category = models.ForeignKey(Category, on_delete=models.CASCADE)

# 5 Модель Comment

class Comment(models.Model):
    id_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    text_com = models.TextField()
    time_in = models.DateTimeField(auto_now_add=True)
    rating_com = models.IntegerField(default=0)

    def like(self):
        self.rating_com = self.rating_com + 1
        self.save()

    def dislike(self):
        if self.rating_com > 0:
            self.rating_com = self.rating_com - 1
            self.save()






