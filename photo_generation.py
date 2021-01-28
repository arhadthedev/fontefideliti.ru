#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from PIL import Image
import os
import sys
import yaml


def save_jpeg(image, path):
	image.save(path, quality=94, optimize=True, progressive=True)


def generate_large(original, output_base):
	output_path = "{}.jpg".format(output_base)
	generated = original.copy()
	generated.thumbnail((794, 794), Image.LANCZOS, None)
	save_jpeg(generated, output_path)


def generate_thumbnail(original, output_base, variant):

	output_path = "{}-{}.jpg".format(output_base, variant)
	max_size = 0, 0
	if variant[0] == "w":
		max_size = int(variant[1:]), 9999
	else:
		max_size = 9999, int(variant[1:])
	generated = original.copy()
	generated.thumbnail(max_size, Image.LANCZOS, None)
	save_jpeg(generated, output_path)


photos_file = open('photo_generation.yml', 'r', encoding='utf-8')
photos = yaml.safe_load(photos_file)

for item in photos:
	relative_base_path = "{}".format(item["path"])
	original = Image.open("{}.jpg".format(relative_base_path))
	if item["mirror"]:
		original = original.transpose(Image.FLIP_LEFT_RIGHT)
	if len(sys.argv) < 2:
		sys.exit('error: output path argument is not specified')
	output_base_path = os.path.join(sys.argv[1], relative_base_path)

	print("Generating {}...".format(relative_base_path))
	generate_large(original, output_base_path)

	for variant in item["output"]:
		print(" - {}...". format(variant))
		generate_thumbnail(original ,output_base_path, variant)
