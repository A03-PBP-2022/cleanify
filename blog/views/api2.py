from rest_framework import routers, serializers, viewsets, pagination, decorators, status
from rest_framework_extensions import routers as ext_routers, mixins as ext_mixins
from authc.models import User
from blog.forms import PostForm, CommentForm
from blog.models import Post, Comment
from rest_framework.response import Response

class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'

class ReadOnlyModelSerializer(serializers.ModelSerializer):
    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        for field in fields:
            fields[field].read_only = True
        return fields
    # pass

class LimitedUserSerializer(ReadOnlyModelSerializer):
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

    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )

    def create(self, request, *args, **kwargs):
        post = Post()
        post.author = request.user
        serializer = self.serializer_class(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class CommentSerializer(serializers.ModelSerializer):
    author = LimitedUserSerializer(required=False)

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)

    class Meta:
        model = Comment
        fields = ['pk', 'author', 'content', 'post', 'created_timestamp', 'modified_timestamp',]
    
class CommentViewSet(ext_mixins.NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = StandardResultsSetPagination

    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )

    def create(self, request, *args, **kwargs):
        # print(f"PK: {request.user.id}")
        comment = Comment()
        comment.author = request.user
        serializer = self.serializer_class(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

router = ext_routers.ExtendedDefaultRouter()
router.register(r'posts', PostViewSet) \
    .register(r'comments', CommentViewSet, 'posts-comment', parents_query_lookups=['post'])

