import firebase_admin

from django.conf import settings
from firebase_admin import credentials


cred = credentials.Certificate(settings.GOOGLE_APPLICATION_CREDENTIALS)
firebase_instance = firebase_admin.initialize_app(cred)
