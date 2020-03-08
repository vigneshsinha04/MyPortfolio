import requests
import sys
import hashlib

def get_api_response(query_char):
	url = 'https://api.pwnedpasswords.com/range/' + query_char
	res = requests.get(url)
	if res.status_code != 200:
		print('Error occured')
	return res

def check_password(pwd):
	hashed_pwd = hashlib.sha1(pwd.encode('utf-8')).hexdigest().upper()
	first5_char, tail_tocheck = hashed_pwd[:5], hashed_pwd[5:]
	response = get_api_response(first5_char)

	hashes = (line.split(':') for line in response.text.splitlines())
	for tail, count in hashes:
		if tail == tail_tocheck:
			return count
	return 0

def main(inputs):
	message_list = []
	for password in inputs:
		count = check_password(password)

		if count:
			message_list.append(f'Your Password \"{password}\" appeared {count} times. Consider changing it!')
		else:
			message_list.append(f'Good news!! Your Password \"{password}\" was NOT found. Carry on.')	
	return message_list

if __name__ == "__main__":
	main(passwords)