from urllib.parse import urlparse, urljoin
from django.http import Http404

from rest_framework import serializers

from core.utilities import calculate_file_hash
from .models import ScanFile, Scan

class ScanFileCreateSerializer(serializers.ModelSerializer):
    file_hash = serializers.SerializerMethodField()
    link = serializers.SerializerMethodField()


    class Meta:
        model = ScanFile
        fields = 'file', 'file_hash', 'link'


    def create(self, validated_data):


        file = validated_data.get('file')

        file_hash = calculate_file_hash(file)

        try:
            return ScanFile.objects.get(sha_256=file_hash)
        except Exception:
            scan_file = ScanFile.objects.create(**validated_data)
            Scan.objects.bulk_create_scan_for_av_in_avs(scan_file)
            return scan_file

    @staticmethod
    def get_file_hash(obj):
        return obj.sha_256

    @staticmethod
    def get_link(obj):
        link = urlparse('http://127.0.0.1:8000/api/file/')
        return urljoin(link.path, f'{obj.sha_256}/')