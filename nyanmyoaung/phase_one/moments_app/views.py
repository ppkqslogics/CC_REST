# from django.core.paginator import EmptyPage, InvalidPage, Paginator
# from profile_app.models import Profile
# from rest_framework import status
# from rest_framework.exceptions import ValidationError
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from userapp.models import User
# from userapp.serializers import img_compress

# from moments_app.models import Comments, SubComments, Timelines
# from moments_app.serializers import (CommentsSerializer, MyTimelinesSerializer,
#                                      PostImagesSerializer,
#                                      SubCommentsSerializer)


# class MyTimeLinesView(APIView):
#     '''
#     View for MyTimelines
#     INPUT : user(id), post_id(auto_generate), caption(status), video(with_limit), liked(liked_person_profile_id), image
#     SREIALIZERS : MyTimelinesSerializer, PostImageSerializer
#     OUTPUT/RETURN : Timelines post list, total page number, image lists
#     METHOD : post, get(my_timeline_view)
#     SUB_FUNCTION: pagination(in get method)
#     PAGINATION_LIMIT : 3
#     '''

#     def post(self, request):
#         try:
#             post_id = request.data['post_id']
#             image = request.data['image']
#             if post_id == "":
#                 print("=====no post id")
#                 print(request.data['video'].size)
#                 if request.data['video'].size >= 50273946:
#                     raise ValidationError
#                 else:
#                     pass
#                 serializer = MyTimelinesSerializer(data=request.data)
#                 print("=====serializer")
#                 if serializer.is_valid():
#                     serializer.save()
#                     if request.data['image'] == "":
#                         if serializer.is_valid():
#                             serializer.save()
#                         return Response(
#                             {
#                                 'isSuccessful': True,
#                                 'message': 'Successfully uploaded post',
#                                 'post_id': serializer.data['post_id']
#                             }
#                         )
#                     else:
#                         # img_obj_list = request.FILES
#                         # img_obj_list = img_obj_list.getlist('image')
#                         # for image in img_obj_list:
#                             # image_file = img_compress(photo=image)
#             # for i in a:
#             #     print("image", i)
#             # print("hh", a.getlist('image'))
#             # b = a.getlist('image')
#             # print(b[1])
#             # return Response({'ok': 'ok'}
#                         img_obj = PostImagesSerializer(data={
#                             'post_id': serializer.data['post_id'],
#                             'image': image
#                         }, context={"request": request})
#                         if img_obj.is_valid():
#                             img_obj.save()
#                             return Response(
#                                 {
#                                     'isSuccessful': True,
#                                     'message': 'Successfully uploaded image',
#                                     'post_id': serializer.data['post_id'],
#                                     'data': img_obj.data
#                                 }
#                             )
#                         else:
#                             return Response(
#                                 {
#                                     'isSuccessful': False,
#                                     'message': 'Fail to upload image'
#                                 }
#                             )
#                 else:
#                     print(serializer.errors)
#                     return Response(
#                         {
#                             'isSuccessful': False,
#                             'message': 'Fail to post'
#                         }
#                     )
#             else:
#                 post_obj = Timelines.objects.filter(post_id=post_id)
#                 if post_obj.exists():
#                     post_obj = post_obj.first()
#                     img_obj = PostImagesSerializer(
#                         data={'post_id': post_obj.post_id, 'image': image})
#                     if img_obj.is_valid():
#                         img_obj.save()
#                         return Response(
#                             {
#                                 'isSuccessful': True,
#                                 'message': 'Successfully uploaded image',
#                                 'post_id':post_obj.post_id
#                             }
#                         )
#                     else:
#                         return Response(
#                             {
#                                 'isSuccessful': False,
#                                 'message': 'Fail to upload image'
#                             }
#                         )
#                 else:
#                     return Response(
#                         {
#                             'isSuccessful': False,
#                             'message': 'Post dose not exit'
#                         }
#                     )
#         except ValidationError as error:
#             print(error)
#             return Response(
#                 {
#                     'isSuccessful': False,
#                     'message': 'Video is longer than limit'
#                 }

#             )
#         except Exception as error:
#             print("MYTIMELINE ERROR: ", str(error))
#             return Response(
#                 {
#                     'isSuccessful': False,
#                     'message': 'Fail to upload post'
#                 }
#             )

