from azure.iot.device import ProvisioningDeviceClient, X509
from azure.iot.device import IoTHubDeviceClient
from app.apis.adapters import logger
import time


# https://github.com/Azure/azure-iot-sdk-python/blob/main/samples/async-hub-scenarios/provision_x509.py

class AzureDpsClient:
    def __init__(self, provisioning_host, id_scope, registration_id, cert_file, key_string):
        self.logger = logger.get_logger("AzureDpsClient")

        self.provisioning_host = provisioning_host
        self.id_scope = id_scope
        self.registration_id = registration_id
        self.cert_file = cert_file
        self.key_string = key_string
        self.X509 = None

        self.create_cert_object()

    def create_cert_object(self):
        # Load the device's certificate and private key
        with open(self.cert_file, "rb") as f:
            cert = f.read()

        # Create an X.509 certificate object
        self.x509 = X509(cert_file=cert)

    def register_device(self):

        # Create a provisioning device client
        provisioning_device_client = ProvisioningDeviceClient.create_from_x509_certificate(
            provisioning_host=self.provisioning_host,
            registration_id=self.registration_id,
            id_scope=self.id_scope,
            x509=self.x509,
        )

        # Register the device with Azure DPS
        registration_result = provisioning_device_client.register()

        self.send_telemtry_data(registration_result)

        # Return the registration result
        return {
            "status": registration_result.status,
            "assigned_hub": registration_result.registration_state.assigned_hub,
            "device_id": registration_result.registration_state.device_id
        }

    def send_telemtry_data(self, registration_result):
        if registration_result.status == "assigned":
            self.logger.info("Will send telemetry from the provisioned device")
            # Create device client from the above result
            device_client = IoTHubDeviceClient.create_from_x509_certificate(
                x509=self.x509,
                hostname=registration_result.registration_state.assigned_hub,
                device_id=registration_result.registration_state.device_id,
            )

            # Connect the client.
            device_client.connect()

            for i in range(1, 2):
                self.logger.info("sending message #" + str(i))
                device_client.send_message("test payload message " + str(i))
                time.sleep(1)
            return 0, f"{registration_result.registration_state.device_id}"

        else:
            self.logger.info("Can not send telemetry from the provisioned device")
            return 1, "Can not send telemetry from the provisioned device"


def main():
    register = AzureDpsClient(provisioning_host="DeviceProvisioning.azure-devices.net",
                              id_scope="0ne009BEB86",
                              registration_id="Testdevice_01",
                              cert_file="/home/admin/certs/my_cert_3443.pem",
                              key_string="pkcs11:model=PKCS%2315;manufacturer=unknown;serial=0000;token=JavaCard%20isoApplet%20%28User%20PIN%29;id=%10%1F%15%A6%7F%00%00%00%10%00%00%00%00%00%00%00;object=ldev_pvt_key_3443;type=private;pinvalue=1234;")

    register.register_device()

if __name__ == "__main__":
    main()