import graphene

import blog.schema
import users.schema


class Query(blog.schema.Query, users.schema.Query, graphene.ObjectType):
    # Combine the queries from different apps
    pass


class Mutation(blog.schema.Mutation, users.schema.Mutation, graphene.ObjectType):
    # Combine the mutations from different apps
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
