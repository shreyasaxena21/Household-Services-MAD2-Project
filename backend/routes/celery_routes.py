from flask_restful import Resource
from flask import jsonify, request, make_response

class DailyMail(Resource):
    def get(self):
        from backend.task import daily_remainder
        daily_remainder = daily_remainder.delay()
        while not daily_remainder.ready():
            pass
        return make_response(jsonify({"message": "task triggered successfully", "id": daily_remainder.id, "name": daily_remainder.result, "status": daily_remainder.status}), 201)
    
class MonthlyREport(Resource):
    def get(self):
        from backend.task import monthly_report
        monthly_report = monthly_report.delay()
        while not monthly_report.ready():
            pass
        return make_response(jsonify({"message": "task triggered successfully", "id": monthly_report.id, "name": monthly_report.result, "status": monthly_report.status}), 201)

class ExportCSV(Resource):
    def get(self):
        from backend.task import create_csv
        create_csv = create_csv.delay()
        while not create_csv.ready():
            pass
        return make_response(jsonify({"message": "task triggered successfully", "id": create_csv.id, "name": create_csv.result, "status": create_csv.status}), 201)
