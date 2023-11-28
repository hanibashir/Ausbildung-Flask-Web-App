from flask import request
from flask_restful import Resource, Api
from . import aus_page_blueprint
from ...helpers.constants import Status
from ...helpers.db.Aus_page_queries import AusPageQueries
from ...helpers.to_json import rows_to_json, message_to_json
from ...helpers.validation.aus_page_validator import AusPageValidator

api = Api(aus_page_blueprint)


class AusPageListResource(Resource):
    def __init__(self):
        self.user_query = AusPageQueries()

    def get(self):
        # get all users and convert response to json
        return rows_to_json(self.user_query.select_all())


class AusPageResource(Resource):
    def __init__(self):
        self.data = request.get_json()
        self.validator = AusPageValidator(data=self.data)
        self.aus_page_query = AusPageQueries(data=self.data)
    """
        {
            "title": "Fachinformatiker",
            "duration": "ثلاث سنوات ونصف",
            "certificate": "الثانوية",
            "content":"إنها سلسلة من الكلمات اللاتينية التي ، عند وضعها في موضعها ، لا تشكل جملًا بمعنى كامل ، ولكنها تعطي الحياة لنص اختبار مفيد لملء الفراغات التي يتم شغلها لاحقًا من نصوص مخصصة كتبها متخصصون في الاتصال.",
            "category_id": 1,
            "user_id": 1,
            "shift_type": "دوام متغير",
            "first_year_salary": 800,
            "second_year_salary": 900,
            "third_year_salary": 1000,
            "fourth_year_salary": 0,
            "best_paid": false,
            "popular": true,
            "image_url": "upload/images/users/user.png",
            "links": "ausbildung.de, fachinformatiker.de",
            "published": false
        }
    """

    def post(self):
        # Receive and validate aus page data
        validated, msg = self.validator.validate_aus_page_input()

        if not validated:
            return message_to_json(msg, Status.BAD_REQUEST.value)  # Return a 400 Bad Request status code

        # insert new user
        msg = self.aus_page_query.insert_aus_page()
        return message_to_json(msg=msg, status=Status.CREATED.value)  # Return a 201 Created status code

    def get(self, page_id):
        pass

    def put(self, page_id):
        pass

    def delete(self, page_id):
        pass


# Aus_page routes
api.add_resource(AusPageResource, '/aus_page/<int:page_id>', endpoint='/aus_page/<int:page_id>')
api.add_resource(AusPageResource, '/aus_pages/create', endpoint='/aus_pages/create')
api.add_resource(AusPageListResource, '/aus_pages', endpoint='/aus_pages')
