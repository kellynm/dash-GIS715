import os
import glob
import pandas

import dash
import dash_core_components as dcc
import dash_html_components as html

os.chdir("data")

extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

#combine all files in the list
combined_csv = pandas.concat([pandas.read_csv(f, sep = ",", engine = "python") for f in all_filenames ])
#export to csv
combined_csv.to_csv( "se_fires_combined.csv", index=False, encoding='utf-8-sig')