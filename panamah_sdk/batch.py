import base64
import hashlib
import os
import shutil
import json
from datetime import datetime

FILENAME_FORMAT = '%Y_%m_%d_%H_%M_%S_%f.pbt'


class Batch():
    def __init__(self, filename=None, force_existence=False):
        self.filename = filename
        if filename is not None:
            if force_existence:
                self.force_existence(filename)
            self.created_at = datetime.strptime(os.path.basename(
                filename), FILENAME_FORMAT) if self.filename_conforms(filename, FILENAME_FORMAT) else datetime.now()
            self.filename = os.path.basename(filename)
            self.operations = self.read_operations(filename)
        else:
            self.reset()

    @property
    def size(self):
        return len(self.json())

    @property
    def length(self):
        return len(self.operations)

    @property 
    def age(self):
        return (datetime.now() - self.created_at).total_seconds()

    def force_existence(self, filename):
        if not os.path.exists(filename):
            with open(filename, mode='w') as fp:
                fp.write('[]')

    def delete(self, directory):
        os.remove('%s/%s' % (directory, self.filename))

    def save(self, directory, filename=None):
        with open('%s/%s' % (directory, filename if filename is not None else self.filename), mode='w') as fp:
            return fp.write(json.dumps(self.operations))

    def move(self, source, destiny):
        shutil.move(src='%s/%s' % (source, self.filename),
                    dst='%s/%s' % (destiny, self.filename))

    def json(self):
        return json.dumps(self.operations)

    def read_operations(self, filename):
        content = self.read_content(filename)
        return json.loads(content) if content else []

    def read_content(self, filename):
        with open(filename, mode='r') as fp:
            return fp.read()

    def filename_conforms(self, filename, expected_format):
        try:
            datetime.strptime(os.path.basename(filename), expected_format)
            return True
        except:
            return False

    def append(self, operation):
        self.operations.append(operation)
        return self

    def remove(self, operation):
        self.operations.remove(operation)
        return self

    def reset(self):
        self.created_at = datetime.now()
        self.filename = self.created_at.strftime(FILENAME_FORMAT)
        self.operations = []

    def hash(self):
        return base64.b64encode(hashlib.sha1(self.json().encode('utf-8')).digest()).decode('utf-8')

    def __str__(self):
        return self.json()
