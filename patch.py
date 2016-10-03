import sys


SUBLIME_TEXT_PATH = "/Applications/Sublime Text.app/Contents/MacOS/Sublime Text"


def _find_all(string, substring):
	result = []
	i = 0
	
	while i < len(string):
		i = string.find(substring, i)

		if i == -1:
			break
		else:
			result.append(i)
			i += 1

	return result


def _find_patch_points(max_distance):
	patch_points = None

	with open(SUBLIME_TEXT_PATH, "rb") as f:
		bytes = f.read()

	for x in _find_all(bytes, "\x35\x0e\x0d\x00"):
		for y in _find_all(bytes, "\xfa\x58\x0e\x00"):
			for z in _find_all(bytes, "\x61\x58\x0e\x00"):
				if abs(x - y) <= max_distance \
				   and abs(y - z) <= max_distance \
				   and abs(z - x) <= max_distance:
					if not patch_points is None:
						return None

					patch_points = [x, y, z]

	return patch_points


def _patch():
	patch_points = _find_patch_points(4096)
	
	if patch_points is None:
		print >> sys.stderr, "Faild to locate patch points"
		sys.exit(1)

	with open(SUBLIME_TEXT_PATH, "rb+") as f:
		for patch_point in patch_points:
			f.seek(patch_point)
			f.write("\x00\x00\x00\x00")


if __name__ == "__main__":
	_patch()
