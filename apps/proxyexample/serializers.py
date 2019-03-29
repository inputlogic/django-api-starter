from rest_framework import serializers


'''
Example of generic non-model based serializer for use with proxy API call.
'''


class ProxyUserListSerialzier(serializers.Serializer):
    company = serializers.CharField(required=True)
    filter = serializers.CharField(required=True)
