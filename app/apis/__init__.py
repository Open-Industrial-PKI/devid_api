from .management_interface import api as mgmt_interface

from .Ldev_cert_service_interface import api as ldev_cert_interface
from .Ldev_key_service_interface import api as ldev_key_interface
from .Ldev_chain_service_interface import api as ldev_chain_interface

from .Idev_cert_service_interface import api as idev_cert_interface
from .Idev_key_service_interface import api as idev_key_interface
from .Idev_chain_service_interface import api as idev_chain_interface

from .highlevel_idev_service_interface import api as highlevel_idev_interface
from .highlevel_ldev_service_interface import api as highlevel_ldev_interface



from flask import Blueprint
from flask_restx import Api

blueprint = Blueprint("api", __name__)

api = Api(
    blueprint,
    title="IEEE 802.1 AR API",
    version="0.1",
    description="Interfaces to communicate with an entity, setup a device and manage DevIDs according to IEEE 802.1 AR"
)

#api.add_namespace(setup_interface, path="/setup")
api.add_namespace(mgmt_interface, path="/mgmt")

api.add_namespace(idev_cert_interface, path="/idev-cert")
api.add_namespace(idev_key_interface, path="/idev-key")
api.add_namespace(idev_chain_interface, path="/idev-chain")

api.add_namespace(ldev_cert_interface, path="/ldev-cert")
api.add_namespace(ldev_key_interface, path="/ldev-key")
api.add_namespace(ldev_chain_interface, path="/ldev-chain")

api.add_namespace(highlevel_idev_interface, path="/idev-highlvl")
api.add_namespace(highlevel_ldev_interface, path="/ldev-highlvl")