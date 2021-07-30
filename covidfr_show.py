#============README============#
# Show French Covid-19 Trend===#
# Using a external screen =====#
# Author: Dan Xu ==============#
# Dependent Libraries =========#
# 1. requests =================#
# 2. shutil ===================#
# 3. PIL ======================#
# 4. Beautifulsoup ============#
# 5. pytesseract ==============#
# 6. re =======================#
# Test platform ===============#
# macOS and Raspberry Pi Zero =#
#============EOF===============#

import sys
import os
import logging
import time
from PIL import Image, ImageDraw, ImageFont
import traceback
import epd2in13_V2
from covidfr_data import get_covid_info

data_covid = get_covid_info()

logging.basicConfig(level=logging.DEBUG)

try:
    logging.info('App: CovidFR')

    epd = epd2in13_V2.EPD()
    logging.info('Init and Clear')
    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)

    # Print data
    font15 = ImageFont.truetype('Font.ttc', 15)

    logging.info('Print Covid data...')
    image = Image.new('1', (epd.height, epd.width), 255)
    draw = ImageDraw.Draw(image)
    draw.text((10, 10), 'I LOVE XD!', font=font15, fill=0)
    draw.text((120, 60), 'Daily confirmed:', font=font15, fill=0)
    draw.text((110, 90), data_covid[1], font=font15, fill=0)

    epd.display(epd.getbuffer(image))
    
    epd.sleep()

except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd2in13_V2.epdconfig.module_exit()
    exit()