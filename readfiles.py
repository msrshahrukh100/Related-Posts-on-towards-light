from settings import DIR
import os


def read_posts_from_files() :
	return [open(os.path.join(DIR,filename)).read() for filename in os.listdir(DIR)]
