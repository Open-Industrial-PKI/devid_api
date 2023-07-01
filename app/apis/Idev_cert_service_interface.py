from flask_restx import Namespace, Resource, fields

api = Namespace("IDevID-Certificate", description="IEEE 802.1 AR IDevID Certificate related operations")

@api.route('/<certificateIndex>', endpoint='idevid-cert')
@api.doc(params={'certificateIndex': 'The certificateIndex of an IDevID certificate'})
class IDevIDCert(Resource):

    @api.doc("post")
    def post(self, certificateIndex):
        """Provision an IDevID certificate (NOT STANDARDIZED)"""
        return {"success": True,
                "status": "NotImplemented"}

    @api.doc("delete")
    def delete(self, certificateIndex):
        """IDevID certificate delete (NOT STANDARDIZED): This operation implicitly deletes any certificate chain associated with the deleted certificate, it does not
        remove the associated DevID secret -  The DevID module performs cryptographic zeroization on IDevID certificate material as part of the
        delete process"""
        return {"success": True,
                "status": "NotImplemented"}

    @api.doc("get")
    def get(self, certificateIndex):
        """IDevID certificate export (NOT STANDARDIZED): Exports a certificate associated to a certificateIndex"""
        return {"success": True,
                "status": "NotImplemented"}




