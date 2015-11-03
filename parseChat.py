import csv
from dateutil.parser import parse
from datetime import datetime as dt

MONTHS = {
	'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
}


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
		for row in self.chat:
			if len(row) == 2 and row[0][:3] in MONTHS:
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
				message = row[2]

				# Pull time out of message
				time = self.parseTime(row[0] + " " + row[1], message.split(' - ')[0])
				author = message.split(' - ')[1].split(': ')[0]

				self.formatted_chat.append({
					'time': time,
					'author': author,
					'text': message.split(' - ')[1].split(': ')[1]
				})
				print time
				print author
				print message.split(' - ')[1].split(': ')[1]
			except IndexError:
				pass
			except ValueError:
				pass

			#print row[0] + " " + time + ", " + row[1] + ": [" + author + "] " + text

	def parseTime(self, dateString, timeString):
		return parse(dateString + " " + timeString)

	def write_to_csv(self):
		with open('./sonia/formatted_sonia.csv', 'wb') as csvfile:
		    spamwriter = csv.writer(csvfile, delimiter=',',
		                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
		    for msg in self.formatted_chat:
		    	spamwriter.writerow([msg['time'], msg['author'], msg['text']])

		



def main():
	whatsapp = WAParser('sonia.txt')
	whatsapp.parseRows()
	whatsapp.formatProper()
	whatsapp.write_to_csv()

if __name__ == "__main__":
    main()

