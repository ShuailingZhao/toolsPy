import numpy as np
import sys
import re
import chardet

def writeDataWithBytes(fpath, file_identifier, width, height, scale, values):
	with open(fpath, 'wb') as f:
		f.write((file_identifier+'\n').encode())
		f.write(b'%d %d\n' % (width, height))
		f.write(b'%d\n' % scale)
		f.write(values)

def writeDataWithStr(fpath, file_identifier, width, height, scale, values):
	with open(fpath, 'wb') as f:
		f.write(file_identifier+'\n')
		f.write('%d %d\n' % (width, height))
		f.write('%d\n' % scale)
		f.write(values)	

def writePfm(data, fpath, scale=1, file_identifier="Pf", dtype="float32"):
	data = np.flipud(data)
	height, width = np.shape(data)[:2]
	values = np.ndarray.flatten(np.asarray(data, dtype=dtype))
	endianness = data.dtype.byteorder

	if endianness == '<' or (endianness == '=' and sys.byteorder == 'little'):
		scale *= -1
	
	if len(data.shape) == 3 and data.shape[2] == 3: # color image
		color = True
	elif len(data.shape) == 2 or len(data.shape) == 3 and data.shape[2] == 1: # greyscale
		color = False
	else:
		raise Exception('Image must have H x W x 3, H x W x 1 or H x W dimensions.')
	
	if color:
		file_identifier = "PF"

	if 3 == sys.version_info.major:
		writeDataWithBytes(fpath, file_identifier, width, height, scale, values)
	else:
		writeDataWithStr(fpath, file_identifier, width, height, scale, values)
		

def readPfm(fpath, expected_identifier="Pf"):

	with open(fpath, 'rb') as f:
		#  header
		identifier = _get_next_line(f)
		
		if identifier == expected_identifier:
			color = False
		elif identifier == 'PF':
			color = True
		else:
			raise Exception('Unknown identifier. Expected: "%s", got: "%s".' % (expected_identifier, identifier))

		try:
			line_dimensions = _get_next_line(f)
			dimensions = line_dimensions.split(' ')
			width = int(dimensions[0].strip())
			height = int(dimensions[1].strip())
		except:
			raise Exception('Could not parse dimensions: "%s". ''Expected "width height", e.g. "512 512".' % line_dimensions)

		try:
			line_scale = _get_next_line(f)
			scale = float(line_scale)
			assert scale != 0
			if scale < 0:
				endianness = "<"
			else:
				endianness = ">"
		except:
			raise Exception('Could not parse max value / endianness information: "%s". ''Should be a non-zero number.' % line_scale)

		try:
			data = np.fromfile(f, "%sf" % endianness)
			shape = (height, width, 3) if color else (height, width)
#			shape = (height, width, 3)
			data = np.reshape(data, shape)
			data = np.flipud(data)
			with np.errstate(invalid="ignore"):
				data *= abs(scale)
		except:
			raise Exception('Invalid binary values. Could not create %dx%d array from input.' % (height, width))

		return data.copy()
        

def _get_next_line(f):
	if 3 == sys.version_info.major:
		next_line = f.readline().rstrip().decode()
	else:
		next_line = f.readline().rstrip()
	# ignore comments
				
	while next_line.startswith('#'):
		next_line = f.readline().rstrip()
		
	return next_line


'''
Read a PFM file into a Numpy array. Note that it will have
a shape of H x W, not W x H. Returns a tuple containing the
loaded image and the scale factor from the file.
'''
def readPfm1(fileName):
	f = open(fileName, 'rb')

	color = None
	width = None
	height = None
	scale = None
	endian = None

	header = f.readline().rstrip()
	if header.decode('ascii') == 'PF':
		color = True    
	elif header.decode('ascii') == 'Pf':
		color = False
	else:
		raise Exception('Not a PFM file.')

	dim_match = re.search(r'(\d+)\s(\d+)', f.readline().decode('ascii'))
	if dim_match:
		width, height = map(int, dim_match.groups())
	else:
		raise Exception('Malformed PFM header.')

	scale = float(f.readline().rstrip())
	if scale < 0: # little-endian
		endian = '<'
		scale = -scale
	else:
		endian = '>' # big-endian

	data = np.fromfile(f, endian + 'f')
	shape = (height, width, 3) if color else (height, width)
	return np.reshape(data, shape), scale

