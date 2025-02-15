import subprocess
import time
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Starts Redis, Django runserver, Celery worker, Celery beat, and Flower.'

    def handle(self, *args, **kwargs):
        try:
            # Start Redis server
            redis_process = subprocess.Popen(['redis-server'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.stdout.write(self.style.SUCCESS('Started Redis server'))

            time.sleep(2)  # Give Redis some time to start

            # Start Django runserver
            runserver_process = subprocess.Popen(['python', 'manage.py', 'runserver'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.stdout.write(self.style.SUCCESS('Started Django runserver'))

            time.sleep(2)  # Ensure Django starts

            # Start Celery worker
            worker_process = subprocess.Popen(['celery', '-A', 'multiav_project', 'worker', '--loglevel=info'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.stdout.write(self.style.SUCCESS('Started Celery worker'))

            time.sleep(2)  # Allow some time for the worker to be ready

            # Start Celery beat
            beat_process = subprocess.Popen(['celery', '-A', 'multiav_project', 'beat', '--loglevel=info'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.stdout.write(self.style.SUCCESS('Started Celery beat'))

            time.sleep(2)  # Allow some time for the beat to be ready

            # Start Celery Flower
            flower_process = subprocess.Popen(['celery', '-A', 'multiav_project', 'flower'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.stdout.write(self.style.SUCCESS('Started Celery Flower'))

            # Keep the process running
            self.stdout.write(self.style.WARNING('All services started. Control-C to stop.'))
            while True:
                time.sleep(1)  # Keep the main thread alive

        except KeyboardInterrupt:
            self.stdout.write(self.style.ERROR('Stopping services...'))

        finally:
            # Terminating all processes when the command is interrupted
            redis_process.terminate()
            runserver_process.terminate()
            worker_process.terminate()
            beat_process.terminate()
            flower_process.terminate()
            self.stdout.write(self.style.SUCCESS('All services stopped.'))