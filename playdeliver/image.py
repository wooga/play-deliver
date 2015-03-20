"""This module helps for uploading and downloading images from/to play."""
import imghdr
import httplib2
import os
from file_util import mkdir_p
from file_util import list_dir_abspath

image_types = ["featureGraphic",
               "icon",
               "phoneScreenshots",
               "promoGraphic",
               "sevenInchScreenshots",
               "tenInchScreenshots",
               "tvBanner",
               "tvScreenshots"]

single_image_types = ['tvBanner',
                      'promoGraphic',
                      'icon',
                      'featureGraphic']


def upload(client, source_dir):
    """
    Upload images to play store.

    The function will iterate through source_dir and upload all matching
    image_types found in folder herachy.
    """
    print('')
    print('upload images')
    print('-------------')
    base_image_folders = [
        os.path.join(source_dir, 'images', x) for x in image_types]

    for type_folder in base_image_folders:
        if os.path.exists(type_folder):
            image_type = os.path.basename(type_folder)
            langfolders = filter(os.path.isdir, list_dir_abspath(type_folder))
            for language_dir in langfolders:
                language = os.path.basename(language_dir)
                delete_and_upload_images(
                    client, image_type, language, type_folder)


def delete_and_upload_images(client, image_type, language, base_dir):
    """
    Delete and upload images with given image_type and language.

    Function will stage delete and stage upload all
    found images in matching folders.
    """
    print('{0} {1}'.format(image_type, language))
    files_in_dir = os.listdir(os.path.join(base_dir, language))
    delete_result = client.deleteall(
        'images', imageType=image_type, language=language)

    deleted = delete_result.get('deleted', list())
    for deleted_files in deleted:
        print('  delete image: {0}'.format(deleted_files['id']))

    for image_file in files_in_dir:
        image_file_path = os.path.join(base_dir, language, image_file)
        image_response = client.upload(
            'images',
            imageType=image_type,
            language=language,
            media_body=image_file_path)
        print("  upload image {0} new id {1}".format(image_file, image_response['image']['id']))


def download(client, target_dir):
    """Download images from play store into folder herachy."""
    print('download image previews')
    tree = {}
    listings = client.list('listings')
    languages = map(lambda listing: listing['language'], listings)

    parameters = [{'imageType': image_type, 'language': language}
                  for image_type in image_types for language in languages]
    tree = {image_type: {language: list()
                         for language in languages}
            for image_type in image_types}

    for params in parameters:
        result = client.list('images', **params)
        image_type = params['imageType']
        language = params['language']
        tree[image_type][language] = map(
            lambda r: r['url'], result)

    for image_type, language_map in tree.items():
        for language, files in language_map.items():
            if len(files) > 0:
                mkdir_p(
                    os.path.join(target_dir, 'images', image_type, language))
            if image_type in single_image_types:
                if len(files) > 0:
                    image_url = files[0]
                    path = os.path.join(
                        target_dir,
                        'images',
                        image_type,
                        language,
                        image_type)
                    load_and_save_image(image_url, path)
            else:
                for idx, image_url in enumerate(files):
                    path = os.path.join(
                        target_dir,
                        'images',
                        image_type,
                        language,
                        image_type + '_' + str(idx))
                    load_and_save_image(image_url, path)


def load_and_save_image(url, destination):
    """Download image from given url and saves it to destination."""
    from urllib2 import Request, urlopen, URLError, HTTPError
    # create the url and the request
    req = Request(url)

    # Open the url
    try:
        f = urlopen(req)
        print "downloading " + url

        # Open our local file for writing

        local_file = open(destination, "wb")
        # Write to our local file
        local_file.write(f.read())
        local_file.close()

        file_type = imghdr.what(destination)
        local_file = open(destination, "rb")
        data = local_file.read()
        local_file.close()

        final_file = open(destination + '.' + file_type, "wb")
        final_file.write(data)
        final_file.close()
        print('save image preview {0}'.format(destination + '.' + file_type))
        os.remove(destination)

    # handle errors
    except HTTPError, e:
        print "HTTP Error:", e.code, url
    except URLError, e:
        print "URL Error:", e.reason, url
