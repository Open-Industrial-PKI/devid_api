import json
from pyhsm.hsmclient import HsmClient

def list_objects_on_hsm(slot_num, pin, library_path):
    result = []
    with HsmClient(slot=slot_num, pin=pin, pkcs11_lib=library_path) as c:
        obj_list = c.get_objects()
        for obj in obj_list:
            object_info = {
                "label": obj.label,
                "class": obj.object_class,
                "id": obj.id,
                "attributes": obj.get_attributes()
            }
            result.append(object_info)
    return json.dumps(result)



if __name__ == "__main__":
    list_objects_on_hsm(
        library_path='/usr/lib/opensc-pkcs11.so',
        slot_num=0,
        pin='1234'
    )