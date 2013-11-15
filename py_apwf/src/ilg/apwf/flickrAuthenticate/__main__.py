import sys
import flickrapi

# -----------------------------------------------------------------------------

def main(argv):

    print 'Authorise Flickr application.'
    api_key = raw_input("Press enter the api key: ")
    api_secret = raw_input("Press enter the api secret: ")
    
    flickr = flickrapi.FlickrAPI(api_key, api_secret)

    (token, frob) = flickr.get_token_part_one(perms='write')
    if not token: 
        raw_input("Press press ENTER after you authorised this program: ")
        
    token = flickr.get_token_part_two((token, frob))
    
    print 'Authorised ({0}).'.format(token)
    
    return


# -----------------------------------------------------------------------------

if __name__ == '__main__':
    sys.exit(main(*sys.argv))
