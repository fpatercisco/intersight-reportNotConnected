#!/usr/bin/python3
#
# Report all targets that don't have status=Connected and the reason why
#
# API key must be in ./api-key.txt
# API secret must be in ./api-secret.pem
#

import intersight
import re

def get_api_client(api_key_id, api_secret_file, endpoint="https://intersight.com"):
    with open(api_secret_file, 'r') as f:
        api_key = f.read()

    if re.search('BEGIN RSA PRIVATE KEY', api_key):
        # API Key v2 format
        signing_algorithm = intersight.signing.ALGORITHM_RSASSA_PKCS1v15
        signing_scheme = intersight.signing.SCHEME_RSA_SHA256
        hash_algorithm = intersight.signing.HASH_SHA256

    elif re.search('BEGIN EC PRIVATE KEY', api_key):
        # API Key v3 format
        signing_algorithm = intersight.signing.ALGORITHM_ECDSA_MODE_DETERMINISTIC_RFC6979
        signing_scheme = intersight.signing.SCHEME_HS2019
        hash_algorithm = intersight.signing.HASH_SHA256

    configuration = intersight.Configuration(
        host=endpoint,
        signing_info=intersight.signing.HttpSigningConfiguration(
            key_id=api_key_id,
            private_key_path=api_secret_file,
            signing_scheme=signing_scheme,
            signing_algorithm=signing_algorithm,
            hash_algorithm=hash_algorithm,
            signed_headers=[
                intersight.signing.HEADER_REQUEST_TARGET,
                intersight.signing.HEADER_HOST,
                intersight.signing.HEADER_DATE,
                intersight.signing.HEADER_DIGEST,
            ]
        )
    )
    return intersight.ApiClient(configuration)



if __name__ == '__main__':
    from intersight.api import asset_api

    with open('./api-key.txt', 'r') as keyfile:
        api_key = keyfile.read().strip()

    api_secret_file='./api-secret.pem'

    api_client=get_api_client(api_key, api_secret_file)
    asset_api_instance = asset_api.AssetApi(api_client)

    api_result=asset_api_instance.get_asset_target_list()

    for target in api_result.results:
        if target.status != 'Connected':
            print(target.name + ' (SN ' + str(target.target_id) + ' IP ' + \
                  str(target.ip_address) + ') is not connected to intersight (' + \
                  target.status + ': ' + target.status_error_reason + ')')