#     def get(self, request, user_id):
#         try:
#             user_obj = Profile.objects.get(user_id=user_id)
#             queryset = user_obj.timelines_set.all().order_by('-updated_at')
#             per_page =request.GET.get('per_page', '')
#             print(per_page)
#             limit = int(per_page)
#             serializer_class = MyTimelinesSerializer
#             if queryset:
#                 serializer, total_page_num = pagination(
#                     request, queryset, limit, serializer_class)
#                 print("===============>", total_page_num)
#                 return Response(
#                     {
#                         'isSuccessful': True,
#                         'message': 'Successfully load my timelines',
#                         'posts': serializer,
#                         'total_page_num': total_page_num
#                     }
#                 )
#             else:
#                 return Response(
#                     {
#                         'isSuccessful': True,
#                         'message': 'There is no posts available',
#                         'posts': []
#                     }
#                 )
#         except Exception as error:
#             print("TIMELINES GET ERROR: ", error)
#             return Response(
#                 {
#                     'isSuccessful': False,
#                     'message': 'Something is wrong.'
#                 }
#             )


# class PostLikeView(APIView):
#     '''
#     View for MyTimelines
#     INPUT : who_like(profile_id), post_id(id), 
#     SREIALIZERS : -
#     OUTPUT/RETURN : message with data
#     METHOD : get(like for post)
#     '''

#     def post(self, request):
#         try:
#             post_id = request.data['post_id']
#             who_like = request.data['who_like']
#             profile_obj = Profile.objects.get(user_id=who_like)
#             post_obj = Timelines.objects.filter(post_id=post_id)
#             if post_obj.exists():
#                 post_obj = post_obj.first()
#                 if profile_obj in post_obj.get_like():
#                     post_obj.liked.remove(profile_obj)
#                     return Response(
#                         {
#                             'isSuccessful': True,
#                             'message': 'Unliked',
#                             'like_counts': post_obj.get_like_counts()
#                         }
#                     )
#                 else:
#                     post_obj.liked.add(profile_obj)
#                     return Response(
#                         {
#                             'isSuccessful': True,
#                             'message': 'Liked',
#                             'like_counts': post_obj.get_like_counts()
#                         }
#                     )
#             else:
#                 return Response(
#                     {
#                         'isSuccessful': False,
#                         'message': 'This post is no longer exist.'
#                     }
#                 )
#         except Exception as error:
#             print("POST LIKE ERROR: ", error)
#             return Response(
#                 {
#                     'isSuccessful': False,
#                     'message': 'Something is wrong.'
#                 }
#             )


# class TimelinesView(APIView):
#     '''
#     View for Mixed Timelines
#     INPUT : user_id(id), limit(in_define)
#     SREIALIZERS : MyTimelinesSerializer
#     OUTPUT/RETURN : message with data, pagination next and previous url
#     METHOD : get(Timelines Post with pagination)
#     '''

#     def get(self, request, user_id):
#         try:
#             per_page =request.GET.get('per_page', '')
#             print(per_page)
#             limit = int(per_page)
#             # limit = 10
#             user_obj = User.objects.get(id=user_id)
#             query_set = user_obj.profile.timelines_set.all()
#             serializer_class = MyTimelinesSerializer
#             for friend in user_obj.contact.get_friends():
#                 query_set = friend.timelines_set.all() | query_set
#             queryset = query_set.order_by('-created_at')
#             if queryset:
#                 serializer, total_page_num = pagination(
#                     request, queryset, limit, serializer_class)
#                 print("=================serializer===>",serializer)
#                 return Response(
#                     {
#                         'isSuccessful': True,
#                         'message': 'Successfully load timeline.',
#                         'posts': serializer,
#                         'total_page_num': total_page_num
#                     }
#                 )
#             else:
#                 print("+++++Fail++++++")
#                 return Response(
#                     {
#                         'isSuccessful': True,
#                         'message': 'There is no posts available',
#                         'posts': []
#                     }
#                 )
#         except Exception as error:
#             print("Error", error)
#             return Response({'error': str(error)}, status=status.HTTP_400_BAD_REQUEST)


# class OtherTimelinesView(APIView):
#     '''
#     View for other person timeline
#     INPUT : other_id(id), limit(in_define)
#     SREIALIZERS : MyTimelinesSerializer
#     OUTPUT/RETURN : message with data, pagination next and previous url
#     METHOD : get(Timelines Post with pagination)
#     '''

