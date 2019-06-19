#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:Administrator
@file: serializers.py
@time: 2019/06/17
@software: PyCharm
@detail: 序列化
"""

from flask_restful import fields

from bluelog.extensions import db
from bluelog.apis.utils import DatetimeItem, RelationshipCountItem

serializer_category = {
    'id': fields.Integer,
    'name': fields.String,
    'posts_count': RelationshipCountItem(attribute='posts'),
    '_links': {
        'self': fields.Url('api.category', absolute=True)
    }
}

serializer_post = {
    'id': fields.Integer,
    'title': fields.String,
    'body': fields.String,
    'timestamp': DatetimeItem(attribute='timestamp'),
    'category': serializer_category,
    'can_comment': fields.Boolean,
    'comments_count': RelationshipCountItem(attribute='comments'),
    'comments': fields.List(
        fields.Nested({
            'author': fields.String,
            'email': fields.String,
            'site': fields.String,
            'body': fields.String
        })
    ),
    'links': {
        'self': fields.Url('api.post', absolute=True),
        'category': fields.Url('api.category', absolute=True),
    }
}


class empty:
    """
    This class is used to represent no data being provided for a given input
    or output value.

    It is required because `None` may be a valid input or output value.
    """
    pass


class DateTime(fields.Raw):
    """
    Return a formatted datetime string in UTC.

    :param dt_format: %Y-%m-%d %H:%M:%S
    :type dt_format: str
    """
    def __init__(self, dt_format='%Y-%m-%d %H:%M:%S', **kwargs):
        super(DateTime, self).__init__(**kwargs)
        self.dt_format = dt_format

    def format(self, value):
        try:
            return value.strftime(self.dt_format)
        except AttributeError as ae:
            raise fields.MarshallingException(ae)


class ModelSerializer:
    serializer_field_mapping = {
        db.Boolean: fields.Boolean,
        db.Integer: fields.Integer,
        db.Float: fields.Float,
        db.Numeric: fields.Fixed,
        db.String: fields.String,
        db.Date: DateTime,
        db.DateTime: DateTime,
        db.Time: DateTime
    }

    def __init__(self, cls_model, depth: int = 0):
        """
        初始化
        :param cls_model: 模型类
        :param depth:
        """
        assert not isinstance(cls_model, db.Model), (
            '初始化序列化器时请传入SQLAlchemy的Model对象'
        )
        self.table = cls_model.__mapper__.tables[0]
        self.relationships = cls_model.__mapper__.relationships
        self.depth = depth

    def _get_field_type_mapping(self, field_type):
        """匹配表字段类型映射关系"""
        for key in self.serializer_field_mapping.keys():
            if isinstance(field_type, key):
                return [key, self.serializer_field_mapping[key]]
        raise LookupError('未匹配到字段类型')

    def get_table_columns(self, columns=None):
        """
        获取表字段对应的类型映射关系
        :return: {表字段对象:[字段类型, 对应序列化类型]}
        """
        columns_type_mapping = {}
        columns = columns or self.table.columns

        for column in columns:
            columns_type_mapping[column] = self._get_field_type_mapping(column.type)
        return columns_type_mapping

    @staticmethod
    def _serializer_boolean(default=None, attribute=None):
        """序列化布尔类型字段"""
        return fields.Boolean(default=default, attribute=attribute)

    @staticmethod
    def _serializer_integer(default: int = None, attribute=None):
        """序列化数值类型字段"""
        return fields.Integer(default=default, attribute=attribute)

    @staticmethod
    def _serializer_float(default=None, attribute=None):
        """序列化浮点类型字段"""
        return fields.Float(default=default, attribute=attribute)

    @staticmethod
    def _serializer_fixed(decimals: int = 5, attribute=None):
        """序列化浮点类型格式化字符串字段"""
        return fields.Fixed(decimals=decimals, attribute=attribute)

    @staticmethod
    def _serializer_string(default=None, attribute=None):
        """序列化字符串类型字段"""
        return fields.String(default=default, attribute=attribute)

    @staticmethod
    def _serializer_datetime(dt_format='%Y-%m-%d %H:%M:%S', attribute=None):
        """序列化日期时间类型字段"""
        return DateTime(dt_format=dt_format, attribute=attribute)

    def serializer_relationships(self):
        serializer_dict = {}
        for relationship in self.relationships:
            if not relationship.uselist:
                continue
            referred_table = relationship.target
            serializer_columns_dict = self.serializer_columns(
                columns=referred_table.columns,
                parent_table_name=self.table.name
            )
            serializer_dict[relationship.key] = fields.List(fields.Nested(serializer_columns_dict, allow_null=True))
        return serializer_dict

    def serializer_columns(self, columns=None, depth: int = None, parent_table_name=None):
        """
        创建格式化字典
        :return: {字段名称: 字段对象}
        """
        serializer_dict = {}
        columns_mapping = self.get_table_columns(columns)
        depth = self.depth if depth is None else depth
        parent_table_name = parent_table_name or self.table.name
        for column, type_mapping in columns_mapping.items():
            # 若字段为外键，并且当前层级数大于0，则可以将外键对应
            if column.foreign_keys and depth:
                constraint = list(column.foreign_keys)[0].constraint
                referred_table = constraint.referred_table
                if referred_table.name not in parent_table_name.split('.'):
                    serializer_dict[column.name] = fields.Nested(self.serializer_columns(
                        columns=referred_table.columns,
                        depth=depth-1,
                        parent_table_name='.'.join((parent_table_name, column.name))
                    ), allow_null=True)
                    continue

            # 参数名称组织，若为外键关联表字段，需要携带关联表名
            # attribute = f'{parent_table_name}.{column.name}' if parent_table_name else column.name
            # attribute = attribute.split('.', 1)[1]
            attribute = column.name

            # 布尔类型字段处理
            if type_mapping[1] == fields.Boolean:
                serializer_dict[column.name] = self._serializer_boolean(attribute=attribute)
            # 数值类型字段处理
            elif type_mapping[1] == fields.Integer:
                serializer_dict[column.name] = self._serializer_integer(attribute=attribute)
            # 浮点类型字段处理
            elif type_mapping[1] == fields.Float:
                serializer_dict[column.name] = self._serializer_float(attribute=attribute)
            # 浮点类型格式化字段处理
            elif type_mapping[1] == fields.Fixed:
                serializer_dict[column.name] = self._serializer_fixed(attribute=attribute)
            # 日期时间字段处理
            elif type_mapping[1] == DateTime:
                if type_mapping[0] == db.DateTime:
                    serializer_dict[column.name] = self._serializer_datetime(attribute=attribute)
                elif type_mapping[0] == db.Date:
                    serializer_dict[column.name] = self._serializer_datetime(attribute=attribute)
                else:
                    serializer_dict[column.name] = self._serializer_datetime(attribute=attribute)
            # 剩余字段均按照字符串字段处理
            else:
                serializer_dict[column.name] = self._serializer_string(attribute=attribute)
        return serializer_dict

    def serializer_result(self):
        result_dict = self.serializer_columns()
        result_dict.update(self.serializer_relationships())
        return result_dict


if __name__ == '__main__':
    from bluelog.models import Post
    serializer = ModelSerializer(Post, depth=1)
    dic = serializer.serializer_result()
    print('>>>>>>>>>>>>>>>%s' % str(dic))
