import csv
import json
from dateutil.parser import parse
from datetime import datetime as dt
from datetime import timedelta, date

# Filenames and paths
# CHANGE THIS TO YOUR OWN THING OR IT WON'T WORK
basePath = './familia'
textFileToParse = 'Familia.txt'
writeToJsonFile = basePath.join('/formatted_familia.json')
writeToCSVFile = basePath.join('/formatted_familia.csv')

MONTHS = {
	'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
}
start_date = parse('2014-10-01 00:00:00')
end_date = parse('2015-10-18 00:00:00')

per = 'day'

# Group by hour or day
if per == 'hour':
	formatS = "%Y-%m-%d %H"
elif per == 'day':
	formatS = "%Y-%m-%d"

# Format date according to grouping
def daterange(start_date, end_date):
	if per == 'hour':
		for n in range(int ((end_date - start_date).total_seconds() / 3600)):
			yield start_date + timedelta(0, n * 3600)

	elif per == 'day':
		for n in range(int ((end_date - start_date).days)):
			yield start_date + timedelta(n)

class WAParser:
	chat = []
	trimChat = []
	formatted_chat = []

	def __init__(self, filesrc):
		with open(filesrc) as inputfile:
		    results = csv.reader(inputfile)

		    for row in results:
		    	self.chat.append(row)

	def parseRows(self):
		previous_msg_w_metadata = []
		previous_has_metadata = True
		tempRow = []
		# Concatenate messages in different lines
		for row in self.chat:
			if len(row) >= 2 and row[0][:3] in MONTHS and row[1].strip() != '2014':
				row.insert(1, '2015')

		# Concatenate messages in different lines
		for row in self.chat:
			try:
				self.trimChat.append(tempRow)
				tempRow = row
			except ValueError:
				for col in row:
					tempRow[-1] = tempRow[-1] + " " + col
			except IndexError:
				pass

	def formatProper(self):
		# Print in a readable form
		for row in self.trimChat[1:]:
			try:
				# Pull time out of message

				timestring = row[1].split(' - ')[0]
				timestring = timestring.split('.')[0] + ':' + timestring.split('.')[1]
				time = self.parseTime(row[0], timestring)

				author = row[1].split(' - ')[1].split(': ')[0]

				message = row[1].split(' - ')[1].split(': ')[1]

				self.formatted_chat.append({
					'time': time,
					'author': author,
					'text': message
				})
			except IndexError:
				pass
			except ValueError:
				pass

	# Create an array with an object per day
	def bucket_by_day(self):
		self.day_buckets = {}
		for single_date in daterange(start_date, end_date):
			self.day_buckets[single_date.strftime(formatS)] = []

    # Put messges in day buckets
	def bucketify_data(self):
		for row in self.formatted_chat:
			print row['time']
			self.day_buckets[row['time'].strftime(formatS)].append({
				'time': row['time'].strftime(formatS),
				'author': row['author'],
				'text': row['text']
			})

		self.day_buckets_list = []
		for single_date in daterange(start_date, end_date):
			date = single_date.strftime(formatS)
			self.day_buckets_list.append({ date: self.day_buckets[date]  })

	def parseTime(self, dateString, timeString):
		return parse(dateString + " " + timeString.strip(), dayfirst=True)

	def write_to_json(self):
		with open(writeToJsonFile, 'w') as outfile:
		    json.dump(self.day_buckets_list, outfile)

	def write_to_csv(self):
		with open(writeToCSVFile, 'wb') as csvfile:
		    spamwriter = csv.writer(csvfile, delimiter=',',
		                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
		    for msg in self.formatted_chat:
		    	spamwriter.writerow([msg['time'], msg['author'], msg['text']])

def main():
	whatsapp = WAParser(textFileToParse)
	whatsapp.parseRows()
	whatsapp.formatProper()
	whatsapp.write_to_csv()
	whatsapp.bucket_by_day()
	whatsapp.bucketify_data()
	whatsapp.write_to_json()

if __name__ == "__main__":
    main()
