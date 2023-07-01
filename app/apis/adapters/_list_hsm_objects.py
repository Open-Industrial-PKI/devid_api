from app.apis.adapters.__config__ import Configuration
from app.apis.adapters.hsm_objects import HsmObjects

config = Configuration()


def main():
    print("--- Print Objects ---")
    hsm_objects = HsmObjects(
        slot_num=0,
        pin=config.hsm_pin
    )
    print(hsm_objects.to_json())


    print("Number of private keys on HSM: {}".format(hsm_objects.count_keys(public=False)))
    print("Number of public keys on HSM: {}".format(hsm_objects.count_keys(private=False)))
    print("Number of certificates on HSM: {}".format(hsm_objects.coun_certificates()))

    print("Number of LDev keys on HSM: {}".format(hsm_objects.count_ldev_keys()))
    print("Number of IDev keys on HSM: {}".format(hsm_objects.count_idev_keys()))

    print("Number of LDev certs on HSM: {}".format(hsm_objects.count_ldev_certs()))
    print("Number of IDev certs on HSM: {}".format(hsm_objects.count_idev_certs()))




if __name__ == "__main__":
    main()