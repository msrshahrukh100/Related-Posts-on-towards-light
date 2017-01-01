from sklearn.feature_extraction.text import CountVectorizer
import scipy as sp 
import sys

from readfiles import read_posts_from_files
posts = read_posts_from_files()

def eucl_dist(v1,v2) :
	''' Returns the eucledian distance between two vectors 
	lialg is linear algebra and norm returns the magnitude of the vector
	we apply normalization by dividing the vector with its magnitude, 
	use to array when using norm'''
	v1_normalized = v1/sp.linalg.norm(v1.toarray())
	v2_normalized = v2/sp.linalg.norm(v2.toarray())
	delta = v1_normalized - v2_normalized 
	return sp.linalg.norm(delta.toarray())

vectorizer = CountVectorizer(min_df = 1,stop_words='english') # stop words
X = vectorizer.fit_transform(posts)

# view the feature vector by uncommenting the below line
# print X.toarray().transpose()  

new_post = "shahrukh programming"
new_post_vec = vectorizer.transform([new_post])

# to view all the extracted feature names
# print vectorizer.get_feature_names()

# to view the feature vector of the testing post uncomment the below line
# print new_post_vec.toarray().transpose()

# finding the post with the minimumdistance
minimum = sys.maxint
most_related_post = ""
for index,post in enumerate(posts) :

	# X[0] is the same as X.getrow(0)
	distance = eucl_dist(new_post_vec, X.getrow(index))
	if(distance < minimum) :
		minimum = distance
		most_related_post = post
	print "===>> Post %i is at distance %.2f . '%s'"%(index,distance,post)

print "\nThe most related post is at a distance of %.2f . '%s'"%(minimum,most_related_post)




