import csv
from flask_mail import Message

from app import celery

from backend.celery_task import FlaskTask
from backend.mailer import mail
from backend.models import *
from jinja2 import Template


@celery.task(base=FlaskTask)
def daily_remainder():
    pending_services = ServiceRequest.query.filter(ServiceRequest.service_status == "Pending").all()  
    for service in pending_services:
            professional = User.query.get(service.professional_id)
            professional_email = professional.email

            email_subject = "Regarding Pending Service Requests!"
            email_body = '''
                        Hi
                        This email is to let you know that there are many pending requests from your end
                        Kindly visit A-Z Household Services to complete those requests!!
                        With Regards,
                        Team A-Z Household Services :) 
                        '''
            msg = Message(subject=email_subject, recipients=[professional_email], body=email_body, sender='a-zhouseholdservices@a.com')
            mail.send(msg)

    return "All the Mails are out"

@celery.task(base=FlaskTask)
def monthly_report():
      service_requests = ServiceRequest.query.all()
      for service in service_requests:
            customer = User.query.get(service.customer_id)
            customer_name = customer.fullname
            professional = User.query.get(service.professional_id)
            professional_email = professional.email
            professional_name = professional.fullname
            service_type = professional.service_type
            
            total_requests = ServiceRequest.query.all()
            total_no_of_requests = ServiceRequest.query.count()
            print(total_no_of_requests)
            requested_requests_count = ServiceRequest.query.filter(ServiceRequest.service_status == "Pending").count()
            print(requested_requests_count)
            completed_requests_count = ServiceRequest.query.filter(ServiceRequest.service_status == "Completed").count()
            print(completed_requests_count)

            
            email_subject = "Monthly Activity Report"

            email_body = 'This is an monthly report. Please check the attachment'

            body = '''
            <html>
            <head>
                <title>Monthly Report</title>

                <style>
                    body {
                        font-family: Georgia, 'Times New Roman', Times, serif;
                        margin: 20px;
                        line-height: 1.6;
                        color: #333;
                        background-color: #f9f9f9;
                    }
                    h3 {
                        color: black;
                        margin-bottom: 10px;
                    }
                    h2 {
                        color: #333;
                        border-bottom: 2px solid #4CAF50;
                        padding-bottom: 5px;
                    }
                    table {
                        width: 100%;
                        border-collapse: collapse;
                        margin: 20px 0;
                        font-size: 16px;
                    }
                    table th, table td {
                        padding: 10px;
                        text-align: left;
                        border: 1px solid #ddd;
                    }
                    table th {
                        background-color: #4CAF50;
                        color: white;
                    }
                    table tr:nth-child(even) {
                        background-color: #f2f2f2;
                    }
                    table tr:hover {
                        background-color: #ddd;
                    }
                    .footer {
                        margin-top: 30px;
                        font-size: 14px;
                        color: #777;
                    }
                </style>
            </head>
            <body>
                <div>
                    <h3>Total number of Requests : {{ total_no_of_requests }}</h3>
                    <h3>Total number of Pending Requests : {{ requested_requests_count }}</h3>
                    <h3>Total number of Completed Requests : {{ completed_requests_count }}</h3>
                <div>

            <h2>Total Requests</h2>
            <table border="2">
            <tr>
                <th>Service Professional Name</th>
                <th>Service Professional Email</th>
                <th>Customer Name</th>
                <th>Service Type</th>
                <th>Service Status</th>
            </tr>
            {% for request in total_requests%}
            <tr>
                <td> {{professional_name}} </td>
                <td> {{professional_email}} </td>
                <td> {{customer_name}}
                <td> {{service_type}}</td>
                <td> {{request.service_status}}</td>
            <tr>
            {% endfor %}
            </table>

            <div class="footer">
                 <p>This is an automated email. Please do not reply to this message.</p>
            </div>

           

            </body>
            </html>
            '''

            template = Template(body)
            body = template.render(total_requests = total_requests, professional_name=professional_name,professional_email=professional_email,  service_type= service_type,total_no_of_requests=total_no_of_requests, requested_requests_count=requested_requests_count, completed_requests_count=completed_requests_count, customer_name=customer_name)


            msg = Message(subject = email_subject, recipients=['shreyasaxena2104@gmail.com'], body = email_body)
            msg.html = body
            mail.send(msg)

            return 'done'

@celery.task(ignore_result=False)
def create_csv():
    requests = ServiceRequest.query.filter_by(service_status = "Completed").all()
    file_path = './backend/static/file.csv'

    # Write the CSV file manually
    with open(file_path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Service ID', 'Customer ID', 'Professional ID', 'Date of Request', 'Remarks'])

        for r in requests:
            csvwriter.writerow([r.service_id, r.customer_id, r.professional_id, str(r.date_of_completion), r.remarks])

    with open(file_path, 'r') as f:
        csv_data = f.read()

    subject = 'CSV File'
    body = 'Hi, Please check the attachment'
    msg = Message(subject=subject, recipients=['shreyasaxena2104@gmail.com'], body=body)
    msg.attach('file.csv', 'text/csv', csv_data)

    mail.send(msg)
    return file_path

            