from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import scipy as sp 
import sys
import nltk.stem

english_stemmer = nltk.stem.SnowballStemmer('english')

from requestposts import request_post_from_site 
from readfiles import read_posts_from_files

# requesting posts from 'http://towardlight.pythonanywhere.com' and then reading them into posts
posts = []
if request_post_from_site() :
	posts = read_posts_from_files()

if len(posts) == 0 : sys.exit()

print "%i Posts have been received" % (len(posts))

class StemmedCountVectorizer(CountVectorizer) :
	def build_analyser(self) :

		'''this function returns the function ( lambda used to return a function ) that
		stems each word using the english_stemmer 'english_stemmer.stem(word)' after it has done
		tokenization.
		english_stemmer.stem("graphics") returns "graphic" '''
		analyser = super(StemmedCountVectorizer,self).build_analyser()
		return lambda document : (english_stemmer.stem(word) for word in analyser(document))



class StemmedTfidfCountVectorizer(TfidfVectorizer) :
	def build_analyser(self) :

		'''this function returns the function ( lambda used to return a function ) that
		stems each word using the english_stemmer 'english_stemmer.stem(word)' after it has done
		tokenization.Here the tokenization is done after applying Tf-Idf.
		english_stemmer.stem("graphics") returns "graphic" '''
		analyser = super(StemmedTfidfCountVectorizer,self).build_analyser()
		return lambda document : (english_stemmer.stem(word) for word in analyser(document))




def eucl_dist(v1,v2) :

	''' Returns the eucledian distance between two vectors 
	lialg is linear algebra and norm returns the magnitude of the vector
	we apply normalization by dividing the vector with its magnitude, 
	use to array when using norm'''

	v1_normalized = v1/sp.linalg.norm(v1.toarray())
	v2_normalized = v2/sp.linalg.norm(v2.toarray())
	delta = v1_normalized - v2_normalized 
	return sp.linalg.norm(delta.toarray())



vectorizer = StemmedTfidfCountVectorizer(min_df = 1,stop_words='english', decode_error='ignore') 
# stop words to remove not required words


# view the feature vector by uncommenting the below line
# print X.toarray().transpose()  
ask_post_id = int(input("Choose the file with whom the nearest related post is to be found : "))
new_post = posts[ask_post_id - 1]

posts.pop(ask_post_id - 1)

X = vectorizer.fit_transform(posts)
new_post_vec = vectorizer.transform([new_post])

# to view all the extracted feature names
# print vectorizer.get_feature_names()

# to view the feature vector of the testing post uncomment the below line
# print new_post_vec.toarray().transpose()

# finding the post with the minimumdistance
minimum = sys.maxint
most_related_post = ""
for index,post in enumerate(posts) :
	print "................",
	if ask_post_id - 1 == index : continue;
	# X[0] is the same as X.getrow(0)
	distance = eucl_dist(new_post_vec, X.getrow(index))
	if(distance < minimum) :
		minimum = distance
		most_related_post = post
	# print "===>> Post %i is at distance %.2f . '%s'"%(index+1,distance,post)

print "\nThe most related post is at a distance of %.2f .Content: '%s...'"%(minimum,most_related_post[:15])




