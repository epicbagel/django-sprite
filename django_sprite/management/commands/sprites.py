import os
import Image
from django.core.management.base import NoArgsCommand
from django.conf import settings
import time
from datetime import datetime
import glob
from operator import itemgetter

from bin_packing import Box, pack_boxes

class Command(NoArgsCommand):

	help = "Describe the Command Here"

	def handle_noargs(self, **options):

		version_stamp = str(int(time.mktime(datetime.now().timetuple())))

		BUFFER_SIZE = 40

		images = []
		
		filenames = []
		
		boxes = []

		directories  = getattr(settings, 'SPRITE_DIRS', ['/media/public_media/images/sprites'])

		for directory in directories:

			for image in [f for f in os.listdir(directory) if f.endswith('.png')]:
				
				image_file = Image.open('%s/%s' % (directory, image, ))
				
				image_width, image_height = image_file.size
				
				boxes.append(Box(image_width, image_height, image_file))

		max_width, y_off, packing = pack_boxes(boxes)
		
		master = Image.new(mode = 'RGBA', size = (max_width, y_off), color = (0,0,0,0))  # fully transparent

		for x, y, image in packing:

		    master.paste(image.filename, (x, y))

		map_ouput = '%s' % getattr(settings, 'SPRITE_MAP_OUTPUT')
		
		location = '%ssprites.r%s.%s' % (getattr(settings, 'SPRITE_MAP_OUTPUT'), version_stamp, 'png')

		master.save(location)
		
		css_file_location = '%ssprites.css' % getattr(settings, 'SPRITE_CSS_OUTPUT')

		sprite_url = '%simages/sprites.r%s.png' % (settings.STATIC_URL, version_stamp)
		
		iconCssFile = open(css_file_location, 'w')
		
		print css_file_location
			
		for x, y, image in packing:
			
			image_file = image.filename

			image_width, image_height = image_file.size
						
			filename = image_file.filename.split('/')[-1].split('.')[0]
			
			css = """.sprite_%(filename)s {
			    background-position: -%(top)spx -%(left)spx;
			    width:%(width)spx;
			    height:%(height)spx;
				display: inline-block;
			}
			""" % {'filename' : filename, 'top' : x, 'left' : y, 'width' : image_width, 'height' : image_height}
			
			
			iconCssFile.write(css)

		iconCssFile.write("""

			.sprite, .sprite_inline {

				background-image: url('%s');
				*background-image: url('%s');
			}

		""" % (sprite_url, sprite_url))

		iconCssFile.close()
			
			
			
	


