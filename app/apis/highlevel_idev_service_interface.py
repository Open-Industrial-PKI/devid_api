from flask_restx import Namespace, Resource
from app.apis.adapters.hsm_objects import HsmObjects
from app.apis.adapters.bootstrap_process import BootstrapDevId
from app.apis.adapters.cert_handler import CertHandler
from flask import jsonify
from app.apis.adapters.__config__ import Configuration

config = Configuration()



api = Namespace("Highlevel-IDevID", description="Highlevel REST API Calls for the IDevID module")

@api.route('/delete', endpoint='highlvl-idev-del')
class HighLvlIDevDelete(Resource):

    @api.doc("delete")
    def delete(self):
        """Only for demonstration purpose: Delete the actual IDevID (key + cert)"""
        try:
            del_idev = HsmObjects(slot_num=0,
                              pin=config.hsm_pin)
            del_idev.delete_idev_objects()
            return {"success": True,
                    "message": "Keys deleted"}
        except Exception as err:
            return {"success": False,
                    "message": str(err)}


@api.route('/validate', endpoint='highlvl-idev-val')
class HighLvlIDevValidate(Resource):

    @api.doc("post")
    def post(self):
        """Only for demonstration purpose: Delete the actual IDevID cert"""
        try:
            idevid = BootstrapDevId(pin=config.hsm_pin, slot=0)
            valid = idevid.validate_idev_certifificate(
                ca_chain_url=config.ca_chain_url_idev)
            return {"success": True,
                    "message": "Validation checked",
                    "valid": valid}
        except Exception as err:
            return {"success": False,
                    "message": str(err),
                    "valid": None}

@api.route('/provision', endpoint='highlvl-idev-prov')
class HighLvlIDevProvision(Resource):

    @api.doc("post")
    def post(self):
        """Only for demonstration purpose: Provision a new IDevID (key + cert)"""
        try:
            idevid = BootstrapDevId(pin=config.hsm_pin, slot=0)
            idevid.setup_idev_id()
            idevid.create_key()
            idevid.generate_csr(o="Keyfactor", ou="IoT-Department", c="DE", pseudonym="Wonderdevice 2.0")
            idevid.request_cert(base_url=config.idev_ejbca_url,
                                p12_file=config.idev_p12_auth_file_path,
                                p12_pass=config.idev_p12_auth_file_pwd,
                                certificate_profile_name=config.certificate_profile_name_idev,
                                end_entity_profile_name=config.end_entity_profile_name_idev,
                                certificate_authority_name=config.certificate_authority_name_idev,
                        token_user=config.idev_token_user,
                        token_pw=config.idev_token_pw)
            idevid.import_certificate()
            key_count = idevid.hsm_key_count()
            return {"success": True,
                    "message": "Bootstrap done",
                    "hsm_key_cnt": key_count}
        except Exception as err:
            return {"success": False,
                    "message": str(err),
                    "hsm_key_cnt": None}



@api.route('/actual', endpoint='highlvl-idev-get')
class HighLvlIDevActual(Resource):
    @api.doc("get")
    def get(self):
        """Only for demonstration purpose: Provide the content of the actual IDevID certificate"""
        try:
            slot_num=0
            pin="1234"
            hsm_objects = HsmObjects(
                slot_num=slot_num,
                pin=pin
            )
            hsm_idev_id = hsm_objects.get_actual_idev_id()

            export_cert = CertHandler(
                pin=pin,
                cert_id=hsm_idev_id,
            )
            export_cert.export_certificate(output_directory="/home/admin/")
            actual_idev = export_cert.parse_certificate()
            data = {"success": True,
                    "message": "IDevId with the HSM ID {}".format(hsm_idev_id),
                    "data": actual_idev}
            return jsonify(data)
        except Exception as err:
            return {"success": False,
                    "message": str(err),
                    "data": None}
