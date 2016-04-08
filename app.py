from factual import Factual
from django.utils.encoding import smart_str
import pandas as pd
import string

# set up api
factual = Factual('6LQjVQD61xphjyDLW4zGQ1FowexFnZS8mhjeaMcB', '2NhZDHfH9DzCn1BnT7RaybL2CUvzzaMyrNvE6wyA')


# US postalcodes
postalcodes = pd.read_csv('/Users/oliver/Desktop/factual-galleries/all-us-postalcodes.csv')
postalcodes = postalcodes['Postalcode'].values[5000:10000]


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
cols = ['Name', 'Locality', 'Postalcode', 'Address', 'Region', 'Country', 'Neighborhood', 'Phone', 'Website', 'Category Labels']

# alphabet
lower = list(string.ascii_lowercase)
upper = list(string.ascii_uppercase)


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

	# dataframe to track postalcodes that have at least 1 gallery
	gallery_postalcodes = pd.DataFrame(columns=['postalcode'], index=range(0,len(postalcodes)))
	gallery_postalcodes['postalcode'] = postalcodes

	# iterate through postal codes
	for y in codes:

		# search with filters
		data = places.search(search_term).limit(50).filters( { "postcode": str(y), "category_labels": { "$includes_any": ['Museums','Arts', 'Art Dealers and Galleries'] } }).data()

		# api request
		results = postal_code_data(data, y)

		if len(results) == 1:
			gallery_postalcodes = gallery_postalcodes.loc[gallery_postalcodes['postalcode']!=y]

		# check length of response
		if len(results) > 49:

			data_w_website = places.search(search_term).limit(50).filters( { "postcode": str(y), "website": { "$blank": False }, "category_labels": { "$includes_any": ['Museums','Arts', 'Art Dealers and Galleries'] } }).data()
			results = postal_code_data(data_w_website, y)

			if len(results) > 49:
				
				data_w_website_A_to_B = places.search('').limit(50).filters( { "postcode": str(y), "category_labels": { "$includes_any": ['Museums','Arts', 'Art Dealers and Galleries'] }, "name":{"$bwin": upper[:2] + lower[:2] } }).data()
				results = postal_code_data(data_w_website_A_to_B, y)

				if len(results) > 49:

					data_w_website_A = places.search('').limit(50).filters( { "postcode": str(y), "category_labels": { "$includes_any": ['Museums','Arts', 'Art Dealers and Galleries'] }, "name":{"$bwin": upper[:1] + lower[:1] } }).data()
					results = postal_code_data(data_w_website_A, y)
					all_results = all_results.append(results)
					if len(results) > 49:
						print 'ALERT ' + str(y) + ' (A) returned ' + tr(len(results)) + ' rows and should be searched with stricter parameters.'
					else:
						print str(y) + ' (A) returned ' + str(len(results)) + ' rows.'

					data_w_website_B = places.search('').limit(50).filters( { "postcode": str(y), "category_labels": { "$includes_any": ['Museums','Arts', 'Art Dealers and Galleries'] }, "name":{"$bwin": upper[1:2] + lower[1:2] } }).data()
					results = postal_code_data(data_w_website_B, y)
					all_results = all_results.append(results)
					print str(y) + ' (B) returned ' + str(len(results)) + ' rows.'

					data_w_website_C_D = places.search('').limit(50).filters( { "postcode": str(y), "category_labels": { "$includes_any": ['Museums','Arts', 'Art Dealers and Galleries'] }, "name":{"$bwin": upper[2:4] + lower[2:4] } }).data()
					results = postal_code_data(data_w_website_C_D, y)
					all_results = all_results.append(results)
					print str(y) + ' (C - D) returned ' + str(len(results)) + ' rows.'

					data_w_website_E_H = places.search('').limit(50).filters( { "postcode": str(y), "category_labels": { "$includes_any": ['Museums','Arts', 'Art Dealers and Galleries'] }, "name":{"$bwin": upper[4:8] + lower[4:8] } }).data()
					results = postal_code_data(data_w_website_E_H, y)
					all_results = all_results.append(results)
					print str(y) + ' (E - H) returned ' + str(len(results)) + ' rows.'

					data_w_website_I_to_L = places.search('').limit(50).filters( { "postcode": str(y), "category_labels": { "$includes_any": ['Museums','Arts', 'Art Dealers and Galleries'] }, "name":{"$bwin": upper[8:12] + lower[8:12] } }).data()
					results = postal_code_data(data_w_website_I_to_L, y)
					all_results = all_results.append(results)
					print str(y) + ' (I - L) returned ' + str(len(results)) + ' rows.'

					data_w_website_M_to_P = places.search('').limit(50).filters( { "postcode": str(y), "category_labels": { "$includes_any": ['Museums','Arts', 'Art Dealers and Galleries'] }, "name":{"$bwin": upper[12:16] + lower[12:16] } }).data()
					results = postal_code_data(data_w_website_M_to_P, y)
					all_results = all_results.append(results)
					print str(y) + ' (M - P) returned ' + str(len(results)) + ' rows.'

					data_w_website_Q_to_S = places.search('').limit(50).filters( { "postcode": str(y), "category_labels": { "$includes_any": ['Museums','Arts', 'Art Dealers and Galleries'] }, "name":{"$bwin": upper[16:19] + lower[16:19] } }).data()
					results = postal_code_data(data_w_website_Q_to_S, y)
					all_results = all_results.append(results)
					print str(y) + ' (Q - S) returned ' + str(len(results)) + ' rows.'

					data_w_website_T_Z = places.search('').limit(50).filters( { "postcode": str(y), "category_labels": { "$includes_any": ['Museums','Arts', 'Art Dealers and Galleries'] }, "name":{"$bwin": upper[19:] + lower[19:] } }).data()
					results = postal_code_data(data_w_website_T_Z, y)
					all_results = all_results.append(results)
					print str(y) + ' (T - Z) returned ' + str(len(results)) + ' rows.'

					continue

				all_results = all_results.append(results)

				print str(y) + ' (A - B) returned ' + str(len(results)) + ' rows.'

				data_w_website_C_to_E = places.search('').limit(50).filters( { "postcode": str(y), "category_labels": { "$includes_any": ['Museums','Arts', 'Art Dealers and Galleries'] }, "name":{"$bwin": upper[2:5] + lower[2:5] } }).data()
				results = postal_code_data(data_w_website_C_to_E, y)
				all_results = all_results.append(results)

				print str(y) + ' (C - E) returned ' + str(len(results)) + ' rows.'

				data_w_website_F_to_I = places.search('').limit(50).filters( { "postcode": str(y), "category_labels": { "$includes_any": ['Museums','Arts', 'Art Dealers and Galleries'] }, "name":{"$bwin": upper[5:9] + lower[5:9] } }).data()
				results = postal_code_data(data_w_website_F_to_I, y)
				all_results = all_results.append(results)

				print str(y) + ' (F - I) returned ' + str(len(results)) + ' rows.'

				data_w_website_J_to_M = places.search(search_term).limit(50).filters( { "postcode": str(y), "category_labels": { "$includes_any": ['Museums','Arts', 'Art Dealers and Galleries'] }, "name":{"$bwin": upper[9:13] + lower[9:13] } }).data()
				results = postal_code_data(data_w_website_J_to_M, y)
				all_results = all_results.append(results)

				print str(y) + ' (J - M) returned ' + str(len(results)) + ' rows.'

				data_w_website_R_Z = places.search(search_term).limit(50).filters( { "postcode": str(y), "category_labels": { "$includes_any": ['Museums','Arts', 'Art Dealers and Galleries'] }, "name":{"$bwin": upper[17:] + lower[17:] } }).data()
				results = postal_code_data(data_w_website_R_Z, y)
				all_results = all_results.append(results)

				print str(y) + ' (R - Z) returned ' + str(len(results)) + ' rows.'


				continue

			else:
			
				print str(y) + ' with a website returned ' + str(len(results)) + ' rows.'

				all_results = all_results.append(results)

				data_no_website = places.search(search_term).limit(50).filters( { "postcode": str(y), "website": { "$blank": True }, "category_labels": { "$includes_any": ['Museums','Arts', 'Art Dealers and Galleries'] } }).data()
				results = postal_code_data(data_no_website, y)

				if len(results) > 49:
					print str(y) + ' without a website returned 50 (max) rows and could be searched with stricter parameters.'
				else:
					print str(y) + ' without a website returned ' + str(len(results)) + ' rows.'

				all_results = all_results.append(results)

		else:
			print str(y) + ' returned ' + str(len(results)) + ' rows.'
			all_results = all_results.append(results)
		
	# drop duplicates and output csv
	all_results = all_results.drop_duplicates()
	# all_results.to_csv('/Users/oliver/Desktop/factual-galleries/' + all_results['Locality'].value_counts().index[0] + '_' + search_term.replace(' ','_') + '.csv')
	all_results.to_csv('/Users/oliver/Desktop/factual-galleries/5000-10000_' + search_term.replace(' ','_') + '.csv')

	gallery_postalcodes.to_csv('/Users/oliver/Desktop/factual-galleries/5000-10000_gallery_present_postalcodes.csv')


# call United States, NYC postalcodes
api_calls('United States', postalcodes, 'Gallery')


