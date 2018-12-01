import sys

def generate_image():
	if not args_are_valid():
		sys.exit("Enter valid arguments")

	with open(sys.argv[1], "rb") as save_file:
		shot_size_offset = find_shot_size_offset(save_file)
		save_file.seek(shot_size_offset)

		shot_width = int.from_bytes(save_file.read(4), byteorder = "little")
		shot_height = int.from_bytes(save_file.read(4), byteorder = "little")

		print("Shot width: {}".format(shot_width))
		print("Shot height: {}".format(shot_height))

def args_are_valid():
	if (len(sys.argv)) != 3:
		return False

	save_file_name = sys.argv[1]
	bmp_file_name = sys.argv[2]

	save_file_valid = save_file_name.endswith(".ess")
	bmp_file_valid = bmp_file_name.endswith(".bmp")

	return save_file_valid and bmp_file_valid

def find_shot_size_offset(save_file):
	save_file.seek(13)
	header_size = int.from_bytes(save_file.read(4), byteorder = "little")
	print(header_size)

	# add 17 bytes to get to the header
	# then subtract 8 to get to the screenshot data
	return header_size + 9

if __name__ == "__main__":
	generate_image()