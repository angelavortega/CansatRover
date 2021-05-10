import csv

with open('data.csv', mode='r') as csv_file:
 
	csv_reader = csv.reader(csv_file, delimiter=',')
	
	i = 0     
	for row in csv_reader:
		if i < 3:
			for element in row:
				print(element, 'is type:' , type(element))
				i += 1
		else:
			break
		
