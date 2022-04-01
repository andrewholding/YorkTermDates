from urllib.request import urlopen
import datetime
import re
import math
from ics import Calendar, Event

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

def find_term(search_term):
	url = "https://www.york.ac.uk/about/term-dates/"
	page = urlopen(url)

	html_bytes = page.read()
	html = html_bytes.decode("utf-8")

	title_index = html.find(search_term)
	start_index = title_index + len(search_term)

	search_end = "</li>"
	end_index = html.find(search_end,start_index)
	
	if html.find("<br>",start_index) <  html.find(search_end,start_index) and html.find("<br>",start_index) > 0:
        	end_index = html.find("<br>",start_index)

	term = html[start_index:end_index]
	
	term = cleanhtml(term)	

	return term

autumn_term = find_term("Autumn Term</strong>: ")
print("Autumn Term:", autumn_term)

spring_term = find_term("Spring Term</strong>: ")
print("Spring Term:", spring_term)

summer_term = find_term("Summer Term (undergraduate)</strong>:&nbsp;Tuesday<strong>&nbsp;</strong>")
print("Summer Term:",summer_term)

c = Calendar()


def termCal(term):
	term_start = term.split(" - ")[0].strip()
	term_end = term.split(" - ")[1].strip()

	

	start_obj = datetime.datetime.strptime(term_start, '%d %B %Y')
	end_obj = datetime.datetime.strptime(term_end, '%d %B %Y')

	term_length = math.ceil((end_obj - start_obj).days/7)

	for x in range(0, term_length):
		print('Week', x+1, ":", start_obj.date() + datetime.timedelta(days=7*x))
		e = Event()
		e.name = "Week " + str(x+1)
		e.begin = start_obj.date() + datetime.timedelta(days=7*x)
		e.make_all_day()
		c.events.add(e)


termCal(autumn_term)
termCal(spring_term)
termCal(summer_term)
	
with open('my.ics', 'w') as f:
    f.write(str(c))

