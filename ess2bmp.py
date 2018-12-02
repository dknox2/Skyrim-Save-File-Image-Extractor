#!/usr/bin/python3

import sys

def generate_image():
	if not args_are_valid():
		sys.exit("Enter valid arguments")

	save_file_name = sys.argv[1]
	with open(save_file_name, "rb") as save_file:
		dimensions = find_shot_dimensions(save_file)

		shot_data = find_shot_data(save_file, dimensions)

	print("Shot width: {}".format(dimensions[0]))
	print("Shot height: {}".format(dimensions[1]))

	bmp_file_name = sys.argv[2]
	with open(bmp_file_name, "w+b") as bmp_file:
		write_bmp_file_header(bmp_file)
		write_bmp_image_header(bmp_file, dimensions)
		write_bmp_shot_data(bmp_file, shot_data)

def args_are_valid():
	if (len(sys.argv)) != 3:
		return False

	save_file_name = sys.argv[1]
	bmp_file_name = sys.argv[2]

	save_file_valid = save_file_name.endswith(".ess")
	bmp_file_valid = bmp_file_name.endswith(".bmp")

	return save_file_valid and bmp_file_valid

def find_shot_dimensions(save_file):
	shot_size_offset = find_shot_size_offset(save_file)
	save_file.seek(shot_size_offset)

	shot_width = int.from_bytes(save_file.read(4), byteorder = "little")
	shot_height = int.from_bytes(save_file.read(4), byteorder = "little")

	return (shot_width, shot_height)

def find_shot_size_offset(save_file):
	# subtract 8 because the shot dimensions are two 4-byte integers
	return find_shot_data_offset(save_file) - 8

def find_shot_data_offset(save_file):
	save_file.seek(13)
	header_size = int.from_bytes(save_file.read(4), byteorder = "little")

	# add 17 bytes to get to the end header
	return header_size + 17

def find_shot_data(save_file, dimensions):
	save_file.seek(find_shot_data_offset(save_file))

	data = list()
	for x in range(3 * dimensions[0] * dimensions[1]):
		r = int.from_bytes(save_file.read(1), byteorder = "little")
		g = int.from_bytes(save_file.read(1), byteorder = "little")
		b = int.from_bytes(save_file.read(1), byteorder = "little")

		data.append((r, g, b))

	return data

def write_bmp_file_header(bmp_file):
	bmp_file.write(b"BM")

	# TODO write file size to file header (4 byte value)
	bmp_file.write((0).to_bytes(4, byteorder = "little"))

	for x in range(2):
		bmp_file.write((0).to_bytes(2, byteorder = "little"))

	# pixel data offset: 14 for file header + 40 for image header
	bmp_file.write((54).to_bytes(2, byteorder = "little"))

def write_bmp_image_header(bmp_file, dimensions):
	bmp_file.seek(14)

	bmp_file.write((40).to_bytes(4, byteorder = "little"))

	for dimension in dimensions:
		bmp_file.write((dimension).to_bytes(4, byteorder = "little"))

	bmp_file.write((1).to_bytes(2, byteorder = "little"))
	bmp_file.write((24).to_bytes(2, byteorder = "little"))

	# luckily everything past this point is optional and can be set to 0
	for x in range(6):
		bmp_file.write((0).to_bytes(4, byteorder = "little"))


def write_bmp_shot_data(bmp_file, shot_data):
	bmp_file.seek(54)

	for pixel in shot_data:
		for color in pixel:
			bmp_file.write((color).to_bytes(1, byteorder = "little"))

if __name__ == "__main__":
	generate_image()