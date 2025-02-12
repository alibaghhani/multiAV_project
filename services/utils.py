
class FileManager:

    @staticmethod
    def collect_results(file_obj):
        scans = file_obj.scan.all()

        if scans.count() == settings.COUNT_OF_SCANNERS:
            return list(scans.values_list('short_result', flat=True))

        return None

    def save_file_result(self, file_obj):
        file_obj.status = 'infected' if 'infected' in self.collect_results(file_obj) else 'clean'
        file_obj.save()