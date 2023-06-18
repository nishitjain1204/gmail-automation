
**Gmail Automation Script Documentation**

Introduction: 

The Gmail Automation Script is a powerful tool designed to automate various tasks within Gmail. It leverages the Gmail API to interact with Gmail accounts programmatically, allowing users to perform actions such as reading emails and filtering through emails. This documentation will guide you through the installation, setup, and usage of the script.

1. Prerequisites:
   - A Gmail account
   - Python 3.x installed on your machine
   - pip (Python package installer) installed
   - Internet connectivity

2. Installation:
   - Open a terminal or command prompt.
   -  Clone this repository from GitHub:
        ```
        git clone https://github.com/nishitjain1204/gmail-automation
        ```
   - Navigate to the project directory:
        ```
        cd gmail-automation
        ```
   -  Install the required Python dependencies:
        ```
        pip3 install -r requirements.txt
        ```

3. Authentication:
   - Enable the Gmail API for your Google account by following the instructions in the Google API Console (https://console.developers.google.com/).
   - Obtain credentials (client_secret.json) for accessing the Gmail API and place it in the project directory.

4. Configuration:
   - Open the  `rules.json`  file in the project directory.
   - Modify the rules according to the requirements
   - The rules file should contain a list of rules
   - Following is a demo `rules.json`
```
[

{

"conditions": [

					{
				
						"field": "subject",
						
						"predicate": "contains",
						
						"value": "Application"
						
					}
		
			],
		
"actions": 
		
				{
				"move":"INBOX"
				"mark":"unread"
				}
				
			,
		
"predicate": "All"
		
		}
]
```

- The above rule selects emails where the subject contains string Application , marks it unread and moves to inbox. 
- A rule contains three main parts : `conditions` , `actions` , `predicate`
-  **conditions** are filters to be applied to the mails available . Conditions have three parts `field`,`predicate`,`value`.
	- `field` can have values (`from_email`,`subject`,`message`,`received_date` 
	- `predicate` can have values (`contains`,`does not contain`,`equals`,`does not equal`)
	- For string type fields - `contains`, `does not contain` and `equals`, `does not equal` - For date type field (Received) - `less than` / `greater than` for days / months.
	- `value` is the string to be used for comparison
 -  **actions** is a dictionary of actions to be performed on the emails selected after applying the above conditions. 
	 - Allowed keys are `move` and `mark`
	 - `move` : mail can be moved to  
		 `'INBOX', 'IMPORTANT', 'TRASH', 'SPAM', 'CATEGORY_FORUMS', 'CATEGORY_UPDATES', 'CATEGORY_PERSONAL', 'CATEGORY_PROMOTIONS', 'CATEGORY_SOCIAL', 'STARRED'
	 - `mark` : mail can be marked `read` and `unread`

5. After creating the rules file run the script using
        ```
        python3 main.py
        ```

6. Problems with the implementation
   - Can't move to drafts and sent due to the SDK issues

7. Future improvements
   - Add a logging system which generates a log of the actions performed
   - Create a validator for validating the rules file.
   - Create a separate rules builder to build the rules