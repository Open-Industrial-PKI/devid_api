from flask_restx import Namespace, Resource, fields

api = Namespace("LDevID-Key", description="IEEE 802.1 AR LDevID Key related operations")

@api.route('/<keyIndex>', endpoint='ldevid-key')
@api.doc(params={'keyIndex': 'The keyIndex of the LDevID'})
class LDevIDKey(Resource):

    @api.doc("delete")
    def delete(self, keyIndex):
        """LDevID key delete (7-2-10): The DevID module performs cryptographic zeroization on LDevID key storage as part of the delete process, removing both private and public key material"""
        return {"success": True,
                "status": "NotImplemented"}

@api.route('/generate/<keyIndex>', endpoint='ldevid-key-generate')
@api.doc(params={'keyIndex': 'The keyIndex of the LDevID'})
class LDevIDKeyGenerate(Resource):

    @api.doc("post")
    def post(self, keyIndex):
        """LDevID key generate (7-2-8): This operation allows the device administrator to generate an additional LDevID key within the DevID module - Newly generated keys are disabled and need to be explicitly enabled before use"""
        return {"success": True,
                "status": "NotImplemented"}

@api.route('/insert/<keyIndex>', endpoint='ldevid-key-insert')
@api.doc(params={'keyIndex': 'The keyIndex of the LDevID'})
class LDevIDKeyInsert(Resource):
    @api.doc("post")
    def post(self, keyIndex):
        """LDevID key insert (7-2-9): This operation allows the device administrator to insert an externally generated LDevID key into the DevID module"""
        return {"success": True,
                "status": "NotImplemented"}