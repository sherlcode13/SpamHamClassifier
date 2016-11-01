
import os, re, tarfile, subprocess, email


def strip_html(file):
	# Remove inline JavaScript/CSS:
	stripped = re.sub(r"(?is)<(script|style).*?>.*?(</1>)","",file)
	# Remove html comments

	stripped = re.sub(r"(?s)<!--(.*?)-->[\n]?"," ",stripped)
	# remove the remaining tags
	stripped = re.sub(r"(?s)<.*?>"," ",stripped)
	# Remove white spaces
	stripped = re.sub(r"&nbsp;"," ",stripped)
	stripped = re.sub(r"^$", "",stripped)
	stripped = re.sub(r"''|,", "", stripped)
	stripped = stripped.lower()
	stripped = re.sub(r"[0-9]+"," number ",stripped)
	stripped = re.sub(r'(http|https)://[^\s]*',' httpaddr ',stripped)
	stripped = re.sub(r'[$]+',' dollar ',stripped)
	stripped = re.sub(r'[^a-z\n]',' ',stripped)
	stripped = re.sub(r" +", " ", stripped)
	return stripped

# def strip_html(data):
# 	p = re.compile(r'<.*?>')
# 	return p.sub('',data)


def untar(file_path,path):
	if (file_path.endswith(('tar.gz')) ):
		tar = tarfile.open(file_path)
		names = tar.getnames()
		tar.extractall(path)
		tar.close()
	else:
		print("Not a tar.gz file.")

def processEmail(email_path):
	
	# clean pre/ directory
	#subprocess.check_call('sh remove_dirs.sh', shell=True)
	print('I am processing.....')
	for path in email_path:
		for root, dir, files in os.walk(path):
			print ('Files in' + root[:])

			#untar tar.gz files one by one
			for file in files:
				print ('Processing '+ file)
				file_path = root+file
				untar(file_path,path)


		# find all files in raw/
		file_str = subprocess.check_output('find emails/ -type f', shell=True)

		# extract all files except tar.gz files

		file_list = [ x for x in file_str.splitlines() if not x.endswith(bytes('tar.gz','UTF-8')) ]

		# check email files one by one

		for fl in file_list:
			raw_html = open(fl, 'r', encoding="ISO-8859-1").read()
			email_content = email.message_from_string(raw_html)
			try:
				# create dirs for preprocess file
				
				pre_path = 'pre' + str(re.search("/.*/",str(fl)).group())
				print(pre_path)
				os.makedirs(pre_path)
			except OSError:
				pass
			finally:
				f = open(re.sub(b"emails/",b"pre/" ,fl), 'w')
				if email_content.is_multipart():
					for payload in email_content.get_payload():
						f.write(strip_html(str(payload.get_payload())))
				else:
					f.write(strip_html(str(email_content.get_payload())))
				f.close()
				print('Finally')
		print ('Done------')

email_path  = ['emails/ham/', 'emails/spam/']
processEmail(email_path)
