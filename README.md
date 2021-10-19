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
