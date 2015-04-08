"""This module helps for uploading and downloading listings from/to play."""
import os
import json
from file_util import mkdir_p
from file_util import list_dir_abspath


def upload(client, source_dir):
    """Upload listing files in source_dir. folder herachy."""
    print('')
    print('upload store listings')
    print('---------------------')
    listings_folder = os.path.join(source_dir, 'listings')
    langfolders = filter(os.path.isdir, list_dir_abspath(listings_folder))

    for language_dir in langfolders:
        language = os.path.basename(language_dir)
        with open(os.path.join(language_dir, 'listing.json')) as listings_file:
            listing = json.load(listings_file)
        listing_response = client.update(
            'listings', language=language, body=listing)

        print('  Listing for language %s was updated.' %
              listing_response['language'])


def download(client, target_dir):
    """Download listing files from play and saves them into folder herachy."""
    print('')
    print('download store listings')
    print('---------------------')
    listings = client.list('listings')
    for listing in listings:
        path = os.path.join(target_dir, 'listings', listing['language'])
        mkdir_p(path)
        with open(os.path.join(path, 'listing.json'), 'w') as outfile:
            print("save listing for {0}".format(listing['language']))
            json.dump(
                listing, outfile, sort_keys=True,
                indent=4, separators=(',', ': '))
