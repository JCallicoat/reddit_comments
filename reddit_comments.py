
import os
import sys
import praw
import time
import datetime
from jinja2 import Template

username = sys.argv[1]
r = praw.Reddit('bot', user_agent='testing')
u = r.redditor(username)

page_num = 1
fullname = False

out_path = username
if not os.path.exists(out_path):
    os.mkdir(out_path)

while True:
  comments = []

  if not fullname:
    params = {}
  else:
    params = {'after': fullname}

  for c in u.comments.new(params=params):
    c.posted = datetime.datetime.fromtimestamp(
               int(c.created_utc)
             ).strftime('%b %d %I:%M %p')
    c.subname = c.subreddit.display_name
    comments.append(c)
    fullname = c.fullname

  with open('comments.html.jinja2') as fh:
      tmpl = Template(fh.read())

  out_file = '{}-comments-page-{}.html'.format(username, page_num)
  out_file = os.path.join(out_path, out_file)
  with open(out_file, 'w') as fh:
    fh.write(tmpl.render(username=username,
                         page_num=page_num,
                         comments=comments))
  print('Wrote {}'.format(out_file))

  page_num += 1
  time.sleep(10)
  if page_num == 11: # can't get more than 1000 comments via api
      break
