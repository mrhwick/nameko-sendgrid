from nameko.rpc import RpcProxy, rpc
from nameko.testing.services import worker_factory

def test_send_email():
    # create worker with mock dependencies
    