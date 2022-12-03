from rest_framework import routers, serializers, viewsets, pagination
from rest_framework_extensions import routers as ext_routers, mixins as ext_mixins
from authc.models import User
from blog.forms import PostForm, CommentForm
from blog.models import Post, Comment
from rest_framework.response import Response

class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'

class LimitedUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    nama = serializers.CharField()

    class Meta:
        model = User
        fields = ['username', 'nama']

class PostSerializer(serializers.ModelSerializer):
    author = LimitedUserSerializer()

    class Meta:
        model = Post
        fields = ['pk', 'author', 'title', 'content', 'created_timestamp', 'modified_timestamp']
    
class PostViewSet(ext_mixins.NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_timestamp')
    serializer_class = PostSerializer
    pagination_class = StandardResultsSetPagination
    
class CommentSerializer(serializers.ModelSerializer):
    author = LimitedUserSerializer()

    class Meta:
        model = Comment
        fields = ['pk', 'author', 'content', 'post', 'created_timestamp', 'modified_timestamp',]
    
class CommentViewSet(ext_mixins.NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = StandardResultsSetPagination
        
    # def list(self, request, post_id):
    #     post = Post.objects.filter(pk=post_id).first()
    #     queryset = Comment.objects.filter(post=post)
    #     serializer = CommentSerializer(queryset, many=True)
    #     return Response(serializer.data)
    
    # def retrieve(self, request, post_id, pk):
    #     post = Post.objects.filter(pk=post_id).first()
    #     comment = Comment.objects.filter(post=post, pk=pk).first()
    #     serializer = CommentSerializer(comment)
    #     return Response(serializer.data)

router = ext_routers.ExtendedDefaultRouter()
router.register(r'posts', PostViewSet) \
    .register(r'comments', CommentViewSet, 'posts-comment', parents_query_lookups=['post'])

