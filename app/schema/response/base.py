# coding=utf-8

from marshmallow import Schema, post_dump


class BaseResponseSchema(Schema):
    # pylint: disable=unused-argument
    @post_dump(pass_original=True)
    def wrap(self, result, original, many, **kwargs):
        context = {}
        if isinstance(original, Schema):
            context = original.context
        return ResponseFormatter.format(result, context)


class ResponseFormatter:
    @staticmethod
    def format(result, context):
        response = {
            "message": "Success",
            "success": True,
        }

        if result:
            response["data"] = result

        if context.get("message"):
            response["message"] = context.get("message")

        return response


class BaseResponseWithDataSchema(Schema):
    # pylint: disable=unused-argument
    @post_dump(pass_original=True)
    def wrap(self, result, original, many, **kwargs):
        context = {}
        if isinstance(original, Schema):
            context = original.context
        return ResponseFormatterNoFieldData.format(result, context)


class ResponseFormatterNoFieldData:
    @staticmethod
    def format(result, context):
        response = {
            "message": "Success",
            "success": True,
        }

        if result:
            response["data"] = result["data"]

        if context.get("message"):
            response["message"] = context.get("message")

        return response
