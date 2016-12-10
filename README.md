RedditScrape: A general purpose reddit scraper
-------------------------------------------------------------------------------------

Downloads images, images from imgur, all types of gifs, and videos via youtube-dl.

Requirements:

praw , bs4 , youtube-dl

`sudo apt-get install youtube-dl`

`sudo pip install praw`

`sudo pip install bs4`

Run:

`python redditScrape.py`

-------------------------------------------------------------------------------------

DRCalc: DR Calculator from GradeCards
-------------------------------------------------------------------------------------

Calculates Department Ranks from PDFs of Grade Cards and outputs a sorted CSV.

Requirements:
pdfminer,slate

`pip install pdfminer`

`pip install slate`

Run:

`python drcalc.py`

-------------------------------------------------------------------------------------

Gif Maker: A HQ gif generator
-------------------------------------------------------------------------------------

Finds the scene related to the query and generates a HQ gif from it.

Requirements:
ffmpeg, pysrt

`pip install pysrt`

[GET ffmpeg](https://ffmpeg.org/download.html#build-linux)


Run:

`python gif_maker.py -q **query** -f **input video file** -s **input srt file** -o **output file**`

-------------------------------------------------------------------------------------
