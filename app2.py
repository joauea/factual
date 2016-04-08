from factual import Factual
from django.utils.encoding import smart_str
import pandas as pd
import string

# set up api
factual = Factual('6LQjVQD61xphjyDLW4zGQ1FowexFnZS8mhjeaMcB', '2NhZDHfH9DzCn1BnT7RaybL2CUvzzaMyrNvE6wyA')


# US postalcodes
postalcodes = pd.read_csv('/Users/oliver/Desktop/factual-galleries/USA/postalcodes_with_galleries.csv')
postalcodes = postalcodes['Postalcode'][0:1000]


# country codes
countries = {'United States': 'places-us',
'China': 'places-cn',
'Japan': 'places-jp',
'Germany': 'places-de',
'Italy': 'places-it',
'France': 'places-fr',
'Spain': 'places-es',
'United Kingdom': 'places-gb',
'Brazil': 'places-br',
'Canada': 'places-ca',
'Australia': 'places-au',
'South Korea': 'places-kr',
'Portugal': 'places-pt',
'Taiwan': 'places-tw',
'Switzerland': 'places-ch',
'Norway': 'places-no',
'Russia': 'places-ru',
'Sweden': 'places-se',
'Austria': 'places-at',
'Mexico': 'places-mx',
'Denmark': 'places-dk',
'South Africa': 'places-za',
'India': 'places-in',
'Indonesia': 'places-id',
'Finland': 'places-fi',
'Netherlands': 'places-nl',
'Belgium': 'places-be',
'Thailand': 'places-th',
'Philippines': 'places-ph',
'Singapore': 'places-sg',
'Argentina': 'places-ar',
'Hong Kong': 'places-hk',
'Ireland': 'places-ie',
'Poland': 'places-pl',
'Turkey': 'places-tr',
'New Zealand': 'places-nz',
'Malaysia': 'places-my',
'Israel': 'places-il',
'Chile': 'places-cl',
'Colombia': 'places-co',
'Hungary': 'places-hu',
'Vietnam': 'places-vn',
'Croatia': 'places-hr',
'Czech Republic': 'places-cz',
'Puerto Rico': 'places-pr',
'Luxembourg': 'places-lu',
'Venezuela': 'places-ve',
'Peru': 'places-pe',
'Greece': 'places-gr',
'Egypt': 'places-eg'}

# columns
cols = ['Name', 'Locality', 'Postalcode', 'Address', 'Region', 'Country', 'Neighborhood', 'Phone', 'Email', 'Website', 'Category Labels']

# alphabet
upper = list(string.ascii_uppercase)
lower = list(string.ascii_lowercase)


def postal_code_data(response, code):

	df = pd.DataFrame(columns=cols, index=[0])

	for x in response:

		bump = pd.DataFrame(columns=cols, index=[0])

		bump['Postalcode'] = str(code)

		try:
			bump['Name'] = smart_str(x['name'])
		except Exception:
			bump['Name'] = ''
		try:	
			bump['Locality'] = smart_str(x['locality'])
		except Exception:
			bump['Locality'] = ''
		try:
			bump['Address'] = smart_str(x['address'])
		except Exception:
			bump['Address'] = ''
		try:
			bump['Region'] = smart_str(x['region'])
		except Exception:
			bump['Region'] = ''
		try:
			bump['Country'] = smart_str(x['country'])
		except Exception:
			bump['Country'] = ''
		try:
			bump['Neighborhood'] = smart_str(x['neighborhood'])
		except Exception:
			bump['Neighborhood'] = ''
		try:
			bump['Phone'] = smart_str(x['tel'])
		except Exception:
			bump['Phone'] = ''
		try:
			bump['Email'] = smart_str(x['email'])
		except Exception:
			bump['Email'] = ''
		try:
			bump['Website'] = smart_str(x['website'])
		except Exception:
			bump['Website'] = ''
		try:
			bump['Category Labels'] = smart_str(x['category_labels'])
		except Exception:
			bump['Category Labels'] = ''

		df = df.append(bump)

	return df


