from nltk.corpus import stopwords
from trainingSetUtils import *

def train(features, sample_proportion):
	train_size = int(len(features)*samples_proportion)
	train_set, test_Set = features[:train_size],features[train_size:]
	print('Training Set size = ' + str(len(train_set)))
	print('Test Set size = ' + str(len(test_set)))


ham = read_files('pre/ham/')
spam = read_files('pre/spam')


ham_files = read_file_contents(ham)
spam_files = read_file_contents(spam)

all_emails = [ (email,0) for email in ham_files]
all_emails += [ (email,1) for email in spam_files]

print(len(all_emails))

random.shuffle(all_emails)

stoplist = stopwords.words('english')

all_features = [ (get_features (email,'bow',stoplist) , label) \
		for (email,label) in all_emails ]

train(all_features,0.6)
