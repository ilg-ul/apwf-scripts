import sys
import flickrapi

from ilg.apwf.flickr import api_key, api_secret

# -----------------------------------------------------------------------------

def main(argv):

    print 'Authorise Flickr application.'
    # api_key = raw_input("Press enter the api key: ")
    # api_secret = raw_input("Press enter the api secret: ")
    
    flickr = flickrapi.FlickrAPI(api_key, api_secret)

    flickr.authenticate_via_browser(perms='write')
    print 'Authorised for user "{0}" "{1}" ({2}) for {3}.'.format(
            flickr.flickr_oauth.oauth_token.username,
            flickr.flickr_oauth.oauth_token.fullname,
            flickr.flickr_oauth.oauth_token.user_nsid,
            flickr.flickr_oauth.oauth_token.access_level)
    
    return


# -----------------------------------------------------------------------------

if __name__ == '__main__':
    sys.exit(main(*sys.argv))
