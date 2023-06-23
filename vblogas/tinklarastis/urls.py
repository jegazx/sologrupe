from django.urls import path, include
from .views import Index, BlogPostDetail, generate_thumbnail, upload_video, LikeBlogpost, Featured, DeleteBlogpostView, AddCommentView


urlpatterns = [
    path('tinymce/', include('tinymce.urls')),
    path('', Index.as_view(), name='index'),
    path('<int:pk>/', BlogPostDetail.as_view(), name='blogpost_detail'),
    path('upload/', upload_video, name='upload_video'),
    path('<int:pk>/like/', LikeBlogpost.as_view(), name='like'),
    path('featured/', Featured.as_view(), name='featured'),
    path('<int:pk>/delete/', DeleteBlogpostView.as_view(), name='delete'),
    path('<int:pk>/add_comment/', AddCommentView.as_view(), name='add_comment'),

]

 