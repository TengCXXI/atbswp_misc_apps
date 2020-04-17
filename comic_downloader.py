#! python3
# comic_downloader.py - Downloads all comic images for a series
# Created by Teng Mao @https://github.com/TengCXXI
# With references to "Automate the Boring Stuff with Python" by Al Sweigart

import requests, os, bs4, time
import pyinputplus as pyip
from pathlib import Path

url = pyip.inputURL("Please provide the url for the comic to download, starting from the first page you want: ")

comic_name = pyip.inputStr("Please provide the comic name: ")

comic_folder_path = './comics/' + comic_name

# Create a folder with the comic name to store the images
os.makedirs(comic_folder_path, exist_ok=True)

while True:

    # Download the page
    print('Downloading page %s...' % url)
    res = requests.get(url)
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    # Create the URL for the home site for URL extraction functions
    site_home = str(Path(url).parents[len(Path(url).parents)-3])

    # Function for image URLs extraction on the Manganelo site
    def image_url_extract(site_home=site_home, soup=soup):
        if site_home == 'https:\\manganelo.com':
            return soup.select('div[class="container-chapter-reader"]')[0].select('img')
        if site_home == 'https:\\mangakakalot.com':
            return soup.select('#vungdoc img')
        if site_home == 'https:\\www.gocomics.com':
            return soup.select('picture[class="item-comic-image"]')[0].select('img')
        else:
            raise Exception("Image URL extraction not defined for this website")

    # Function for next chapter URL extraction (ncue)
    def next_chap_url_extract(site_home=site_home, soup=soup):
        if site_home == 'https:\\manganelo.com':
            return soup.select('a[class="navi-change-chapter-btn-next a-h"]')[0].get('href')
        if site_home == 'https:\\mangakakalot.com':
            return soup.select('a[class="back"]')[0].get('href')
        if site_home == 'https:\\www.gocomics.com':
            return res.headers['Access-Control-Allow-Origin'][:-1] + \
                    soup.select('a[class="fa btn btn-outline-secondary btn-circle fa-caret-right sm"]')[0].get('href')
        else:
            raise Exception("Next chapter URL extraction not defined for this website")

    # Isolate the URLs of the comic pages
    comic_element = image_url_extract()

    # Check to see if the comic page will load
    if comic_element == []:
        print('Could not find comic images.')
    else:
        # Put all the URLs of comic pages into a list using list comprehension
        comic_image_urls = []
        [comic_image_urls.append(comic_element[i].get('src')) for i in range(len(comic_element))];

    # Create a loop to download the images and save them to the comic folder
    for url in comic_image_urls:

        # Download the image
        res_image = requests.get(url)
        res_image.raise_for_status()

        # Create the file name with the chapter in name
        file_name = str(Path(url)).replace(str(Path(url).parents[1]), "")\
                .replace("\\", "_")

        # Add .jpg to the end of image files from 'https:\\www.gocomics.com' so that they can be opened with photos app
        if site_home in ['https:\\www.gocomics.com']:
            file_name = file_name + '.jpg'

        # Save the image
        with open(os.path.join(comic_folder_path, file_name), 'wb') as image_file:
            [image_file.write(chunk) for chunk in res_image.iter_content(100_000)]

    # Set the URL for the following chapter
    try:
        url = next_chap_url_extract()
    except:
        break
    # Time to wait between downloading each chapter
    time.sleep(1)

print('Done')