'''
Write a Numpy array to a PFM file.
'''
def writePfm1(fileName, image, scale = 1):
	f = open(fileName, 'wb')

	color = None

	if image.dtype.name != 'float32':
		raise Exception('Image dtype must be float32.')

	if len(image.shape) == 3 and image.shape[2] == 3: # color image
		color = True
	elif len(image.shape) == 2 or len(image.shape) == 3 and image.shape[2] == 1: # greyscale
		color = False
	else:
		raise Exception('Image must have H x W x 3, H x W x 1 or H x W dimensions.')

	f.write(b'PF\n' if color else b'Pf\n')
	f.write(b'%d %d\n' % (image.shape[1], image.shape[0]))

	endian = image.dtype.byteorder

	if endian == '<' or endian == '=' and sys.byteorder == 'little':
		scale = -scale

	f.write(b'%f\n' % scale)

	image.tofile(f)

def readPfm3(filename, verbose=False):
	"""
	Reads in a PFM file by the given name and returns its contents in a new
	numpy ndarray with float32 elements. The absolute value of the 'scale
	factor' attribute is also returned. Both 1-channel and 3-channel images
	are supported, as well as both byte orders.
	"""
	with open(filename, 'rb') as f:
		if verbose:
			print("Reading file %s "%(filename), end='')
		buf = f.read()
		parsed = parse(buf, verbose)
		if parsed is not None:
			pixels, scale = parsed
			return pixels, scale
		raise RuntimeError("File %s is not a valid PFM file."%(filename))

def writePfm3(filename, pixels, scale=1.0, little_endian=True, verbose=False):
	"""
	Writes the contents of the given float32 ndarray into a 1- or 3-channel
	PFM file by the given name. Both little-endian and big-endian files are
	supported. The shape of the given array must be (h, w, c), where c is
	either 1 or 3.
	"""
	with open(filename, 'wb') as f:
		if verbose:
			print("Writing file %s "%(filename), end='')
		pfm_bytearray = generate(pixels, scale, little_endian, verbose)
		f.write(pfm_bytearray)

def parse(pfm_bytearray, verbose=False):
	"""
	Converts the given byte array, representing the contents of a PFM file, into
	a 1-channel or 3-channel numpy ndarray with float32 elements. Returns a tuple
	of (pixels, scale), where 'pixels' is the array and 'scale' is the absolute
	value of the scale factor attribute extracted from the header. Returns None
	if the file cannot be parsed.
	"""
	regex_pfm_header = b"(^(P[Ff])\\s+(\\d+)\\s+(\\d+)\\s+([+-]?\\d+(?:\\.\\d+)?)\\s)"
	match = re.search(regex_pfm_header, pfm_bytearray)
	if match is not None:
		header, typestr, width, height, scale = match.groups()
		width, height, scale = int(width), int(height), float(scale)
		numchannels = 3 if typestr == b"PF" else 1
		dtype = "<f" if scale < 0.0 else ">f"
		scale = abs(scale)
		if verbose:
			print("(w=%d, h=%d, c=%d, scale=%.3f, byteorder='%s')"%(width, height, numchannels, scale, dtype[0]))
		f32 = np.frombuffer(pfm_bytearray, dtype=dtype, count=width * height * numchannels, offset=len(header))
		f32 = f32.reshape((height, width) if numchannels == 1 else (height, width, 3))
		f32 = f32.astype(np.float32)  # pylint: disable=no-member
		return f32, scale
	return None

def generate(pixels, scale=1.0, little_endian=True, verbose=False):
	"""
	Converts the given float32 ndarray into an immutable byte array representing
	the contents of a PFM file. The byte array can be written to disk as-is. Both
	1-channel and 3-channel images are supported, and the pixels can be written
	in little-endian or big-endian order. The shape of the given array must be
	either (h, w), representing grayscale data, or (h, w, c), where c is either
	1 or 3, for grayscale and color data, respectively.
	"""
	assert pixels.ndim in [2, 3], "pixel array must not have ndim == %d"%(pixels.ndim)
	assert pixels.ndim == 2 or pixels.shape[2] in [1, 3]
	numchannels = 1 if pixels.ndim == 2 else pixels.shape[2]
	typestr = "PF" if numchannels == 3 else "Pf"
	width = pixels.shape[1]
	height = pixels.shape[0]
	f32 = pixels.astype(np.float32)  # pylint: disable=no-member
	if little_endian:
		byteorder = "<"
		scale = -scale
		f32bs = f32
	else:
		byteorder = ">"
		scale = scale
		f32bs = f32.byteswap()
	if verbose:
		print("(w=%d, h=%d, c=%d, scale=%.3f, byteorder='%s')"%(width, height, numchannels, abs(scale), byteorder))
	pfm_bytearray = bytearray("%s %d %d %.3f\n"%(typestr, width, height, scale), 'utf-8')
	pfm_bytearray.extend(f32bs.flatten())
	return bytes(pfm_bytearray)
