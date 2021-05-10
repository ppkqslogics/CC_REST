# import uuid
# from datetime import datetime

# from django.db import models
# from profile_app.models import Profile
# from userapp.id_generator import post_id_generator
# from userapp.models import User


# def unique_tag_id():
#     unique_id = post_id_generator()
#     try:
#         while Timelines.objects.filter(post_id=unique_id).exists():
#             unique_id = post_id_generator()
#         return unique_id
#     except Exception:
#         return unique_id

# def unique_timeline_id():
#     unique_id = str(uuid.uuid4())+str(datetime.now().strftime('%d-%m-%y-%X'))
#     try:
#         while Timelines.objects.filter(post_id=unique_id).exists():
#             unique_id = str(uuid.uuid4())+str(datetime.now().strftime('%d-%m-%y-%X'))
#         return unique_id
#     except Exception:
#         return unique_id

# class Timelines(models.Model):
#     '''
#     Timelines for posting
#     INPUT : user(id), post_id(auto_generate), caption(status), video(with_limit), liked(liked_person_profile_id)
#     OUTPUT/RETURN : timelines_model, _str_(self), get_like(self), get_like_counts(self)
#     '''
#     # id = models.CharField(primary_key=True, default=str(uuid.uuid4)+'self.created_at', editable=False, unique=True, max_length=1000)
#     user_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
#     post_id = models.CharField(
#         default=unique_timeline_id, max_length=100, unique=True, primary_key=True)
#     caption = models.TextField(blank=True)
#     video = models.FileField(upload_to="data", blank=True)
#     liked = models.ManyToManyField(
#         Profile, related_name="timeline_like", blank=True)
#     created_at = models.DateTimeField(auto_now_add=True, blank=True)
#     updated_at = models.DateTimeField(auto_now=True, blank=True)

#     def __str__(self):
#         return f'{str(self.user_id)}-{self.caption}'

#     def get_like(self):
#         return self.liked.all()

#     def get_like_counts(self):
#         return self.liked.all().count()


# class PostImages(models.Model):
#     '''
#     Image Upload for Post
#     INPUT : post(post_id), image(one time at a time, compression included, 50%)
#     OUTPUT/RETURN : postimages_model
#     '''
#     post_id = models.ForeignKey(
#         Timelines, on_delete=models.CASCADE, blank=True)
#     image = models.ImageField(upload_to="post_image", blank=True)


# class Comments(models.Model):
#     '''
#     Comments for post
#     INPUT : user(id), post(id), comments, liked(liked_person_profile_id)
#     OUTPUT/RETURN : comments_model, _str_(self), get_like(self), get_like_counts(self) 
#     '''
#     id = models.CharField(default=unique_timeline_id, max_length=100, unique=True, primary_key=True)
#     user_id = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True)
#     post = models.ForeignKey(Timelines, on_delete=models.CASCADE, blank=True)
#     comment = models.TextField(blank=True)
#     liked = models.ManyToManyField(
#         Profile, related_name="comments_like", blank=True)
#     created_at = models.DateTimeField(auto_now_add=True, blank=True)
#     updated_at = models.DateTimeField(auto_now=True, blank=True)

#     def __str__(self):
#         return f'{str(self.post)}-{self.comment}'

#     def get_like(self):
#         return self.liked.all()

#     def get_like_counts(self):
#         return self.liked.all().count()


# class SubComments(models.Model):
#     '''
#     Comments for post
#     INPUT : user(id), comment(id), sub_comment, liked(liked_person_profile_id)
#     OUTPUT/RETURN : subcomments_model, _str_(self), get_like(self), get_like_counts(self) 
#     '''
#     id = models.CharField(default=unique_timeline_id, max_length=100, unique=True, primary_key=True)
#     user_id = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True)
#     comment = models.ForeignKey(Comments, on_delete=models.CASCADE, blank=True)
#     sub_comment = models.TextField(blank=True)
#     liked = models.ManyToManyField(
#         Profile, related_name="sub_comments_like", blank=True)
#     created_at = models.DateTimeField(auto_now_add=True, blank=True)
#     updated_at = models.DateTimeField(auto_now=True, blank=True)

#     def __str__(self):
#         return f'{str(self.user_id)}-{self.sub_comment}'

#     def get_like(self):
#         return self.liked.all()

#     def get_like_counts(self):
#         return self.liked.all().count()
