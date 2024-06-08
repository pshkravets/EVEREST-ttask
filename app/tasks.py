import logging

from time import sleep
from celery import shared_task

from models import db, Order

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename='status.log'
)


@shared_task(name='tasks.order_status_changing')
def order_status_changing(order_id):
    sleep(20)
    order = Order.query.get(order_id)
    order.status = 'Delivered'
    db.session.commit()
    logging.info(f'Order {order_id} changed status to {order.status}')
    db.session.close()
