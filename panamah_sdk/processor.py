import os
import hashlib
import glob
from threading import Thread
from datetime import datetime
from .client import StreamClient
from .batch import Batch
from .exceptions import DataException

ROOT_PATH = './.panamah'
ACCUMULATED_PATH = ROOT_PATH + '/accumulated'
SENT_PATH = ROOT_PATH + '/sent'


class BatchProcessor(Thread):
    def __init__(self, authorization_token, secret, assinante_id):
        Thread.__init__(self, daemon=True)
        self.client = StreamClient(authorization_token, secret, assinante_id)
        self.current_batch = None
        self.last_batch_hash = None

    def run(self):
        self.initialize_structure()
        self.keep_processing()

    def initialize_structure(self):
        if not os.path.exists(ACCUMULATED_PATH):
            os.makedirs(ACCUMULATED_PATH)
        if not os.path.exists(SENT_PATH):
            os.makedirs(SENT_PATH)

    def keep_processing(self):
        if self.accumulated_batch_exists():
            self.send_accumulated_batches()
        self.watch_current_batch()
        self.delete_old_batches()

    def accumulated_batch_exists(self):
        return len([file for file in os.listdir(ACCUMULATED_PATH) if file.endswith('.pbt')]) > 0

    def send_accumulated_batches(self):
        batches = self.get_accumulated_batches()
        for batch in batches:
            response = self.client.post('/stream/data', batch.json())
            if response.status_code == 200:
                response_data = response.json()
                if hasattr(response_data, 'falhas'):
                    self.recover_from_failures(batch, response_data.falhas)
                    break
                else:
                    batch.move(source=ACCUMULATED_PATH, destiny=SENT_PATH)
            else:
                raise DataException()

    def watch_current_batch(self):
        if self.current_batch_expired():
            self.accumulate_current_batch()
        else:
            self.write_changes_to_current_batch()

    def delete_old_batches(self):
        sent_batches = [Batch(filename='%s/%s' % (SENT_PATH, file))
                        for file in os.listdir(SENT_PATH) if file.endswith('.pbt')]
        old_batches = [batch for batch in sent_batches if (
            datetime.now() - batch.created_at).total_seconds() > 24 * 60 * 60]
        if len(old_batches) > 0:
            for batch in old_batches:
                batch.delete(SENT_PATH)

    def current_batch_expired(self):
        def expired_by_count():
            return self.current_batch.length >= 500

        def expired_by_size():
            return self.current_batch.size >= 5 * 1024

        def expired_by_time():
            return self.current_batch.created_at >= 5 * 60 * 1000

        return expired_by_count() or expired_by_size() or expired_by_time()

    def accumulate_current_batch(self):
        if self.current_batch.length > 0:
            self.current_batch.save(directory=ACCUMULATED_PATH)
            self.current_batch.reset()

    def write_changes_to_current_batch(self):
        self.current_batch_hash = self.current_batch.hash()
        if self.current_batch_hash != self.last_batch_hash:
            self.current_batch.save(
                directory=ROOT_PATH,
                filename='current.pbt'
            )
            self.last_batch_hash = self.current_batch.hash()

    def get_accumulated_batches(self):
        return [Batch(filename='%s/%s' % (ACCUMULATED_PATH, file))
                for file in os.listdir(ACCUMULATED_PATH) if file.endswith('.pbt')]

    def recover_from_failures(self, batch, failures):
        return NotImplementedError
