import csv

def repeat_rows_quantity(file_name):

	# to which file to write to 
	write_f_name = file_name.split(".")[0]+"_modified.csv"
	write_to_file = open(write_f_name,'wb')
	writer = csv.writer(write_to_file,delimiter=',')

	# read the input csv file
	f_obj = open(file_name,"rb")
	reader2 = csv.reader(f_obj)
	
	row_num = 1
	for row in reader2:
		if(row_num == 1):
			writer.writerow(row)
			row_num += 1
			continue
		quantity = int(row[1])
		# write each row in the output csv quantity number of times
		for q in range(quantity):
			writer.writerow(row)

repeat_rows_quantity("aug_selected_features.csv")
repeat_rows_quantity("sept_selected_features.csv")
repeat_rows_quantity("oct_selected_features.csv")
repeat_rows_quantity("nov_selected_features.csv")