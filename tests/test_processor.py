import os
import shutil
from time import sleep
from unittest import main, mock, TestCase
from panamah_sdk.processor import BatchProcessor, BATCH_MAX_LENGTH, BATCH_MAX_SIZE, BATCH_MAX_AGE, ROOT_PATH, ACCUMULATED_PATH, SENT_PATH
from panamah_sdk.models.base import Model, StringField
from panamah_sdk.models.definitions import PanamahHolding, PanamahAcesso, PanamahSecao
from .server import start as start_test_server, stop as stop_test_server, set_next_response, clear_next_response


def test_expiration(self, by_max_length=False, by_max_size=False, by_max_age=False):
    holding = PanamahHolding(id='1234', descricao='teste')
    acesso = PanamahAcesso(id='4321', funcionario_ids=['1', '2'])
    secao = PanamahSecao(id='5555', codigo='6666', descricao='teste')

    b = BatchProcessor('auth', 'secret', '12345', batch_max_length=1 if by_max_length else 999999,
                       batch_max_size=80 if by_max_size else 99999 * 1024, batch_max_age=.5 if by_max_age else 9999999999)

    with mock.patch.object(b, 'send_accumulated_batches') as send_accumulated_batches_method:

        self.assertFalse(b.current_batch_expired())

        b.save(secao)

        if (by_max_age):
            sleep(.6)

        self.assertTrue(b.current_batch_expired())
        self.assertFalse(b.accumulated_batch_exists())
        batch_name = b.current_batch.get_filename_by_created_date()

        b.process()

        self.assertTrue(b.accumulated_batch_exists())
        self.assertTrue(os.path.exists('%s/%s' %
                                       (ACCUMULATED_PATH, batch_name)))
        self.assertEqual(len(b.get_accumulated_batches()), 1)
        self.assertEqual(b.current_batch.length, 0)

        b.save(holding)

        if (by_max_age):
            sleep(.6)

        b.process()

        self.assertEqual(send_accumulated_batches_method.call_count, 1)
        self.assertEqual(len(b.get_accumulated_batches()), 2)

        b.save(acesso)        
        
        if (by_max_age):
            sleep(.6)

        b.process()

        self.assertEqual(send_accumulated_batches_method.call_count, 2)
        self.assertEqual(len(b.get_accumulated_batches()), 3)


class TestStream(TestCase):
    def setUp(self):
        if os.path.exists(ROOT_PATH):
            shutil.rmtree(ROOT_PATH)

    def test_initialization_and_accumulation(self):
        holding = PanamahHolding(id='1234', descricao='teste')
        acesso = PanamahAcesso(id='4321', funcionario_ids=['1', '2'])
        secao = PanamahSecao(id='5555', codigo='6666', descricao='teste')

        b = BatchProcessor('auth', 'secret', '12345')

        self.assertTrue(os.path.exists(ROOT_PATH))
        self.assertTrue(os.path.exists(ACCUMULATED_PATH))
        self.assertTrue(os.path.exists(SENT_PATH))

        b.save(holding)

        self.assertEqual(b.current_batch.length, 1)
        self.assertEqual(b.current_batch.size, 83)
        sleep(.5)
        self.assertAlmostEqual(b.current_batch.age, 0.5, delta=0.2)

        b.save(acesso)

        self.assertEqual(b.current_batch.length, 2)
        self.assertEqual(b.current_batch.size, 174)
        sleep(.5)
        self.assertAlmostEqual(b.current_batch.age, 1, delta=0.2)

        b.save(secao)

        self.assertEqual(b.current_batch.length, 3)
        self.assertEqual(b.current_batch.size, 273)
        sleep(.5)
        self.assertAlmostEqual(b.current_batch.age, 1.5, delta=0.2)

    def test_expiration_by_max_length(self):
        test_expiration(self, by_max_length=True)

    def test_expiration_by_max_size(self):
        test_expiration(self, by_max_size=True)

    def test_expiration_by_max_age(self):
        test_expiration(self, by_max_age=True)

if __name__ == '__main__':
    main()
