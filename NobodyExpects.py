import praw
import sys
import redis
import os
import time

# get redis info from environment
r_host = os.environ['REDIS_HOST']
r_port = os.environ['REDIS_PORT']
r_db = os.environ['REDIS_DB']

#initialise redis
try:
	db = redis.Redis(host=r_host, port=r_port, db=r_db)
except Exception as e:
	print("Redis Initialisation Error: ", e)
	sys.exit(1)


# initialise reddit api through praw
try:
	reddit = praw.Reddit('bot') # bot as defined in praw.ini
except Exception as e:
	print("Reddit Initialisation Error: ", e)
	sys.exit(1)


def exists(subreddit_comment):
	if db.get(str(subreddit_comment)) == None:
		return False
	else:
		return True

def search_comment(comment):

	if 'spain' in comment.lower():
		return True
	elif 'spanish' in comment.lower():
		return True
	return False

def reply_to_comment(subreddit_comment):
	try:
		subreddit_comment.reply("Nobody Expects the Spanish Inquisition")
	except praw.exceptions.APIException:
			# reddit rate limit exceeded
			# wait 1s and process again
			print('Waiting')
			time.sleep(1)
			reply_to_comment(subreddit_comment)
	except Exception as e:
		print('Failed to reply to comment', e)
	else:
		# insert into redis to prevent re-commenting
		db.set(str(subreddit_comment),1)
# define subreddit
# in production read subreddit from sqs queue
subreddit = 'test'

# initialise subreddit
try:
	subreddit = reddit.subreddit("test")
except Exception as e:
	print("Subreddit Initialisation Error: ", e)
	sys.exit(1)

# list the comments from the subreddits
for subreddit_comment in subreddit.stream.comments():
	comment = subreddit_comment.body

	# check if comment has already been processed
	comment_processed_before = exists(subreddit_comment)
	if comment_processed_before == False:
		# check if the comment is relevant
		is_relevant = search_comment(comment)
		if is_relevant == True:
			reply_to_comment(subreddit_comment)
			














