from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from .models import Post,Category
from .serializer import PostSerializer,CategorySerializer
from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

class CategoryListAPIView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

class CategoryCreateAPIViews(APIView):
    def post(self,request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            object = serializer.save()
            return Response(CategorySerializer(object).data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class CategoryDetailAPIView(APIView):
    def get(self,request,pk):
        category =get_object_or_404(category,pk=pk)
        return Response(CategorySerializer(category).data,status = status.HTTP_200_OK)
    

class CategoryUpdateAPIView(APIView):
    def put (self,request,pk):  
        category = get_object_or_404(Category,pk=pk)
        serializer = CategorySerializer(category,data=request.data)    
        if serializer.is_valid():
            object = serializer.save()
            return Response(CategorySerializer(object).data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

class CategoryDeleteAPIView(APIView):
    def delete(self,request,pk):
        category =get_object_or_404(Category,pk=pk)  
        category.delete ()
        return Response(status=status.HTTP_204_NO_CONTENT)
      




class BlogListAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]

    # enable filters
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category']  # filter by category
    search_fields = ['title', 'content']  # search by title/con


# ----------------- Retrieve Single Blog (by slug or ID) -----------------
class BlogDetailAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk=None, slug=None):
        if slug:
            post = get_object_or_404(Post, slug=slug)
        else:
            post = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)


# ----------------- Create Blog -----------------
class BlogCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)  # assign logged-in user as author
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ----------------- Update Blog (only author) -----------------
class BlogUpdateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, pk):
        post = get_object_or_404(Post, pk=pk, author=request.user)  # check author
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ----------------- Delete Blog (only author) -----------------
class BlogDeleteAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        post = get_object_or_404(Post, pk=pk, author=request.user)  # check author
        post.delete()
        return Response({"message": "Blog deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    


    
class PostListAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]

    # add filters + search
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category']  # filter by category id or slug if you add slug
    search_fields = ['title', 'content'] 