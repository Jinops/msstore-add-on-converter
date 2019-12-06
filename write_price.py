import csv
from private import iap_product_csv
import time

#e.g) com.github.coin.10 => 9.99
def write_price_from_id() :
	product_list = []
	with open("./" + iap_product_csv, 'r') as csv_file:
		reader = csv.reader(csv_file)
		product_list = list(reader)

		for product in product_list :
			if (product[6] == ""):
				product[6] = (float(product[0].rsplit('.',1)[1])-0.01)

	with open("./" + iap_product_csv, 'w') as csv_file:		writer = csv.writer(csv_file)
		writer.writerows(product_list)

write_price_from_id()
