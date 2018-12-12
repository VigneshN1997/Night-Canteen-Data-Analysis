import csv

def convert_file_to_presence_absence(file_name):
	# which csv file to write the matrix to
	write_f_name = file_name.split(".")[0]+"_pa_matrix.csv"
	write_to_file = open(write_f_name,'wb')
	writer = csv.writer(write_to_file,delimiter=',')
	
	# dictionary where key is item id and value is 0/1(absent/present in transaction)
	present_item_dict = {} 
	
	f_obj = open(file_name,"rb")
	reader2 = csv.reader(f_obj)
	f_obj2 = open(file_name,"rb")
	reader3 = csv.reader(f_obj2)
	row_num = 1
	lis_item_names = [] # the list of item names(item_item id) sold that month
	item_ids = []		# the list of items sold that month
	
	# for each row in transactions file
	# this loop is to get the list of items sold that month
	for row in reader2:
		if(row_num == 1):
			row_num += 1
			continue
		# split the transaction to get list of items in that transaction
		trans = row[0].split("_")
		for item in trans:
			present_item_dict[int(item)] = 0
			if(int(item) not in item_ids):
				item_ids.append(int(item))
				lis_item_names.append("item_"+str(item))
	row_num = 1
	writer.writerow(lis_item_names)
	# for each row in transactions file
	for row in reader3:
		temp_dict = present_item_dict.fromkeys(present_item_dict,0)
		if(row_num == 1):
			row_num += 1
			continue
		transaction = row[0].split("_")
		for item in transaction:
			temp_dict[int(item)] = 1 # item present in transaction
		write_r = []
		for item_id in item_ids:
			write_r.append(temp_dict[item_id])
		# write the row of 0's and 1's to the csv output file
		writer.writerow(write_r)

convert_file_to_presence_absence("augTransactions.csv")
convert_file_to_presence_absence("septTransactions.csv")
convert_file_to_presence_absence("octTransactions.csv")
convert_file_to_presence_absence("novTransactions.csv")
