import csv
def calculate_revenue_increase(month_file_name):

	f1 = open("monthwisePriceList.csv","rb")
	r1 = csv.reader(f1)
	f3 = open("newPrices.csv","rb")
	r3 = csv.reader(f3)
	f_obj = open(month_file_name,"rb")
	reader = csv.reader(f_obj)
	
	item_dict = {}			# this dictionary is used for penalty calculation
	old_prices_dec = {}		# dictionary key: item id value: old price in december
	new_prices = {}			# new prices : key is item id, 
	#value is a dictionary key: is hour number, value is a dictionary with key as student segment and value as [num hours,change in price]
	old_rev = 0				# december revenue with old prices
	new_rev = 0				# december revenue with new prices
	penalty = 0				# the penalty

	hour_weights = {1:1,2:4,3:9,4:16,5:25,6:36,7:50}
	segment_weights = {"F1":12,"F2":32,"F3":30,"F4":20,"F5":3,"H1":2,"H2":2,"others":1}
	student_segment_arr = ["F1","F2","F3","F4","F5","H1","H2","others"]
	hours_arr = [16,17,18,19,20,21,22,23,0,1,2]
	
	row_num = 1
	# for each row in monthwisePrice file
	for row in r1:
		if(row_num == 1):
			row_num += 1
			continue
		item_dict[int(row[0])] = {}
		new_prices[int(row[0])] = {}
		for hr in hours_arr:
			new_prices[int(row[0])][hr] = {}
			for segment in student_segment_arr:
				item_dict[int(row[0])][segment] = [0,0] # [num hours,change in price]
				new_prices[int(row[0])][hr][segment] = 0
				
	row_num = 1
	# for each row in newPrices.csv
	for row in r3:
		if(row_num == 1):
			row_num += 1
			continue
		# update the old_prices_dec dictionary
		if(int(row[0]) not in old_prices_dec.keys()):
			old_prices_dec[int(row[0])] = float(row[1])
		hour = int(row[2])
		if(hour >= 24):
			hour -= 24
		# update the old_prices_dec dictionary
		for i in range(len(student_segment_arr)):
			new_prices[int(row[0])][hour][student_segment_arr[i]] = float(row[i+3])
			# if for that segment in that hour there is a price change then only update the new prices dict
			if(float(row[1]) != float(row[i+3])):
				item_dict[int(row[0])][student_segment_arr[i]][0] += 1
				item_dict[int(row[0])][student_segment_arr[i]][1] = float(row[i+3])-float(row[1])
	row_num = 1
	# for each row in decSales.csv
	for row in reader:
		if(row_num == 1):
			row_num += 1
			continue
		# extract student segment and hour
		segment = row[4][0]+row[4][1]
		hour = ((row[5].split(" "))[1].split(":"))[0]
		# old revenue is the old price of item* quantity bought
		old_rev += int(row[3])*old_prices_dec[int(row[2])]
		
		# calculating new revenue
		if(segment in student_segment_arr):
			new_rev += int(row[3])*new_prices[int(row[2])][int(hour)][segment]
		else:
			new_rev += int(row[3])*new_prices[int(row[2])][int(hour)]["others"]
	# increase in revenue
	inc_in_rev = ((new_rev - old_rev)/old_rev)*100

	for item_id in item_dict:
		for segment in student_segment_arr:
			segment_weight = segment_weights[segment]
			hour_weight = 0
			if(item_dict[item_id][segment][0] > 6):
				hour_weight = hour_weights[7]
			elif(item_dict[item_id][segment][0] > 0):
				hour_weight = hour_weights[item_dict[item_id][segment][0]]
			# penalty calculation
			penalty += item_dict[item_id][segment][1]*hour_weight*segment_weight
	print(inc_in_rev)
	print(penalty)
calculate_revenue_increase("decSales.csv")
