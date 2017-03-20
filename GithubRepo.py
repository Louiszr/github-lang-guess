from github import Github, GithubException

import sys, getpass

# Login before make an API request (optional)
apiuser = input('Type in Github username for API use: ')
if apiuser == '':
	github_instance = Github()
	print('Anonymous API requests may be restricted.')
else:
	apipswd = getpass.getpass('Type in the password of this user: ')
	github_instance = Github(apiuser, apipswd)

while True:
	username = input('\nPlease input the GitHub username you want to search, press Enter to quit: ')
	# Quit when no username is provided
	if username == '':
		break
	# Handle API-related exceptions
	try:
		user_repos = github_instance.get_user(username).get_repos()
	except GithubException as err:
		if err.status == 401:
			print('401: Please check if the login details are correct')
		elif err.status == 404:
			print('404: Cannot find this user '+username)
		else:
			print('ERROR: '+str(err.status))
		break
	# Initialise counters for two methods
	project_count = {}
	byte_count = {}
	repo_counter = 0
	for repo in user_repos:
		lang_dict = repo.get_languages()
		for lang in lang_dict:
			try:
				project_count[lang] += 1
				byte_count[lang] += int(lang_dict[lang])
			except KeyError:
				project_count[lang] = 1
				byte_count[lang] = int(lang_dict[lang])
		repo_counter += 1
		sys.stdout.write('\r'+str(repo_counter)+' repos has been processed...')
	# Output the project count results
	print('\n'+'='*20)
	print('Favourite language(s) based on the usage among repos')
	for k in project_count:
		if project_count[k] == max(project_count.values()):
			print('{} is used in {} repos'.format(k, project_count[k]))
	# Output the byte count results
	print('='*20)
	print('Favourite language(s) based on bytes written in this language among repos')
	for k in byte_count:
		if byte_count[k] == max(byte_count.values()):
			print('{} --- {} bytes in all repos were written in this language'.format(k, byte_count[k]))
	print('='*10+'Fnished'+'='*10)