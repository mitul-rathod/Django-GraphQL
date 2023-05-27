# schema.py
import graphene
from graphene_django import DjangoObjectType

from .models import Author, Post


class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = "__all__"


class AuthorType(DjangoObjectType):
    class Meta:
        model = Author
        fields = "__all__"


class CreatePost(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        content = graphene.String(required=True)
        author_id = graphene.ID(required=True)

    post = graphene.Field(PostType)

    def mutate(self, info, title, content, author_id):
        """
        The mutate function is the function that will be called when a client
        makes a request to this mutation. It takes in four arguments:
        self, info, title and content. The first two are required by all mutations;
        the last two are the arguments we defined in our CreatePostInput class.

        :param self: Access the object's attributes and methods
        :param info: Access the context of the request
        :param title: Create a new post with the title provided
        :param content: Pass the content of the post
        :param author_id: Get the author object from the database
        :return: A createpost object
        """
        author = Author.objects.get(pk=author_id)
        post = Post(title=title, content=content, author=author)
        post.save()
        return CreatePost(post=post)


class UpdatePost(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        title = graphene.String()
        content = graphene.String()

    post = graphene.Field(PostType)

    def mutate(self, info, id, title=None, content=None):
        """
        The mutate function is the function that will be called when a client
        calls this mutation. It takes in four arguments: self, info, id and title.
        The first two are required by all mutations and the last two are specific to this mutation.
        The self argument refers to the class itself (UpdatePost) while info contains information about
        the query context such as authentication credentials or access control lists.

        :param self: Pass the instance of the class
        :param info: Access the context of the request
        :param id: Find the post we want to update
        :param title: Update the title of a post
        :param content: Update the content of a post
        :return: An instance of the updatepost class, which is a subclass of mutation
        """
        try:
            post = Post.objects.get(pk=id)
        except Post.DoesNotExist:
            raise Exception("Post not found")

        if title is not None:
            post.title = title
        if content is not None:
            post.content = content

        post.save()
        return UpdatePost(post=post)


class DeletePost(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        """
        The mutate function is the function that will be called when a client
        calls this mutation. It takes in four arguments: self, info, id. The first
        argument is the object itself (the class instance). The second argument is
        information about the query context and user making this request. We don't
        need to use it here so we'll just pass it along as-is to our model method.
        The third argument is an ID of a post we want to delete.

        :param self: Represent the instance of the class
        :param info: Access the context of the query
        :param id: Find the post that is to be deleted
        :return: A deletepost object, which is the return type of the mutation
        """
        try:
            post = Post.objects.get(pk=id)
        except Post.DoesNotExist:
            raise Exception("Post not found")

        post.delete()
        return DeletePost(success=True)


class Query(graphene.ObjectType):
    posts = graphene.List(PostType)
    authors = graphene.List(AuthorType)

    def resolve_posts(self, info):
        """
        The resolve_posts function is a resolver. It’s responsible for retrieving the posts from the database and returning them to GraphQL.

        :param self: Refer to the current instance of a class
        :param info: Pass along the context of the query
        :return: All post objects from the database
        """
        return Post.objects.all()

    def resolve_authors(self, info):
        """
        The resolve_authors function is a resolver. It’s responsible for retrieving the data that will be returned as part of an execution result.

        :param self: Pass the instance of the object to be used
        :param info: Pass information about the query to the resolver
        :return: A list of all the authors in the database
        """
        return Author.objects.all()


class Mutation(graphene.ObjectType):
    create_post = CreatePost.Field()
    update_post = UpdatePost.Field()
    delete_post = DeletePost.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
