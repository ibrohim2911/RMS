import time
import logging
from django.core.management.base import BaseCommand
from escpos.printer import Network
from hardware.models import PrinterJob

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Runs the asynchronous printer spooler'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting Printer Spooler..."))
        while True:
            try:
                # Get the oldest pending job
                job = PrinterJob.objects.filter(status='pending').order_by('created_at').first()
                if job:
                    job.status = 'printing'
                    job.save()

                    printer_ip = job.printer.ip_address
                    printer_port = job.printer.port or 9100

                    try:
                        self.stdout.write(f"Printing job {job.id} to {printer_ip}:{printer_port}")
                        # Initialize escpos Network printer
                        if printer_ip:
                            p = Network(printer_ip, port=printer_port)
                            p.text(job.payload)
                            p.cut()
                            p.close()
                        else:
                            raise Exception("No IP address provided for network printer.")

                        job.status = 'printed'
                        job.save()
                        self.stdout.write(self.style.SUCCESS(f"Job {job.id} printed successfully."))
                    except Exception as e:
                        job.status = 'failed'
                        job.error_message = str(e)
                        job.save()
                        self.stderr.write(self.style.ERROR(f"Failed to print job {job.id}: {e}"))
                else:
                    # Sleep if no jobs
                    time.sleep(1)
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Spooler error: {e}"))
                time.sleep(1)
