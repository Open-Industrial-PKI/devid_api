from app.apis.adapters import logger

class Configuration:
    def __init__(self):
        self.logger = logger.get_logger("Configuration")

        # EJBCA URL and authentication
        self.ejbca_url = None
        self.p12_auth_file_path = None
        self.p12_auth_file_pwd = None

        # IDevID configuration for EJBCA
        self.certificate_profile_name_idev = None
        self.end_entity_profile_name_idev = None
        self.certificate_authority_name_idev = None
        self.ca_chain_url_idev = None

        self.idev_token_user = None
        self.idev_token_pw = None

        # LDevID configuration for EJBCA
        self.certificate_profile_name_ldev_basic = None
        self.end_entity_profile_name_ldev_basic = None
        self.certificate_authority_name_ldev_basic = None

        self.certificate_profile_name_ldev_opc_server = None
        self.end_entity_profile_name_ldev_opc_server = None
        self.certificate_authority_name_ldev_opc_server = None

        self.certificate_profile_name_ldev_azure = None
        self.end_entity_profile_name_ldev_azure = None
        self.certificate_authority_name_ldev_azure = None

        self.certificate_profile_name_ldev_aws = None
        self.end_entity_profile_name_ldev_aws = None
        self.certificate_authority_name_ldev_aws = None

        self.ldev_token_user = None
        self.ldev_token_pw = None

        self.hsm_pin = "1234"

        self.local_setup()

    def azure_setup(self):
        #self.logger.info("Using the Azure configuration")

        # EJBCA URL and authentication
        self.idev_ejbca_url = 'campuspki.germanywestcentral.cloudapp.azure.com'
        self.idev_p12_auth_file_path = '/home/admin/fhk_hmi_setup_v3.p12'
        self.idev_p12_auth_file_pwd = 'foo123'
        self.idev_ca_certificate = '/home/admin/certs/ManagementCA.cacert.pem'

        self.ldev_ejbca_url = 'campuspki.germanywestcentral.cloudapp.azure.com'
        self.ldev_p12_auth_file_path = '/home/admin/fhk_hmi_setup_v3.p12'
        self.ldev_p12_auth_file_pwd = 'foo123'

        self.idev_token_user = "testuser-idev-001"
        self.idev_token_pw = "foo123"

        # IDevID configuration for EJBCA
        self.certificate_profile_name_idev = 'DeviceIdentity-Raspberry'
        self.end_entity_profile_name_idev = 'KF-CS-EE-DeviceIdentity-Raspberry'
        self.certificate_authority_name_idev = 'KF-CS-HMI-2023-CA'
        self.ca_chain_url_idev = "https://campuspki.germanywestcentral.cloudapp.azure.com/ejbca/publicweb/webdist/certdist?cmd=cachain&caid=-1791256346&format=pem"
        # LDevID configuration for EJBCA
        self.certificate_profile_name_ldev_basic = 'DeviceIdentity-Raspberry'
        self.end_entity_profile_name_ldev_basic = 'KF-CS-EE-DeviceIdentity-Raspberry'
        self.certificate_authority_name_ldev_basic = 'KF-CS-HMI-2023-CA'

        self.ldev_token_user = "testuser-ldev-001"
        self.ldev_token_pw = "foo123"

    def local_setup(self):
        #self.logger.info("Using the Local configuration")

        # EJBCA URL and authentication
        #self.ejbca_url = 'ejbca-node1.local'
        self.idev_ejbca_url = '192.168.1.3'
        self.idev_p12_auth_file_path = '/home/admin/certs/rest-admin-idevid-02.p12'
        self.idev_p12_auth_file_pwd = 'foo123'
        self.idev_ca_certificate = False

        self.ldev_ejbca_url = '192.168.1.3'
        self.ldev_p12_auth_file_path = '/home/admin/certs/rest-admin-idevid-02.p12'
        self.ldev_p12_auth_file_pwd = 'foo123'

        # IDevID configuration for EJBCA
        self.certificate_profile_name_idev = 'EndEntityProfile-IDevId'
        self.end_entity_profile_name_idev = 'IDevId-EndEntity'
        self.certificate_authority_name_idev = 'IDevId-CA'
        self.ca_chain_url_idev = "https://192.168.1.3/ejbca/publicweb/webdist/certdist?cmd=cachain&caid=576048594&format=pem"

        self.idev_token_user = "testuser-001"
        self.idev_token_pw = "foo123"

        # LDevID configuration for EJBCA

        self.certificate_profile_name_ldev_basic = 'DeviceIdentity-Raspberry'
        self.end_entity_profile_name_ldev_basic = 'KF-CS-EE-DeviceIdentity-Raspberry'
        self.certificate_authority_name_ldev_basic = 'KF-CS-HMI-2023-CA'

        self.certificate_profile_name_ldev_opc_server = "EndEntityProfile-OpcUa-Server"
        self.end_entity_profile_name_ldev_opc_server = "EndEntity-OpcUa-Server"
        self.certificate_authority_name_ldev_opc_server = "OpcUa-CA"

        self.certificate_profile_name_ldev_azure = "EndEntityProfile-Azure"
        self.end_entity_profile_name_ldev_azure = "EndEntity-Azure"
        self.certificate_authority_name_ldev_azure = "CloudConnect-CA"

        self.certificate_profile_name_ldev_aws = "EndEntityProfile-Aws"
        self.end_entity_profile_name_ldev_aws = "EndEntity-Aws"
        self.certificate_authority_name_ldev_aws = "CloudConnect-CA"

        self.ldev_token_user = "testuser-ldev-001"
        self.ldev_token_pw = "foo123"
