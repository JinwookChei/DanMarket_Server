from django.contrib import admin
from django.urls import path, include
# index는 대문, blog는 게시판
from main.views import hello_world, index, blog, new_post, posting, remove_post, hello_world_drf

# 이미지를 업로드하자
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers
from . import views

router = routers.DefaultRouter(trailing_slash=False)
router.register('post', views.Postview)

urlpatterns = [
    path('admin/', admin.site.urls),
    # 웹사이트의 첫화면은 index 페이지이다 + URL이름은 index이다
    path('', index, name='index'),
    # URL:80/blog에 접속하면 blog 페이지 + URL이름은 blog이다
    path('blog/', blog, name='blog'),
    # URL:80/blog/숫자로 접속하면 게시글-세부페이지(posting)
    path('blog/<int:pk>/', posting, name='posting'),
    path('new_post/', new_post, name='new_post'),
    path('blog/<int:pk>/remove/', remove_post),
    #Post View
    path('', include(router.urls)),

]

# 이미지 URL 설정
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
