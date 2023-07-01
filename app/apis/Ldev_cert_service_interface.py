from flask_restx import Namespace, Resource, fields

api = Namespace("LDevID-Certificate", description="IEEE 802.1 AR LDevID Certificate related operations")

@api.route('/<certificateIndex>', endpoint='ldevid-cert')
@api.doc(params={'certificateIndex': 'The certificateIndex of an LDevID certificate'})
class LDevIDCert(Resource):

    @api.doc("post")
    def post(self, certificateIndex):
        """Provision an LDevID certificate"""
        return {"success": True,
                "status": "NotImplemented"}

    @api.doc("delete")
    def delete(self, certificateIndex):
        """LDevID certificate delete (7-2-13): This operation implicitly deletes any certificate chain associated with the deleted certificate, it does not
        remove the associated DevID secret - This operation does not delete an IDevID certificate even if identified
        by the certificateIndex - The DevID module performs cryptographic zeroization on LDevID certificate material as part of the
        delete process"""
        return {"success": True,
                "status": "NotImplemented"}

    @api.doc("get")
    def get(self, certificateIndex):
        """LDevID certificate export (NOT STANDARDIZED): Exports a certificate associated to a certificateIndex"""
        return {"success": True,
                "status": "NotImplemented"}




