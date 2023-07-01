from flask_restx import Namespace, Resource, fields
from app.apis.adapters.__config__ import Configuration
from app.apis.adapters import ejbca_health
from app.apis.adapters.hsm_objects import HsmObjects

config = Configuration()

api = Namespace("mgmt", description="IEEE 802.1 ARManagement related operations")

@api.route('/logs/', endpoint='logs')
class Logs(Resource):

    @api.doc("get")
    def get(self):
        """Get the logs of the DevID Management Interface"""
        return {"success": True,
                "status": "NotImplemented"}

@api.route('/dev-id-enumeration', endpoint='dev-id-enum')
class DevIDCertEnable(Resource):

    @api.doc("get")
    def get(self):
        """DevID certificate enumeration (7.2.3)"""
        # A table containing, for each certificate:
        #    — The certificateIndex,
        #    — The associated keyIndex,
        #    — A value indicating if the certificate is enabled,
        #    — A value indicating if the certificate is an IDevID certificate, and
        #    — The certificate itself, DER encoded as specified in RFC 5280.
        return {"success": True,
                "status": "NotImplemented"}

@api.route('/sign/<keyIndex>/<data>', endpoint='sign')
@api.doc(params={'keyIndex': 'The keyIndex of the DevID',
                 'data': 'Data to be signed'})
class Sign(Resource):

    @api.doc("post")
    def post(self, keyIndex, state):
        """DevID key enable/disable (7.2.7)"""
        # This operation allows the device administrator to control the use of DevID keys, and to maintain a measure
        # of privacy by limiting exposure of the device’s cryptographic identity.
        return {"success": True,
                "status": "NotImplemented"}

@api.route('/status/rest', endpoint='status-rest')
class RestStatus(Resource):

    @api.doc("post")
    def post(self):
        """Status of the REST API"""
        return {"success": True,
                "message": "Rest Interface is online"}

@api.route('/status/hsm', endpoint='status-hsm')
class HsmStatus(Resource):

    @api.doc("post")
    def post(self):
        """Status of the HSM"""
        return {"success": True,
                "message": "NotImplemented"}

@api.route('/status/idevid', endpoint='status-idevid')
class IDevIdStatus(Resource):

    @api.doc("post")
    def post(self):
        """Status of the IDevID"""
        return {"success": True,
                "message": "NotImplemented"}

@api.route('/status/ldevid', endpoint='status-ldevid')
class LDevIdStatus(Resource):

    @api.doc("post")
    def post(self):
        """Status of the LDevID"""
        return {"success": True,
                "message": "NotImplemented"}

@api.route('/status/ejbca', endpoint='status-ejbca')
class EjbcaStatusStatus(Resource):

    @api.doc("post")
    def post(self):
        """Status of the EJBCA instance"""
        try:
            config = Configuration()
            health = ejbca_health.EjbcaHealth(
                base_url=config.ejbca_url,
                p12_file=config.p12_auth_file_path,
                p12_pass=config.p12_auth_file_pwd,
            )
            status = health.health_status()
            return {"success": status['success'],
                    "message": status['message']}
        except Exception as err:
            return {"success": False,
                    "message": str(err)}

@api.route('/delete/keys-all', endpoint='delete-keys-all')
class DeleteAllKeys(Resource):

    @api.doc("delete")
    def delete(self):
        """Delete all keys on the HSM"""
        try:
            hsm_objects = HsmObjects(
                slot_num=0,
                pin=config.hsm_pin
            )
            cnt_deleted_objects = hsm_objects.delete_all_objects()
            return {"success": True,
                    "message": "Number of objects deleted: {}".format(cnt_deleted_objects)}
        except Exception as err:
            return {"success": False,
                    "message": str(err)}

@api.route('/delete/keys-ldev', endpoint='delete-keys-ldev')
class DeleteLDevKeys(Resource):

    @api.doc("delete")
    def delete(self):
        """Delete all LDev keys on the HSM"""
        try:
            hsm_objects = HsmObjects(
                slot_num=0,
                pin=config.hsm_pin
            )
            cnt_deleted_objects = hsm_objects.delete_objects_by_type("ldev", 3)
            return {"success": True,
                    "message": "Number of LDev objects deleted: {}".format(cnt_deleted_objects)}
        except Exception as err:
            return {"success": False,
                    "message": str(err)}

@api.route('/dev-id-cert/<certificateIndex>/<state>', endpoint='dev-id-cert')
@api.doc(params={'certificateIndex': 'The certificateIndex of the DevID',
                 'state': 'The desired state of a certificateIndex'})
class DevIDKeyEnable(Resource):

    @api.doc("post")
    def post(self, certificateIndex, state):
        """DevID key enable/disable (7-2-6): This operation allows the device administrator to disable use of a DevID without disabling the associated key, which might be in use by a different DevID"""
        return {"success": True,
                "status": "NotImplemented"}

@api.route('/dev-id-key/<keyIndex>/<state>', endpoint='dev-id-key')
@api.doc(params={'keyIndex': 'The keyIndex of the DevID',
                 'state': 'The desired state of a keyIndex'})
class DevIDCertEnable(Resource):

    @api.doc("post")
    def post(self, keyIndex, state):
        """DevID key enable/disable (7.2.7)"""
        # This operation allows the device administrator to control the use of DevID keys, and to maintain a measure
        # of privacy by limiting exposure of the device’s cryptographic identity.
        return {"success": True,
                "status": "NotImplemented"}


