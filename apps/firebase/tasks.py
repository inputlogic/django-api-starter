import logging

from workers import task


log = logging.getLogger(__name__)


@task()
def send_notification(registration_id, data):
    from firebase_admin import messaging
    from .libs import firebase_instance

    # See documentation on defining a message payload.
    # https://firebase.google.com/docs/reference/admin/python/firebase_admin.messaging#message
    message = messaging.Message(
        # data = { 'title': '..', 'body': '..' }
        notification=messaging.Notification(**data),
        token=registration_id,
    )

    # https://firebase.google.com/docs/cloud-messaging/send-message
    try:
        response = messaging.send(message)
        log.info('send_notification: {}'.format(response))
    except messaging.ApiCallError as e:
        log.error('send_notification failed! {} - {}'.format(e.code, e.message))
        log.exception(e)

