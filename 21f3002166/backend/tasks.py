
from jinja2 import Template
from flask import render_template
from celery.schedules import crontab
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os
import numpy as np
import matplotlib.pyplot as pt
import csv
import io
import string
from models import *
from cache import get_orders
import datetime
from sqlalchemy.orm import joinedload
from config import app as a
from config import smtp_server, port, smtp_username, smtp_password
from celeryconfig import app as celery

# celery = Celery('tasks', broker='redis://127.0.0.1:6379/0',
#                 enable_utc=False, timezone='Asia/Kolkata')


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(day_of_month=1, month_of_year='*', hour=6, minute=0),
                             monthly_report.s(), name='Monthly Report')
    sender.add_periodic_task(crontab(hour=13, minute=12),
                             send_reminder.s(), name='Reminder')


@celery.task
def monthly_report():
    from datetime import date
    orders = get_orders()
    c_month = str(date.today().month)
    orderlist = [{"id": order.id, "name": order.name, "order_value": order.total_value,
                  "order_date": order.order_timestamp[:8], "order_time":order.order_timestamp[9:18]} for order in orders
                 if order.order_timestamp[1:2] == c_month]
    sender = 'swastik01cs@gmail.com'
    receivers = []
    with a.app_context():
        receivers = [user.email for user in User.query.all()
                     if user.role == "storem"]

    msg = MIMEMultipart()
    msg['Subject'] = "Monthly Report"
    msg['From'] = sender
    # msg['To'] = receiver
    body = """
<h1>Monthly Activity Report</h1>
<!-- make a table to show orders -->
<table style="text-align: center;">
  <thead>
    <tr>
      <th>Order ID</th>
      <th>Order Date</th>
      <th>Order Time</th>
      <th>Customer Name</th>
      <th>Order Total</th>
    </tr>
  </thead>
  <tbody>
    {% for o in orderlist %}
    <tr>
      <td>{{ o.id }}</td>
      <td>{{ o.order_date }}</td>
      <td>{{ o.order_time }}</td>
      <td>{{ o.name }}</td>
      <td>{{ o.order_value }}</td>
    </tr>

    {% endfor %}
  </tbody>
</table>

"""
    tm = Template(body)
    tem = tm.render(orderlist=orderlist)

    msg.attach(MIMEText(tem, 'html'))

    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        for receiver in receivers:
            server.sendmail(sender, receiver, msg.as_string())
        server.close()
    print("Mail sent successfully")


@celery.task
def send_reminder():
    sender = "swastik01cs@gmail.com"

    with a.app_context():
        receivers = [user.email for user in User.query.all()
                     if user.role == "customer"]

    r = receivers
    print(r)
    msg = MIMEMultipart()
    msg['Subject'] = "Reminder"
    msg['From'] = sender
    # msg['To'] = receiver
    body = "It's 6'o clock 🕕! Time to calm down your cravings\n Hurry up order snacks\n EMarket"
    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        for receiver in receivers:
            server.sendmail(sender, receiver, msg.as_string())
        server.close()
    print("Mail sent successfully")



@celery.task
def csv_creator(path):
    with a.app_context():
        products = db.session.query(Product).options(
            joinedload(Product.section)).all()

    csvfile = io.StringIO()

    writer = csv.writer(csvfile)
    writer.writerow(['Id', 'Name', 'Price', 'ExpDate',
                    'Left Stock', 'Measuring Scale', 'Description', 'Category'])
    for product in products:
        writer.writerow([product.id, product.name, product.price, str(product.expdate),
                        product.quantity, product.ms, product.desc, product.section])
        print([product.id, product.name, product.price, product.expdate,
               product.quantity, product.ms, product.desc, product.section])
    csvfile.seek(0)

    # csv_f_path = 'D:\\EMarket V2\\EMarket\\src\\assets\\csv\products.csv'

    with open(path, 'w') as f:
        f.write(csvfile.getvalue())


@celery.task
def catwisesales():
    with a.app_context():
        t = Transaction.query.all()
        d = {}
        for i in t:
            p = Product.query.filter_by(id=i.product_id).options(
                joinedload(Product.section)).first().section
            p = str(p)
            if p not in d:
                d[p] = 1
            else:
                d[p] += 1
    pt.clf()
    cat = np.array(list(d.keys()))
    val = np.array(list(d.values()))
    filepath = os.getcwd()+"\\static\catwisesales.jpg"
    pt.title("Category Wise Sales")
    if os.path.exists(filepath):
        os.remove(filepath)
    print(os.getcwd())
    # pt.bar(cat,val)
    pt.pie(val, labels=cat, autopct='%1.1f%%')
    pt.savefig(filepath)
    pt.clf()


@celery.task
def timeseries():
    # with a.app_context():
    #     o = Order.query.all()
    o = get_orders()
    print("hii")
    daytime = ['Morning', 'AfterNoon', 'Evening', 'Night']
    d = {'Morning': 0, 'AfterNoon': 0, 'Evening': 0, 'Night': 0}
    for i in o:
        k = int(i.order_timestamp[9:11])
        if k >= 5 and k < 12:

            d[daytime[0]] += 1
        if k > 12 and k <= 17:

            d[daytime[1]] += 1
        if k > 17 and k <= 21:

            d[daytime[2]] += 1
        else:

            d[daytime[3]] += 1
    timeser = np.array(list(d.keys()))
    no_orders = np.array(list(d.values()))
    filepath = os.getcwd()+"\\static\order_timeseries.jpg"
    if os.path.exists(filepath):
        os.remove(filepath)

    pt.pie(no_orders, labels=timeser, autopct='%1.1f%%')
    pt.savefig(filepath)
    pt.clf()


@celery.task
def orderrange():

    # with a.app_context():
    #     o=Order.query.all()
    o = get_orders()
    d = dict()
    for i in o:
        d = {'Under ₹100': 0, 'Under ₹500': 0,
             'Under ₹1000': 0, 'Over ₹1000': 0}

        val = i.total_value
        print(type(val))
        if val < 100:
            d['Under ₹100'] += 1
        if val >= 100 and val < 500:
            d['Under ₹500'] += 1
        if val >= 500 and val < 1000:
            d['Under ₹1000'] += 1
        else:
            d['Over ₹1000'] += 1
    print(d)
    order_range = np.array(list(d.keys()))
    print(order_range)
    no_orders = np.array(list(d.values()))
    print(no_orders)
    filepath = os.getcwd()+"\\static\orange.jpg"
    if os.path.exists(filepath):
        os.remove(filepath)
    pt.pie(no_orders, labels=order_range, autopct='%1.1f%%')
    pt.savefig(filepath)

    return "hii"
