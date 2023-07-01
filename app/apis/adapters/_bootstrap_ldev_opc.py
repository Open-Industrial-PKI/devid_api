from app.apis.adapters.__config__ import Configuration
from app.apis.adapters.bootstrap_process import BootstrapDevId

config = Configuration()


def main():
    ldevid = BootstrapDevId(pin=config.hsm_pin, slot=0)
    ldevid.setup_ldev_id()
    ldevid.validate_idev_certifificate(ca_chain_url=config.ca_chain_url_idev)
    ldevid.create_key()
    ldevid.generate_csr()
    ldevid.request_cert(base_url=config.ldev_ejbca_url,
                        p12_file=config.ldev_p12_auth_file_path,
                        p12_pass=config.ldev_p12_auth_file_pwd,
                        certificate_profile_name=config.certificate_profile_name_ldev_opc_server,
                        end_entity_profile_name=config.end_entity_profile_name_ldev_opc_server,
                        certificate_authority_name=config.certificate_authority_name_ldev_opc_server,
                        token_user=config.ldev_token_user,
                        token_pw=config.ldev_token_pw)
    ldevid.import_certificate()


if __name__ == "__main__":
    main()