def api_calls(location, codes, search_term):

	places = factual.table(countries[location])

	# results dataframe
	all_results = pd.DataFrame(columns=cols)

	# iterate through postal codes
	for y in codes:

		t = y

		if y < 10000:
			y = '0' + str(y)

		if y < 1000:
			y = '00' + str(y)

		# search with filters
		data = places.search(search_term).limit(50).filters( { "postcode": str(y), "category_labels": { "$includes_any": ['Art Dealers and Galleries'] } }).data()

		# api request
		results = postal_code_data(data, y)

		if len(results) > 49:
				
			data_A_D = places.search(search_term).limit(50).filters( { "postcode": str(y), "category_labels": { "$includes_any": ['Art Dealers and Galleries'] }, "name":{"$bwin": upper[:4] + lower[:4] } }).data()
			results = postal_code_data(data_A_D, y)
			all_results = all_results.append(results)
			print str(y) + ' (A - D) returned ' + str(len(results)) + ' rows.'

			if len(results) > 49:

				data_A = places.search(search_term).limit(50).filters( { "postcode": str(y), "category_labels": { "$includes_any": ['Art Dealers and Galleries'] }, "name":{"$bwin": upper[:1] + lower[:1] } }).data()
				results = postal_code_data(data_A, y)
				all_results = all_results.append(results)
				print str(y) + ' (A) returned ' + str(len(results)) + ' rows.'

				data_B = places.search(search_term).limit(50).filters( { "postcode": str(y), "category_labels": { "$includes_any": ['Art Dealers and Galleries'] }, "name":{"$bwin": upper[1:2] + lower[1:2] } }).data()
				results = postal_code_data(data_B, y)
				all_results = all_results.append(results)
				print str(y) + ' (B) returned ' + str(len(results)) + ' rows.'

				data_C_D = places.search(search_term).limit(50).filters( { "postcode": str(y), "category_labels": { "$includes_any": ['Art Dealers and Galleries'] }, "name":{"$bwin": upper[2:4] + lower[2:4] } }).data()
				results = postal_code_data(data_C_D, y)
				all_results = all_results.append(results)
				print str(y) + ' (C - D) returned ' + str(len(results)) + ' rows.'

				data_E_G = places.search(search_term).limit(50).filters( { "postcode": str(y), "category_labels": { "$includes_any": ['Art Dealers and Galleries'] }, "name":{"$bwin": upper[4:7] + lower[4:7] } }).data()
				results = postal_code_data(data_E_G, y)
				all_results = all_results.append(results)
				print str(y) + ' (E - G) returned ' + str(len(results)) + ' rows.'

				data_H_L = places.search(search_term).limit(50).filters( { "postcode": str(y), "category_labels": { "$includes_any": ['Art Dealers and Galleries'] }, "name":{"$bwin": upper[7:12] + lower[7:12] } }).data()
				results = postal_code_data(data_H_L, y)
				all_results = all_results.append(results)
				print str(y) + ' (H - L) returned ' + str(len(results)) + ' rows.'

				data_M_O = places.search(search_term).limit(50).filters( { "postcode": str(y), "category_labels": { "$includes_any": ['Art Dealers and Galleries'] }, "name":{"$bwin": upper[12:15] + lower[12:15] } }).data()
				results = postal_code_data(data_M_O, y)
				all_results = all_results.append(results)
				print str(y) + ' (M - O) returned ' + str(len(results)) + ' rows.'

				data_P_S = places.search(search_term).limit(50).filters( { "postcode": str(y), "category_labels": { "$includes_any": ['Art Dealers and Galleries'] }, "name":{"$bwin": upper[15:18] + lower[15:18] } }).data()
				results = postal_code_data(data_A_D, y)
				all_results = all_results.append(results)
				print str(y) + ' (P - S) returned ' + str(len(results)) + ' rows.'

				data_T_Z = places.search(search_term).limit(50).filters( { "postcode": str(y), "category_labels": { "$includes_any": ['Art Dealers and Galleries'] }, "name":{"$bwin": upper[18:] + lower[18:] } }).data()
				results = postal_code_data(data_T_Z, y)
				all_results = all_results.append(results)
				print str(y) + ' (T - Z) returned ' + str(len(results)) + ' rows.'
			
			data_E_K = places.search(search_term).limit(50).filters( { "postcode": str(y), "category_labels": { "$includes_any": ['Art Dealers and Galleries'] }, "name":{"$bwin": upper[4:11] + lower[4:11] } }).data()
			results = postal_code_data(data_E_K, y)
			all_results = all_results.append(results)
			print str(y) + ' (E - K) returned ' + str(len(results)) + ' rows.'

			data_L_to_P = places.search(search_term).limit(50).filters( { "postcode": str(y), "category_labels": { "$includes_any": ['Art Dealers and Galleries'] }, "name":{"$bwin": upper[11:16] + lower[11:16] } }).data()
			results = postal_code_data(data_L_to_P, y)
			all_results = all_results.append(results)
			print str(y) + ' (L - P) returned ' + str(len(results)) + ' rows.'

			data_Q_Z = places.search(search_term).limit(50).filters( { "postcode": str(y), "category_labels": { "$includes_any": ['Art Dealers and Galleries'] }, "name":{"$bwin": upper[16:] + lower[16:] } }).data()
			results = postal_code_data(data_Q_Z, y)
			all_results = all_results.append(results)
			print str(y) + ' (Q - Z) returned ' + str(len(results)) + ' rows.'

		else:
			print str(y) + ' returned ' + str(len(results)) + ' rows.'
			all_results = all_results.append(results)
		
	# output csv
	all_results = all_results.drop_duplicates()
	all_results.to_csv('/Users/oliver/Desktop/factual-galleries/USA/CRAWL2/0_1000_' + search_term.replace(' ','_') + '.csv')


# call United States, NYC postalcodes
api_calls('United States', postalcodes, 'Fine Art')



