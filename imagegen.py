from PIL import Image
import PIL.ImageOps
import argparse
import os

DEFAULT_OUTPUT_SUBDIR = "TestPatterns"
FILE_EXT = ".png"

def create_stripedV_image(width, height, i):
	for x in range(width):
		if x % i != 0:
			for y in range(height):
				pixels[x, y] = (0, 0, 0)  # Set pixel to black
				
def create_stripedH_image(width, height):
	for y in range(height):
		if y % i != 0:	# Odd rows
			for x in range(width):
				pixels[x, y] = (0, 0, 0)  # Set pixel to black

patternDict = {
		'striped_horizontal': create_stripedH_image,
		'striped_vertical': create_stripedV_image
	}

def create_image(pattern, width, height, output_path, interval):
	
	global pixels  # Declare pixels as global

	# Create a new image with a white background
	image = Image.new('RGB', (width, height), 'white')

	# Load the pixel data
	pixels = image.load()
	
	switch = patternDict

	# Call the appropriate function based on the command
	func = switch.get(pattern)
	if func:
		func(width, height, interval)
		
		if output_path is None:
			current_dir = os.getcwd()
			file_name = str(width) + "x" + str(height) + pattern + FILE_EXT
			output_path = os.path.join(current_dir, DEFAULT_OUTPUT_SUBDIR, file_name)
		os.makedirs(os.path.dirname(output_path), exist_ok=True)
		
		if args.invert:
			image = PIL.ImageOps.invert(image)
		
		image.save(output_path)
		print(f"Image saved as {output_path}")
	else:
		print("Invalid pattern")
		

def main():
	parser = argparse.ArgumentParser(description="Generate an image with a specified pattern.")
	parser.add_argument("pattern", type = str, choices = patternDict.keys(), help = "Pattern of the image")
	parser.add_argument("width", type = int, help = "Width of the image")
	parser.add_argument("height", type = int, help = "Height of the image")
	parser.add_argument("--output", type = str, default = None, help = "Output file path")
	parser.add_argument("--interval", type = int, default = 2, help = "2 - every other white...")
	parser.add_argument("--invert", action = "store_true", help = "Invert colors")

	global args
	args = parser.parse_args()

	create_image(args.pattern, args.width, args.height, args.output, args.interval)

if __name__ == "__main__":
	main()