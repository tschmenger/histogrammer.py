# histogrammer.py
This script will take a numeric column of a given file and plot a histogram in the command line.
The purpose of doing so is solely to get an overview of the inspected data, and how this data is distributed.
Equal sized Groups will be formed according to the highest value of the given column divided by the number of bins.
After assigning counts into each group the script will normalize the values from 0 to 1.
The histogram is then plotted using = for each 0.005 of the normalized value.

How to use:

/.histogrammer.py -c NUM -f FILEPATH [OPTIONS] -h -g SYMBOL -s SEPARATOR -b SIZE -k VALUE

 	-c	NUM defines the target column
	-f	FILEPATH determines the target file
	-h	prints this help text
	-s	SEPARATOR sets the field-delimiter in the target file, default is \"\t\" (tab)
	-g	SYMBOL can either be \"#\" or = or '0' or 'o' or '.' to plot the histogram, default is =
	-b	SIZE sets the number of bins, default is 10
	-k	VALUE can be y/1 or n/0, default is n/0. Prints the column header specified with -c. Specify after -c and -f!



Example

Running "/.histogrammer.py -f EGFR_COSMIC_Example.txt -c 6 -b 64" will produce:

Detected Input: Target file is EGFR_COSMIC_Example.txt
Detected Input: Column of Interest is 6
Detected Input: Changed the Number of Bins from 10 to 64

Bin Groups      rel. value      Histogram
1.0000 to 1.9844        0.7317  | ==================================================================================================================================================
1.9844 to 2.9688        0.1777  | ====================================
2.9688 to 3.9531        0.0279  | ======
3.9531 to 4.9375        0.0174  | ===
4.9375 to 5.9219        0.0035  | =
5.9219 to 6.9062        0.007   | =
6.9062 to 7.8906        0.0035  | =
7.8906 to 8.8750        0.0105  | ==
8.8750 to 9.8594        0.0035  | =
9.8594 to 10.8438       0.0     |
10.8438 to 11.8281      0.0035  | =
11.8281 to 12.8125      0.0035  | =
12.8125 to 13.7969      0.0     |
13.7969 to 14.7812      0.0     |
14.7812 to 15.7656      0.0     |
15.7656 to 16.7500      0.0     |
16.7500 to 17.7344      0.0     |
17.7344 to 18.7188      0.0     |
18.7188 to 19.7031      0.0     |
19.7031 to 20.6875      0.0     |
20.6875 to 21.6719      0.0     |
21.6719 to 22.6562      0.0     |
22.6562 to 23.6406      0.0035  | =
23.6406 to 24.6250      0.0     |
24.6250 to 25.6094      0.0035  | =
25.6094 to 26.5938      0.0     |
26.5938 to 27.5781      0.0     |
27.5781 to 28.5625      0.0     |
28.5625 to 29.5469      0.0     |
29.5469 to 30.5312      0.0     |
30.5312 to 31.5156      0.0     |
31.5156 to 32.5000      0.0     |
32.5000 to 33.4844      0.0     |
33.4844 to 34.4688      0.0     |
34.4688 to 35.4531      0.0     |
35.4531 to 36.4375      0.0     |
36.4375 to 37.4219      0.0     |
37.4219 to 38.4062      0.0     |
38.4062 to 39.3906      0.0     |
39.3906 to 40.3750      0.0     |
40.3750 to 41.3594      0.0     |
41.3594 to 42.3438      0.0     |
42.3438 to 43.3281      0.0     |
43.3281 to 44.3125      0.0     |
44.3125 to 45.2969      0.0     |
45.2969 to 46.2812      0.0     |
46.2812 to 47.2656      0.0     |
47.2656 to 48.2500      0.0     |
48.2500 to 49.2344      0.0     |
49.2344 to 50.2188      0.0     |
50.2188 to 51.2031      0.0     |
51.2031 to 52.1875      0.0     |
52.1875 to 53.1719      0.0     |
53.1719 to 54.1562      0.0     |
54.1562 to 55.1406      0.0     |
55.1406 to 56.1250      0.0     |
56.1250 to 57.1094      0.0     |
57.1094 to 58.0938      0.0     |
58.0938 to 59.0781      0.0     |
59.0781 to 60.0625      0.0     |
60.0625 to 61.0469      0.0     |
61.0469 to 62.0312      0.0     |
62.0312 to 63.0156      0.0035  | =
63.0156 to 64.0000      0.0     |


Statistics
Mean= 1.91
STDEV= 4.32



This will tell us that a) the majority of somatic EGFR mutations do have a low frequency and b) that some residues are exceptionally often mutated.
This fits to the visual inspection over at https://cancer.sanger.ac.uk/cosmic/gene/analysis?ln=EGFR
