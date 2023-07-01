import json
import requests
from requests_pkcs12 import Pkcs12Adapter
from app.apis.adapters import logger
from app.apis.adapters.__config__ import Configuration

class EjbcaHealth:
    def __init__(self, base_url, p12_file, p12_pass):
        self.logger = logger.get_logger("EjbcaHealth")

        self.base_url = base_url
        self.p12_file = p12_file
        self.p12_pass = p12_pass



    def health_status(self):
        self.logger.info("--Check health status of EJBCA instance")
        # Create JSON payload
        up_and_running = False
        message = "Initial message"
        try:
            url = f'https://{self.base_url}/ejbca/ejbca-rest-api/v1/certificate/status'

            # Send request
            session = requests.Session()
            session.mount(url, Pkcs12Adapter(max_retries=3, pkcs12_filename=self.p12_file, pkcs12_password=self.p12_pass))
            response = session.get(
                url=url,
                headers={'Content-Type': 'application/json', 'Accept': 'application/json'},
                verify=False
            )
            response.raise_for_status()  # raise an HTTPError if status code is >= 400
            response = json.loads(response.text)
            if response['status'] == "OK":
                self.logger.info("-EJBCA up and running ✅")
                up_and_running = True
                message = "EJBCA up and running"
            else:
                self.logger.info("-EJBCA down ❌")
                message = "EJBCA down"

            #self.logger.info("--Response: {}".format(response))
        except requests.exceptions.HTTPError as err:
            self.logger.error("HTTP error occurred:", str(err))
            message = str(err)
        except requests.exceptions.RequestException as err:
            self.logger.error("An error occurred:", str(err))
            message = str(err)
        except (json.JSONDecodeError, OSError, KeyError) as err:
            self.logger.error(f"Error requesting certificate: {str(err)}")
            message = str(err)
        finally:
            return {'success': up_and_running, 'message': message}


if __name__ == "__main__":
    config = Configuration()
    health = EjbcaHealth(
        base_url=config.ejbca_url,
        p12_file=config.p12_auth_file_path,
        p12_pass=config.p12_auth_file_pwd,
    )
    health.health_status()