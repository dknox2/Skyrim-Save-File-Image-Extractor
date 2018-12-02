#!/usr/bin/python3

import sys

usage = """python3 tes5file.ess output.bmp
./ess2bmp.py tes5file.ess output.bmp

Writes the screenshot data from the given Skyrim save file to the given bitmap
image file. Returns exit status 0 on a success, and non-zero otherwise (if the
parameters are invalid).
"""

INCORRECT_USAGE = -1
BMP_GENERATION_SUCCESS = 0

TESV_MAGIC_OFFSET = 13
TESV_HEADER_LENGTH = 17

BMP_FILE_HEADER_LENGTH = 14
BMP_IMAGE_HEADER_LENGTH = 40

BMP_PIXEL_DATA_OFFSET = BMP_FILE_HEADER_LENGTH + BMP_IMAGE_HEADER_LENGTH

UINT8 = 1
UINT16 = 2
UINT32 = 4

def main():
	validate_command_line_args()
	validate_usage(sys.argv[1], sys.argv[2])

	ess_to_bmp(sys.argv[1], sys.argv[2])
	sys.exit(BMP_GENERATION_SUCCESS)

def ess_to_bmp(save_file_name, bmp_file_name):
	with open(save_file_name, "rb") as save_file:
		dimensions = find_shot_dimensions(save_file)
		shot_data = find_shot_data(save_file, dimensions)

	write_bmp_file(bmp_file_name, dimensions, shot_data)

	print(save_file_name)
	print("Shot width: {}".format(dimensions[0]))
	print("Shot height: {}".format(dimensions[1]))

def validate_command_line_args():
	if (len(sys.argv)) != 3:
		exit_invalid_args()

def exit_invalid_args():
		print(usage)
		sys.exit(INCORRECT_USAGE)

def validate_usage(save_file_name, bmp_file_name):
	if not args_are_valid(save_file_name, bmp_file_name):
		exit_invalid_args()

def args_are_valid(save_file_name, bmp_file_name):
	save_file_valid = save_file_name.endswith(".ess")
	bmp_file_valid = bmp_file_name.endswith(".bmp")

	return save_file_valid and bmp_file_valid

def find_shot_dimensions(save_file):
	shot_size_offset = find_shot_size_offset(save_file)
	save_file.seek(shot_size_offset)

	shot_width = int.from_bytes(save_file.read(UINT32), byteorder = "little")
	shot_height = int.from_bytes(save_file.read(UINT32), byteorder = "little")

	return (shot_width, shot_height)

def find_shot_size_offset(save_file):
	return find_shot_data_offset(save_file) - UINT32 * 2

def find_shot_data_offset(save_file):
	save_file.seek(TESV_MAGIC_OFFSET)

	header_size = int.from_bytes(save_file.read(UINT32), byteorder = "little")

	return header_size + TESV_MAGIC_OFFSET + UINT32

def find_shot_data(save_file, dimensions):
	save_file.seek(find_shot_data_offset(save_file))

	data = list()
	for x in range(dimensions[1]):
		row = find_shot_data_row(save_file, dimensions[0], x)
		data.append(row)

	data.reverse()
	return data

def find_shot_data_row(save_file, row_width, row_num):
	save_file.seek(find_shot_data_offset(save_file) + row_width * row_num * 3)

	row = list()
	for x in range(row_width):
		b = int.from_bytes(save_file.read(UINT8), byteorder = "little")
		g = int.from_bytes(save_file.read(UINT8), byteorder = "little")
		r = int.from_bytes(save_file.read(UINT8), byteorder = "little")

		row.append((r, g, b))

	return row

def write_bmp_file(file_name, dimensions, shot_data):
	with open(file_name, "w+b") as bmp_file:
		write_bmp_file_header(bmp_file)
		write_bmp_image_header(bmp_file, dimensions)
		write_bmp_shot_data(bmp_file, shot_data)

def write_bmp_file_header(bmp_file):
	bmp_file.write(b"BM")
	bmp_file.write((0).to_bytes(UINT32, byteorder = "little"))
	for x in range(2):
		bmp_file.write((0).to_bytes(UINT16, byteorder = "little"))
	bmp_file.write((BMP_PIXEL_DATA_OFFSET).to_bytes(UINT16, byteorder = "little"))

def write_bmp_image_header(bmp_file, dimensions):
	bmp_file.seek(BMP_FILE_HEADER_LENGTH)

	bmp_file.write((BMP_IMAGE_HEADER_LENGTH).to_bytes(UINT32, byteorder = "little"))

	for dimension in dimensions:
		bmp_file.write((dimension).to_bytes(UINT32, byteorder = "little"))

	bmp_file.write((1).to_bytes(UINT16, byteorder = "little"))
	bmp_file.write((24).to_bytes(UINT16, byteorder = "little"))

	for x in range(6):
		bmp_file.write((0).to_bytes(UINT32, byteorder = "little"))

def write_bmp_shot_data(bmp_file, shot_data):
	bmp_file.seek(BMP_PIXEL_DATA_OFFSET)

	for row in shot_data:
		for pixel in row:
			for color_value in pixel:
				bmp_file.write((color_value).to_bytes(UINT8, byteorder = "little"))

if __name__ == "__main__":
	main()