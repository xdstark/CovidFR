#============README============#
# Get French Covid-19 Trend ===#
# Author: Dan Xu ==============#
# Dependent Libraries =========#
# 1. requests =================#
# 2. shutil ===================#
# 3. PIL ======================#
# 4. Beautifulsoup ============#
# 5. pytesseract ==============#
# 6. re =======================#
# 7. os =======================#
# 8. lxml =====================#
# Test platform ===============#
# macOS and Raspberry Pi Zero =#
#============EOF===============#

import os
import requests
import shutil
from PIL import Image, ImageOps
from bs4 import BeautifulSoup
import pytesseract
import re
import lxml


def get_covid_info():
     # basic url
    url_base = 'https://www.santepubliquefrance.fr'
    url_main = 'https://www.santepubliquefrance.fr/dossiers/coronavirus-covid-19/coronavirus-chiffres-cles-et-evolution-de-la-covid-19-en-france-et-dans-le-monde'

    # Get the image
    resp_src = requests.get(url=url_main)
    resp_bs = BeautifulSoup(resp_src.text, features='html.parser')
    img_src = resp_bs.find(class_='content__img-ctn').find('img')['src']
    img_url = url_base + img_src

    # Image process
    img_get = requests.get(img_url, stream=True)
    with open('img.png', 'wb') as out_file:
        shutil.copyfileobj(img_get.raw, out_file)

    img = Image.open('img.png')

    os.remove('img.png')

    box = (0, 0, 386, 240)
    img_region = img.crop(box)

    img_region_inv = ImageOps.invert(img_region)
    img_region_gry = img_region_inv.convert('L')

    threshold = 100

    table = []

    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)

    img_bin = img_region_gry.point(table, '1')

    img_region = img_region.convert('1')

    # Extract info
    pattern = re.compile(r'\d+')
    cas_info = re.findall(r"(\d+(?:\s+\d+)*)",
                          pytesseract.image_to_string(img_bin))

    return cas_info
