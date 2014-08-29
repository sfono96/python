import csv
from stripHTML import strip_tags # function to clean a string from HTML

read_path = '/Users/samfonoimoana/Documents/Standards Stuff/math-standards-html.csv'
write_path = '/Users/samfonoimoana/Documents/Standards Stuff/math-standards-clean.csv'

# let's go ahead and open the csv and clean the data (single-column)
cleaned_standards = []
with open(read_path,'rU') as f:
	reader = csv.reader(f, dialect=csv.excel_tab)
	for row in reader:
		cleaned_standards.append([strip_tags(row[0])]) # single column (first and only)

# now we can write it to file
with open(write_path, 'w') as fp:
    a = csv.writer(fp, delimiter=',')
    a.writerows(cleaned_standards)


