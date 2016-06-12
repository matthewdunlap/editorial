#coding: utf-8

from PIL import Image, ExifTags
import photos
import workflow
import console
import editor
import os
import io
import time

timestr = time.strftime("%Y-%m-%d")

img = photos.pick_image()
if not img:
	workflow.stop()

try:
	for orientation, value in ExifTags.TAGS.items():
		if value == 'Orientation':
			break
	exif = dict(img._getexif().items())
	rot_degrees = {3: 180, 6: 270, 8: 90}.get(exif[orientation], 0)
	if rot_degrees:
		img=image.rotate(rot_degrees, expand=True)
# cases: image don't have getexif
except (AttributeError, KeyError, IndexError):
	pass

doc_path = editor.get_path()
doc_dir, fn = os.path.split(doc_path)
default_name = '{}_image'.format(timestr)

i = 1
while True:
	if not os.path.exists(os.path.join(doc_dir, default_name + '.jpg')):
		break
	default_name = '{}_image_{}'.format(timestr, i)
	i += 1

root, rel_doc_path = editor.to_relative_path(editor.get_path())
filename = default_name + '.jpg'

if not filename:
	workflow.stop()

img_data = io.BytesIO()
img.save(img_data, 'jpeg')

rel_doc_dir, fn = os.path.split(rel_doc_path)
dest_path = os.path.join(rel_doc_dir, filename)
editor.set_file_contents(dest_path, img_data.getvalue(), root)
workflow.set_output(filename)
