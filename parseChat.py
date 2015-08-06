import csv

MONTHS = {
	'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
}

class WAParser:
	chat = []
	trimChat = []

	def __init__(self, filesrc):
		with open(filesrc) as inputfile:
		    results = csv.reader(inputfile)

		    for row in results:
		    	self.chat.append(row)

	def parseRows(self):
		tempRow = []
		prev_len = 2

		# Concatenate messages in different lines
		for row in self.chat:
			if prev_len == 2:
				if len(row) >= 2 and row[0][0:3] in MONTHS:
					self.trimChat.append(tempRow)
					tempRow = row
					prev_len = 2

				#elif len(row) == 1:
				#	prev_len = 1
				#	tempRow = append_text_to_previous_row(row, tempRow)
				
				elif len(row) > 0 and row[0][0:3] not in MONTHS:
					prev_len = 1
					tempRow = self.append_text_to_previous_row(row, tempRow)
					print tempRow
			
			elif prev_len == 1:
				if len(row) == 1 and row[0][0:3] not in MONTHS:
					tempRow = self.append_text_to_previous_row(row, tempRow)
					prev_len = 1

				elif len(row) >= 2:
					self.trimChat.append(tempRow)
					tempRow = row
					prev_len = 2

	def formatProper(self):
		# Print in a readable form
		for row in self.trimChat[1:]:
			#print row

			# Add year for current year
			if row[1] != ' 2014':
				row.insert(1, '2015')
			else:
				row[1] = '2014'

			# Concatenate the whole message
			message = ''
			for col in row[2:]:
				message += col
			print message

			# Pull time out of message
			#time = message.split(' - ')[0]
			#author = message.split(' - ')[1].split(': ')[0]
			# print time + " " + author
			#text = message.split(' - ')[1].split(': ')[1]

			#print row[0] + " " + time + ", " + row[1] + ": [" + author + "] " + text

	def append_text_to_previous_row(self, row, tempRow):
		tempRow[-1] = tempRow[-1] + " " + row[0]
		#print tempRow
		return tempRow

def main():
	whatsapp = WAParser('chat.txt')
	whatsapp.parseRows()
	whatsapp.formatProper()

if __name__ == "__main__":
    main()

