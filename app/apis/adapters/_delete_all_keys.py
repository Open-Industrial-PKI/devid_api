from hsm_objects import HsmObjects
from app.apis.adapters.__config__ import Configuration

config = Configuration()

def main():
    hsm_objects = HsmObjects(
        slot_num=0,
        pin=config.hsm_pin
    )
    hsm_objects.delete_all_objects()


if __name__ == "__main__":
    main()