#     def get(self, request, other_id):
#         try:
#             user_obj = User.objects.get(id=other_id)
#             queryset = user_obj.timelines_set.all().order_by('-updated_at')
#             limit = 3
#             serializer_class = MyTimelinesSerializer
#             if queryset:
#                 serializer, next_page, previous_page, url_link = pagination(
#                     request, queryset, limit, serializer_class)
#                 return Response(
#                     {
#                         'posts': serializer,
#                         'next': f'{url_link}?page={next_page}',
#                         'previous': f'{url_link}?page={previous_page}'
#                     }
#                 )
#             else:
#                 return Response(
#                     {
#                         'isSuccessful': False,
#                         'message': 'There is no posts'
#                     }
#                 )
#         except Exception as error:
#             return Response({'error': str(error)})


# def pagination(request, queryset, limit, serializer_class):
#     paginator = Paginator(queryset, limit)
#     total_page_num = paginator.num_pages
#     print(f"query{queryset}-limit{limit}-paginator{paginator}=====>total{total_page_num}")
#     # b = paginator.page(1)
#     # print(b)
#     try:
#         page = int(request.GET.get('page', '1'))
#         # print(page)
#     except:
#         page = 1
#     try:
#         posts = paginator.page(page)
#     except(EmptyPage, InvalidPage):
#         posts = paginator.page(paginator.num_pages)
#     serializer = serializer_class(
#         posts.object_list, many=True, context={"request": request})
#     # print(serializer.data)
#     try:
#         previous_page = posts.previous_page_number()
#     except:
#         previous_page = posts.number
#     try:
#         next_page = posts.next_page_number()
#     except:
#         next_page = posts.number
#     # return serializer.data, next_page, previous_page, url_link[0]
#     return serializer.data, total_page_num


# class CommentsView(APIView):
#     def post(self, request):
#         try:
#             serializer = CommentsSerializer(data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(
#                     {
#                         'isSuccessful': True,
#                         'message': 'Commented Successfully',
#                         'data': serializer.data
#                     }
#                 )
#             else:
#                 return Response(
#                     {
#                         'isSuccessful': False,
#                         'message': 'Failed to comment'
#                     }
#                 )
#         except Exception as error:
#             print("COMMENTS ERROR: ", error)
#             return Response(
#                 {
#                     'isSuccessful': False,
#                     'message': 'Failed to comment'
#                 }
#             )

#     def get(self, request, post_id, user_id):
#         try:
#             user_obj = User.objects.get(id=user_id)
#             post_obj = Timelines.objects.get(post_id=post_id)
#             queryset = post_obj.comments_set.all()
#             limit = 3
#             serializer_class = CommentsSerializer
#             if queryset:
#                 new_query = post_obj.comments_set.all().filter(user_id=user_id)
#                 for query_obj in queryset:
#                     if query_obj.user_id in user_obj.contact.get_friends():
#                         queryset_obj = post_obj.comments_set.all().filter(user_id=query_obj.user_id)
#                         new_query = queryset_obj | new_query
#                 if new_query:
#                     queryset = new_query.order_by('-created_at')
#                     serializer, total_page_num = pagination(
#                         request, queryset, limit, serializer_class)
#                     return Response(
#                         {
#                             'comments': serializer,
#                             'total_page_num': total_page_num
#                         }
#                     )
#                 else:
#                     return Response(
#                         {
#                             'isSuccessful': True,
#                             'message': 'There is no comment.',
#                             'comments': []
#                         }
#                     )
#             else:
#                 return Response(
#                     {
#                         'isSuccessful': True,
#                         'message': 'There is no posts'
#                     }
#                 )
#         except Exception as error:
#             print("COMMENTS VIEW GET: ", error)
#             return Response(
#                 {
#                     'isSuccessful': False,
#                     'message': 'Something is wrong'
#                 }
#             )


# class CommentLikeView(APIView):
#     def post(self, request):
#         try:
#             comment_id = request.data['comment_id']
#             who_like = request.data['who_like']
#             profile_obj = Profile.objects.get(user_id=who_like)
#             comment_obj = Comments.objects.filter(id=comment_id)
#             if comment_obj.exists():
#                 comment_obj = comment_obj.first()
#                 if profile_obj in comment_obj.get_like():
#                     comment_obj.liked.remove(profile_obj)
#                     return Response(
#                         {
#                             'isSuccessful': True,
#                             'message': 'Unliked',
#                             'like_counts': comment_obj.get_like_counts()
#                         }
#                     )
#                 else:
#                     comment_obj.liked.add(profile_obj)
#                     return Response(
#                         {
#                             'isSuccessful': True,
#                             'message': 'Liked',
#                             'like_counts': comment_obj.get_like_counts()
#                         }
#                     )
#             else:
#                 return Response(
#                     {
#                         'isSuccessful': False,
#                         'message': 'This post is no longer exist.'
#                     }
#                 )
#         except Exception as error:
#             print("POST LIKE ERROR: ", error)
#             return Response(
#                 {
#                     'isSuccessful': False,
#                     'message': 'This post is no longer exist.'
#                 }
#             )


