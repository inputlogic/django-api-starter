# from django.db import models


# class Webhook(models.Model):
#     url = models.URLField()
#     name = models.CharField(max_length=255)
#     app_name = models.CharField(max_length=32)
#     model_name = models.CharField(max_length=128, blank=True)
#     signal_type = models.CharField(max_length=32)
#     enabled = models.BooleanField(default=True)

#     class Meta:
#         unique_together = (('url', 'model_name', 'signal_type'), )

#     def __unicode__(self):
#         return u'%s' % self.signal_name

#     def __str__(self):
#         return self.signal_name
