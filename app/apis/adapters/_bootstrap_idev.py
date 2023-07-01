from app.apis.adapters.__config__ import Configuration
from app.apis.adapters.bootstrap_process import BootstrapDevId

config = Configuration()


def main():
    idevid = BootstrapDevId(pin=config.hsm_pin, slot=0)
    idevid.setup_idev_id()
    idevid.create_key()
    idevid.generate_csr()
    idevid.request_cert(base_url=config.idev_ejbca_url,
                        p12_file=config.idev_p12_auth_file_path,
                        p12_pass=config.idev_p12_auth_file_pwd,
                        certificate_profile_name=config.certificate_profile_name_idev,
                        end_entity_profile_name=config.end_entity_profile_name_idev,
                        certificate_authority_name=config.certificate_authority_name_idev,
                        token_user=config.idev_token_user,
                        token_pw=config.idev_token_pw,
                        ca_certificate=config.idev_ca_certificate)
    idevid.import_certificate()


if __name__ == "__main__":
    main()