# class SubCommentsView(APIView):
#     def post(self, request):
#         try:
#             serializer = SubCommentsSerializer(data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(
#                     {
#                         'isSuccessful': True,
#                         'message': 'Commented Successfully',
#                         'data': serializer.data
#                     }
#                 )
#             else:
#                 return Response(
#                     {
#                         'error': serializer.errors,
#                         'isSuccessful': False,
#                         'message': 'Failed to comment'
#                     }
#                 )
#         except Exception as error:
#             print("COMMENTS ERROR: ", error)
#             return Response(
#                 {
#                     'isSuccessful': False,
#                     'message': 'Failed to comment'
#                 }
#             )

#     def get(self, request, comment, user_id):
#         try:
#             user_obj = User.objects.get(id=user_id)
#             comment = Comments.objects.filter(comment=comment)
#             limit = 3
#             if comment.exists():
#                 comment_obj = comment.first()
#                 queryset = comment_obj.subcomments_set.all()
#                 serializer_class = SubCommentsSerializer
#                 if queryset:
#                     new_query = queryset.filter(user_id=user_id)
#                     for query_obj.user_id in user_obj.contact.get_friends():
#                         queryset_obj = queryset.filter(
#                             user_id=query_obj.user_id)
#                         new_query = queryset_obj | new_query
#                     if new_query:
#                         queryset = new_query.order_by('-created_at')
#                         serializer, total_page_num = pagination(
#                             request, queryset, limit, serializer_class)
#                         return Response(
#                             {
#                                 'comment': 'aa',
#                                 'sub_comments': serializer,
#                                 'total_page_num': total_page_num
#                             }
#                         )
#                     else:
#                         return Response(
#                             {
#                                 'isSuccessful': True,
#                                 'message': 'There is no subcomment.',
#                                 'sub_comments': []
#                             }
#                         )
#                 else:
#                     return Response(
#                         {
#                             'isSuccessful': True,
#                             'message': 'There is no subcomment.',
#                             'sub_comments': []
#                         }
#                     )
#             else:
#                 return Response(
#                     {
#                         'isSuccessful': False,
#                         'message': 'Comments is no longer available.'
#                     }
#                 )
#         except Exception as error:
#             print("SUBCOMMENTS VIEW GET: ", error)
#             return Response(
#                 {
#                     'isSuccessful': False,
#                     'message': 'Comments is no longer available.'
#                 }, status=status.HTTP_400_BAD_REQUEST
#             )


# class SubCommentLikeView(APIView):
#     def post(self, request):
#         try:
#             sub_comment_id = request.data['sub_comment_id']
#             who_like = request.data['who_like']
#             profile_obj = Profile.objects.get(user_id=who_like)
#             sub_comment_obj = SubComments.objects.filter(id=sub_comment_id)
#             if sub_comment_obj.exists():
#                 sub_comment_obj = sub_comment_obj.first()
#                 if profile_obj in sub_comment_obj.get_like():
#                     sub_comment_obj.liked.remove(profile_obj)
#                     return Response(
#                         {
#                             'isSuccessful': True,
#                             'message': 'Unliked',
#                             'like_counts': sub_comment_obj.get_like_counts()
#                         }
#                     )
#                 else:
#                     sub_comment_obj.liked.add(profile_obj)
#                     return Response(
#                         {
#                             'isSuccessful': True,
#                             'message': 'Liked',
#                             'like_counts': sub_comment_obj.get_like_counts()
#                         }
#                     )
#             else:
#                 return Response(
#                     {
#                         'isSuccessful': False,
#                         'message': 'This post is no longer exist.'
#                     }
#                 )
#         except Exception as error:
#             print("POST LIKE ERROR: ", error)
#             return Response(
#                 {
#                     'isSuccessful': False,
#                     'message': 'This post is no longer exist.'
#                 }
#             )

# # MultiValueDict Tester

# from userapp.serializers import img_compress


# class testing(APIView):
#     def post(self, request):
#         try:
#             print(request.FILES)
#             a = request.FILES
#             for i in a:
#                 print("image", i)
#             print("hh", a.getlist('image'))
#             b = a.getlist('image')
#             for c in b:
#                 d = img_compress(photo=c)
#                 print("========>",d.url, type(d))
#             return Response({'ok': 'ok'})
#         except Exception as error:
#             return Response({'error': str(error)})
