import os
import shutil
import json
from datetime import datetime

FILENAME_FORMAT = '%Y_%m_%d_%H_%M_%S_%f.pbt'

class Batch():
    def __init__(self, filename=None):
        self.filename = filename
        self.content = None
        self.operations = []
        if filename is not None:
            self.created_at = datetime.strptime(os.path.basename(filename), FILENAME_FORMAT) if self.filename_conforms(filename, FILENAME_FORMAT) else datetime.now()
            self.filename = os.path.basename(filename)
            self.content = self.read_content(filename)
        else:
            self.created_at = datetime.now()
            self.filename = self.created_at.strftime(FILENAME_FORMAT)

    def delete(self, directory):
        os.remove('%s/%s' % (directory, self.filename))

    def save(self, directory, filename=None):
        with open('%s/%s' % (directory, filename if filename is not None else self.filename), mode='w') as fp:
            return fp.write(self.content)        

    def move(self, source, destiny):
        shutil.move(src='%s/%s' % (source, self.filename), dst='%s/%s' % (destiny, self.filename))

    def json(self):
        if self.content:
            return json.loads(self.content)

    def read_content(self, filename):
        with open(filename, mode='r') as fp:
            return fp.read()

    def filename_conforms(self, filename, expected_format):
        try:
            datetime.strptime(os.path.basename(filename), expected_format)
            return True
        except:
            return False

    def __str__(self):
        return self.content if self.content else super().__str__()
