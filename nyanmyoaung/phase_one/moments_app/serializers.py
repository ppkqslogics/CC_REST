# from rest_framework import serializers
# from rest_framework.exceptions import ValidationError
# from userapp.serializers import img_compress

# from moments_app.models import Comments, PostImages, SubComments, Timelines


# class PostImagesSerializer(serializers.ModelSerializer):
#     '''
#     Serializer for PostImages
#     INPUT : post(post_id), image(one time at a time, compression included, 50%)
#     OUTPUT/RETURN : serilized_data, image_url(full_path with domain), validate_image(image_compression), get_image_url(build_image_url)
#     MODEL : PostImages
#     FIELDS : all
#     '''
#     image = serializers.ImageField(allow_empty_file=True, use_url=True)
#     image_url = serializers.SerializerMethodField('get_image_url')

#     class Meta:
#         model = PostImages
#         # exclude = ['image_url']
#         fields = '__all__'

#     def get_image_url(self, obj):
#         request = self.context.get("request")
#         print("======>",type(obj.image))
#         return request.build_absolute_uri(obj.image.url)

#     def validate_image(self, photo):
#         print("PHOTO", photo)
#         if photo == "":
#             return photo
#         else:
#             request = self.context.get("request")
#             new_image = img_compress(photo)
#             print("======>new",type(new_image))
#             # return new_image
#             return new_image

    


# class MyTimelinesSerializer(serializers.ModelSerializer):
#     '''
#     Serializer for Timelines
#     INPUT : user(id), post_id(auto_generate), caption(status), video(with_limit), liked(liked_person_profile_id)
#     OUTPUT/RETURN : serilized_data, validate_video(video_size_validation)
#     MODEL : Timelines
#     FIELDS : all
#     VALIDATORS : validate_video, get_like_count, get_comments_count, get_images(post image list)
#     '''
#     name = serializers.CharField(max_length = 30, source='user_id.user.name', read_only=True)
#     photo = serializers.ImageField(source='user_id.user.photo', read_only=True)
#     like_count = serializers.SerializerMethodField('get_like_count')
#     comments_count = serializers.SerializerMethodField('get_comments_count')
#     images = serializers.SerializerMethodField('get_images')
    
#     class Meta:
#         model = Timelines
#         #fields = '__all__'#['like_count']
#         exclude = ['liked']

#     # Video size validation
    
#     # timeline post like count
#     def get_like_count(self, obj):
#         # print("obj",obj.liked.all().count())
#         return obj.liked.all().count()

#     # timeline post comment count
#     def get_comments_count(self, obj):
#         # print("obj",obj.liked.all().count())
#         return obj.comments_set.all().count()

#     # get timeline image lists
#     def get_images(self, obj):
#         image_obj = obj.postimages_set.all()
#         if image_obj.count() != 0:
#             request = self.context.get("request")
#             images = PostImagesSerializer(image_obj, context={"request": request}, many=True)
#             images = images.data
#         else:
#             images = []
#         return images

#     # def validate_video(self, video):
#     #     print(self)
#     #     print("======================mmmmmmmmmmmmmmmmmmmmmm=====>", video)
#     #     print("======================mmmmmmmmmmmmmmmmmmmmmm=====>", video.size)
#     #     if video.size >= 209460:
#     #         print("+++++++++++++++++++++>?",video.size)
#     #         raise ValidationError
#     #     else:
#     #         print("======================hhhhhhhhhhhhhhhhhhhh=====>", video.size)
#     #         return video


# class CommentsSerializer(serializers.ModelSerializer):
#     '''
#     Serializer for Timelines
#     INPUT : user(id), post(id), comments, liked(liked_person_profile_id)
#     OUTPUT/RETURN : serilized_data
#     MODEL : Comments
#     FIELDS : all
#     '''
#     like_count = serializers.SerializerMethodField('get_like_count')
#     sub_cmt_count = serializers.SerializerMethodField('get_sub_cmt_count')
#     class Meta:
#         model = Comments
#         exclude = ['liked']
#         # fields = '__all__'

#     def get_like_count(self, obj):
#         # print("obj",obj.liked.all().count())
#         return obj.liked.all().count()

#     def get_sub_cmt_count(self, obj):
#         # print("obj",obj.liked.all().count())
#         return obj.subcomments_set.all().count()


# class SubCommentsSerializer(serializers.ModelSerializer):
#     '''
#     Serializer for Timelines
#     INPUT : user(id), comment(id), sub_comment, liked(liked_person_profile_id)
#     OUTPUT/RETURN : serilized_data
#     MODEL : SubComments
#     FIELDS : all
#     '''
#     class Meta:
#         model = SubComments
#         fields = '__all__'
