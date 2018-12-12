import csv

y = 20

def find_combos(combos_arr,transac):
	index = -1
	num_combos = 0
	# find the combo present in the december transaction
	for i in range(len(combos)):
		temp1 = set(transac.keys())
		temp2 = set(combos_arr[i])
		if(temp2.issubset(temp1)):
			index = i
			break
	# if no combo is present
	if(index == -1):
		return (-1,0)
	min_val = 99999
	# to find the number of combos purchased in the transaction
	for item in combos_arr[index]:
		if(transac[item] < min_val):
			min_val = transac[item]
	num_combos = min_val
	return (index,num_combos)


def extract_combos(file_name):
	f1 = open(file_name,"rb")
	reader1 = csv.reader(f1)
	# extract the combos from combos.csv file
	combos_list = []
	row_num = 1
	# for each row in combos.csv 
	for row in reader1:
		if(row_num == 1):
			row_num += 1
			continue
		combo = []
		i1 = int(row[0].split("_")[1])
		combo.append(i1)
		lis = row[1].split("and")
		for item in lis:
			item_id = int((item.strip()).split("_")[1])
			combo.append(item_id)
		combo.sort()
		# if the combo is already not put in combos_list
		if(combo not in combos_list):
			combos_list.append(combo)
	return combos_list
def compute_loss_in_profit(month_file,combos):
	f1 = open(month_file,"rb")
	reader1 = csv.reader(f1)
	f2 = open("monthwisePriceList.csv","rb")
	reader2 = csv.reader(f2)

	item_prices = {}		# dictionary with key as item id and value as item price
	old_sum_prices = []		# sum of prices of items in each combo
	combo_prices = []		# combo prices of each combo
	old_rev = 0				# old revenue
	new_rev = 0				# revenue after considering combos
	row_num = 1
	transactions_dict = {}	# dictionary storing transactions
	days = [i for i in range(1,15)]
	hours = [16,17,18,19,20,21,22,23,0,1,2]
		
	row_num = 1
	# reading item prices from monwisePriceList.csv
	for row in reader2:
		if(row_num == 1):
			row_num += 1
			continue
		item_id = int(row[0])
		selling_price_dec = float(row[6])
		item_prices[item_id] = selling_price_dec

	# calculating sum of prices of items in each combo and combo price too
	for combo in combos:
		sum_prices = 0
		k = len(combo)
		multiply_factor = (100-(float(y)/k))/float(100)
		for item_id in combo:
			sum_prices += item_prices[item_id]
		old_sum_prices.append(sum_prices)
		combo_price = multiply_factor*sum_prices
		combo_prices.append(combo_price)
	
	f_write = open("problem2.csv","wb")
	writer = csv.writer(f_write,delimiter=',')
	row1 = ["ItemID","oldPriceSum","newPrice","items"]
	writer.writerow(row1)
	uid = 1
	# creating the output file problem2.csv (to which old sum, combo price, items in combo are written)
	for i in range(len(combos)):

		row_to_write = [uid,old_sum_prices[i],combo_prices[i],str(combos[i])]
		writer.writerow(row_to_write)
		uid += 1

	# creating the dictionary for storing transactions
	for day in days:
		transactions_dict[day] = {}
		for hr in hours:
			transactions_dict[day][hr] = {}

	# print(days)
	row_num = 1
	# storing transactions along with quantity of each item bought in a transaction
	for row in reader1:
		if(row_num == 1):
			row_num += 1
			continue
		day = int(row[5].split("/")[1])
		hour = int(row[5].split(" ")[1].split(":")[0])
		# print(hour)
		bill_no = int(row[0])
		if(bill_no not in transactions_dict[day][hour].keys()):
			transactions_dict[day][hour][bill_no] = {}

		item_id = int(row[2])
		if(item_id not in transactions_dict[day][hour][bill_no].keys()):
			transactions_dict[day][hour][bill_no][item_id] = 0			
		transactions_dict[day][hour][bill_no][item_id] += int(row[3])

	# this loop is for calculating the old revenue and new revenue
	for day in transactions_dict.keys():
		for hr in transactions_dict[day].keys():
			for bill_no in transactions_dict[day][hr]:
				sum_prices = 0
				for item_id in transactions_dict[day][hr][bill_no]:
					sum_prices += transactions_dict[day][hr][bill_no][item_id]*item_prices[item_id]

				old_rev += sum_prices
				# find if combo exists in the transaction
				(index,num_combos) = find_combos(combos,transactions_dict[day][hr][bill_no])
				if(index == -1):
					new_rev += sum_prices
				else:
					sp = 0
					sp += num_combos*combo_prices[index]
					for item_id in transactions_dict[day][hr][bill_no]:
						if(item_id not in combos[index]):
							sp += transactions_dict[day][hr][bill_no][item_id]*item_prices[item_id]
					new_rev += sp
	# calculating the loss in revenue
	loss = ((new_rev - old_rev)/old_rev)*100
	print("loss:"+str(-1*loss) +"%")


combos = extract_combos("combos.csv")
compute_loss_in_profit("decSales.csv",combos)