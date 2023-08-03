from graphene import ObjectType, relay, String, Schema
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField

from main import Memo


class MemoModel(SQLAlchemyObjectType):
    class Meta:
        model = Memo
        interfaces = (relay.Node,)


class MemoConnection(relay.Connection):
    class Meta:
        node = MemoModel


class Query(ObjectType):
    node = relay.Node.Field()

    memo = SQLAlchemyConnectionField(MemoConnection, id=String())
    memo_list = SQLAlchemyConnectionField(MemoConnection, sort=MemoModel.sort_argument())

    def resolve_memo(self, info, **kwargs):
        id = kwargs.get('id')

        memos_query = MemoModel.get_query(info)

        if id is not None:
            return memos_query.filter_by(id=id)

    def resolve_memo_list(self, info, **kwargs):
        return MemoModel.get_query(info).all()


schema = Schema(query=Query)
