from urllib.parse import urlparse, urljoin
from decouple import config
from rest_framework import serializers

from core.utilities import calculate_file_hash
from .models import ScanFile, Scan;from django.db import transaction

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
            with transaction.atomic():
                scan_file = ScanFile.objects.create(**validated_data)
                Scan.objects.bulk_create_scan_for_av_in_avs(scan_file)
            return scan_file

    @staticmethod
    def get_file_hash(obj):
        return obj.sha_256

    @staticmethod
    def get_link(obj):
        link = urlparse(config('HOST') + '/api/files/')
        return urljoin(link.path, f'{obj.sha_256}/')



class ScanFileRetrieveSerializer(serializers.ModelSerializer):
    number_of_scanners = serializers.SerializerMethodField()
    scanned_with = serializers.SerializerMethodField()
    class Meta:
        model = ScanFile
        fields = 'file', 'sha_256', 'file_size', 'status', 'name', 'number_of_scanners', 'scanned_with'


    @staticmethod
    def get_number_of_scanners(obj):
        return obj.scan.filter(status=1).count()

    @staticmethod
    def get_scanned_with(obj):
        return [scanner.av_name for scanner in obj.scan.all()]





class ScanListSerializer(serializers.ModelSerializer):
    """Serializer for listing all scans with only av_name and short_result."""
    class Meta:
        model = Scan
        fields = ["av_name", "short_result"]

class ScanDetailSerializer(serializers.ModelSerializer):
    """Serializer for retrieving a single scan's full final_result."""
    class Meta:
        model = Scan
        fields = ["av_name", "final_result"]