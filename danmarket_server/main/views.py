#from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import redirect, render
# View에 Model(Post 게시글) 가져오기
from .models import Post
from .serializers import PostSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt


# index.html 페이지를 부르는 index 함수
def index(request):
    return render(request, 'main/index.html')

# blog.html 페이지를 부르는 blog 함수
def blog(request):
    # 모든 Post를 가져와 postlist에 저장
    postlist = Post.objects.all()
    # blog.html 페이지를 열 때, 모든 Post인 postlist도 같이 가져옴 
    return render(request, 'main/blog.html', {'postlist':postlist})

# blog의 게시글(posting)을 부르는 posting 함수
def posting(request, pk):
    # 게시글(Post) 중 pk(primary_key)를 이용해 하나의 게시글(post)를 검색
    post = Post.objects.get(pk=pk)
    # posting.html 페이지를 열 때, 찾아낸 게시글(post)을 post라는 이름으로 가져옴
    return render(request, 'main/posting.html', {'post':post})

@csrf_exempt
def new_post(request):
    if request.method != 'POST':
        postname = request.POST.get('postname')
        contents = request.POST.get('contents')
        mainphoto = request.FILES.get('mainphoto')

        if postname and contents and mainphoto:
            post = Post(postname=postname, contents=contents, mainphoto=mainphoto)
            post.save()
            return JsonResponse({'message': '게시물이 성공적으로 추가되었습니다.'}, status=200)
        else:
            return JsonResponse({'error': '모든 필드를 입력하세요.'}, status=400)
    
    return JsonResponse({'error': '잘못된 요청입니다.'}, status=400)

def remove_post(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('/blog/')
    return render(request, 'main/remove_post.html', {'Post': post})

#기존 방식
# def hello_world(response):
#     return render('Hellow_world')

#render를 사용하면 html기반으로 유저에게 넘겨줄수 있음.
def hello_world(request):
    return render(request, 'main/temp.html')

#DRF 방식
@api_view()
def hello_world_drf(request):
    return Response({"message" : "Hello world DRF"})


class Postview(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer