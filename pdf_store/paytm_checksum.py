import paytmchecksum

def generate_checksum(param_dict, merchant_key):
    """
    Generates a checksum for the given parameters using the merchant key.
    """
    return paytmchecksum.generateSignature(param_dict, merchant_key)

def verify_checksum(param_dict, merchant_key, checksum):
    """
    Verifies the checksum for the given parameters.
    """
    return paytmchecksum.verifySignature(param_dict, merchant_key, checksum)
