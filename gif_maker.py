import pysrt
from datetime import datetime
import argparse
import subprocess


def find_gif(subsfile,query):
	subs = pysrt.open(subsfile)
	start = 0
	duration = 0
	print(query)
	for sub in subs:
		text = " ".join(sub.text.lower().split())
		if query in text:
			start = datetime.strptime(str(sub.start),"%H:%M:%S,%f").strftime("%H:%M:%S")
			duration = (datetime.strptime(str(sub.end),"%H:%M:%S,%f")-datetime.strptime(str(sub.start),"%H:%M:%S,%f")).seconds
			break	
	return start,duration

def make_gif(video,subs,query,output):
	start,duration = find_gif(subs,query)
	filters="fps=15,scale=320:-1:flags=lanczos"
	pallete_generate = "ffmpeg -y -ss {} -t {} -i {} -vf fps=10,scale=320:-1:flags=lanczos,palettegen /tmp/palette.png".format(start,duration,video)
	gif_generate = 'ffmpeg -ss {} -t {} -i {} -i /tmp/palette.png -filter_complex "fps=10,scale=320:-1:flags=lanczos[x];[x][1:v]paletteuse" {}'.format(start,duration,video,output)
	# print(pallete_generate)
	subprocess.call(pallete_generate,shell=True)
	subprocess.call(gif_generate,shell=True)


def main():
	parser = argparse.ArgumentParser(prog="Gif Maker")
	parser.add_argument('-f','--file',required=True)
	parser.add_argument('-s','--subs',required=True)
	parser.add_argument('-q','--query',required=True)
	parser.add_argument('-o','--output',required=True)
	parsed = parser.parse_args()
	make_gif(parsed.file,parsed.subs,parsed.query,parsed.output)

if __name__ == "__main__":
	main()