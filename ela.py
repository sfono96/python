import urllib2, re, csv
from stripHTML import strip_tags # function to clean a string from HTML


# url = 'http://www.uen.org/core/core.do?courseNum=4200' # kindergarten
# url = "http://www.uen.org/core/core.do?courseNum=4210" # 1st
# url = 'http://www.uen.org/core/core.do?courseNum=4220' # 2nd
# url = 'http://www.uen.org/core/core.do?courseNum=4230' # 3rd
# url = 'http://www.uen.org/core/core.do?courseNum=4240' # 4th
# url = 'http://www.uen.org/core/core.do?courseNum=4250' # 5th
# url = 'http://www.uen.org/core/core.do?courseNum=4260' # 6th
# url = 'http://www.uen.org/core/core.do?courseNum=4270' # 7th
url = 'http://www.uen.org/core/core.do?courseNum=4280' # 8th

content = urllib2.urlopen(url).read()
# content = content

def clean_newlines_and_tabs(text):
	return text.replace('\n','').replace('\t','').rstrip().lstrip()

cl = '<span class="big-bold">(.*?)</span>' # cluster
st = '<span class="paratitle">.*?</a>(.*?)</span>' # standard name
d1 = '<span class="paratitle">.*?<br />(.*?)</p>' # standard description
sc = '<span class="bold">.*?</a>(.*?)</span>' # standard sub component name (a,b,c,d ...)
d2 = '<span class="bold">.*?<br />(.*?)</p>' # standard sub component description

# go through the html and look for the
# 1) DOMAIN NAME (IGNORE BECAUSE IT IS PART OF THE STANDARD NAME)
# 2) CLUSTER NAME (<span class="big-bold"></span>)
# 3) STANDARD NAME (<span class="paratitle"></span>)
# 4) STANDARD SUB COMPONENT IF ANY (<span class="bold"></span>) THIS WILL BE a., b., c., d., etc.  
# 5) STANDARD DESCRIPTION

starting_point_text = '<p class="big-bold">Core Standards of the Course</p>'
not_finished = True
idx = content.index(starting_point_text)
cluster_idx = 0
standard_idx = 0
sub_standard_idx = 0
cluster = None
standard = None
standard_description = None
complete_standards = []

while not_finished:
	searched_content = content[idx:]
	
	next_cluster = strip_tags(clean_newlines_and_tabs(re.findall(cl,searched_content,re.DOTALL|re.MULTILINE)[0])) if len(re.findall(cl,searched_content,re.DOTALL|re.MULTILINE)) > 0 else ''
	next_standard = strip_tags(clean_newlines_and_tabs(re.findall(st,searched_content,re.DOTALL|re.MULTILINE)[0])) if len(re.findall(st,searched_content,re.DOTALL|re.MULTILINE)) > 0 else ''
	next_standard_description = strip_tags(clean_newlines_and_tabs(re.findall(d1,searched_content,re.DOTALL|re.MULTILINE)[0])) if len(re.findall(d1,searched_content,re.DOTALL|re.MULTILINE)) > 0 else ''
	next_sub_standard = strip_tags(clean_newlines_and_tabs(re.findall(sc,searched_content,re.DOTALL|re.MULTILINE)[0])) if len(re.findall(sc,searched_content,re.DOTALL|re.MULTILINE)) > 0 else ''
	next_sub_standard_description = strip_tags(clean_newlines_and_tabs(re.findall(d2,searched_content,re.DOTALL|re.MULTILINE)[0])) if len(re.findall(d2,searched_content,re.DOTALL|re.MULTILINE)) > 0 else ''

	# get current indexes of next cluster, standard, 
	next_cluster_idx = searched_content.index('<span class="big-bold">')+23 if '<span class="big-bold">' in searched_content else 99999
	next_standard_idx = searched_content.index('<span class="paratitle">')+23 if '<span class="paratitle">' in searched_content else 99999
	next_sub_standard_idx = searched_content.index('<span class="bold">')+23 if '<span class="bold">' in searched_content else 99999
	# print next_cluster_idx, next_standard_idx, next_sub_standard_idx

	# check to see if next standard or sub standard - if none then quit else continue
	if next_standard == '' and next_sub_standard == '':
		not_finished = False
	else:
		# assign cluster (new only if next cluster is closer than next standard and sub standard)
		if next_cluster_idx < next_standard_idx and next_cluster_idx < next_sub_standard_idx:
			cluster = next_cluster

		# assign standard 
		if next_standard_idx < next_sub_standard_idx:
			standard = next_standard
			standard_description = next_standard_description
		else:
			standard = next_sub_standard
			standard_description = next_sub_standard_description

	row = [cluster, standard, standard_description]
	complete_standards.append(row)
	idx += min([next_cluster_idx,next_standard_idx,next_sub_standard_idx])
	# not_finished = False


# now we can write it to file
write_path = '/Users/samfonoimoana/Documents/Standards Stuff/ELA-standards-clean.csv'
with open(write_path, 'w') as fp:
    a = csv.writer(fp, delimiter=',')
    a.writerows(complete_standards)

