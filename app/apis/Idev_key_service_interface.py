from flask_restx import Namespace, Resource, fields

api = Namespace("IDevID-Key", description="IEEE 802.1 AR IDevID Key related operations")

@api.route('/<keyIndex>', endpoint='idevid-key')
@api.doc(params={'keyIndex': 'The keyIndex of the IDevID'})
class IDevIDKey(Resource):

    @api.doc("delete")
    def delete(self, keyIndex):
        """IDevID key delete (7-2-10): The DevID module performs cryptographic zeroization on IDevID key storage as part of the delete process, removing both private and public key material"""
        return {"success": True,
                "status": "NotImplemented"}

@api.route('/generate/<keyIndex>', endpoint='idevid-key-generate')
@api.doc(params={'keyIndex': 'The keyIndex of the IDevID'})
class IDevIDKeyGenerate(Resource):

    @api.doc("post")
    def post(self, keyIndex):
        """IDevID key generate (NOT STANDARDIZED): This operation allows the device administrator to generate an  IDevID key within the DevID module - Newly generated keys are disabled and need to be explicitly enabled before use"""
        return {"success": True,
                "status": "NotImplemented"}