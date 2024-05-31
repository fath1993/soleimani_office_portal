from django.core.management import base
import hmac
import hashlib


class Command(base.BaseCommand):
    def handle(self, *args, **options):
        # URL and key
        # url = "https://dl.dropboxusercontent.com/scl/fi/hql2ts33xbnllvtj80vfb/soleimani_office_portal.txt?rlkey=to4bzuk46abf52nyb5dbn64sg&dl=0"
        # key = "Uisl54d"
        # encoded_url = encode_url_with_key(url, key)
        # print("Encoded URL:", encoded_url)


        decoded_url = decode_url_with_key("89bae20e0bd83c45a02c85997c423aa0", "Uisl54d")
        print("Decoded URL:", decoded_url)




# Function to encode URL with a key using HMAC
def encode_url_with_key(url, key):
    encoded_url = hmac.new(key.encode('utf-8'), url.encode('utf-8'), hashlib.md5).hexdigest()
    return encoded_url


# Function to decode URL with a key using HMAC
def decode_url_with_key(encoded_url, key):
    decoded_url = hmac.new(key.encode('utf-8'), encoded_url.encode('utf-8'), hashlib.md5).hexdigest()
    return decoded_url


# encoded_url = encode_url_with_key(url, key)
# print("Encoded URL:", encoded_url)
#
#
# # Decode URL with key
# decoded_url = decode_url_with_key(encoded_url, key)
# print("Decoded URL:", decoded_url)
