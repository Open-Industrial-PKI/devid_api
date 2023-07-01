from flask_restx import Namespace, Resource, fields

api = Namespace("LDevID-Chain", description="IEEE 802.1 AR LDevID Certificate Chain operations")

@api.route('/chain/<certificateIndex>', endpoint='ldevid-chain')
@api.doc(params={'certificateIndex': 'The certificateIndex of the certificate associated with the certificate chain.'})
class LDevIDChain(Resource):

    @api.doc("post")
    def post(self, certificateIndex):
        """LDevID certificate chain insert (7-2-12): A certificate chain to be associated with a certificateIndex"""
        return {"success": True,
                "status": "NotImplemented"}

    @api.doc("get")
    def get(self, certificateIndex):
        """LDevID certificate chain export (NOT STANDARDIZED): Exports a certificate chain associated to a certificateIndex"""
        return {"success": True,
                "status": "NotImplemented"}

    @api.doc("delete")
    def delete(self, certificateIndex):
        """LDevID certificate chain delete (7-2-14): The DevID module performs cryptographic zeroization on LDevID certificate chain material as part of the delete process"""

        return {"success": True,
                "status": "NotImplemented"}



