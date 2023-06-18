import json

from gmail_functions import (
    
    mark_email_as_unread,
    mark_email_as_read,
    move_email_to_folder,
    get_valid_folders,
)

from sql_functions import (
    execute_query,
    create_database,
    fetch_emails
)

valid_folders = get_valid_folders()

def apply_rules(rules):
    
    # Apply rules and perform actions on emails
    for rule in rules:
       
        conditions = rule['conditions']
        actions = rule['actions']
        
        # Construct SQL query for conditions
        condition_sql = []
       
        for condition in conditions:
            
            field_name = condition['field']
            predicate = condition['predicate']
            value = condition['value']
            days = condition.get('days_older')

            if field_name == 'received_date_time':
                if predicate == 'less than':
                    if days:
                        condition_sql.append('''received_date < DATE('now', '-{}  days');'''.format(str(days)))
                    else :
                        condition_sql.append('''received_date < DATE({});'''.format(str(value)))
                elif predicate == 'greater than':
                    if days:
                        condition_sql.append('''received_date > DATE('now', '-{}  days');'''.format(str(value)))
                    else :
                        condition_sql.append('''received_date > DATE({});'''.format(str(value)))
                elif predicate == 'equals':
                    condition_sql.append(''' received_date = '{}' '''.format(str(value)))
            else:
                if predicate == 'contains':
                    condition_sql.append(''' {field} LIKE '%{value}%' '''.format(field=field_name,value=value))
                    
                elif predicate == 'does not contain':
                    condition_sql.append(''' {field} NOT LIKE '%{value}%' '''.format(field=field_name,value=value))
                    
                elif predicate == 'equals':
                    condition_sql.append(''' {field} = {value}'''.format(field=field_name,value=value))
                    
                elif predicate == 'does not equal':
                    condition_sql.append('''{field} != {value}'''.format(field=field_name,value=value))

        predicate = rule['predicate']
        
        if predicate == 'All':
            join_operator = ' AND '
        else:
            join_operator = ' OR '

        query = 'SELECT id from emails'+' WHERE ' + join_operator.join(condition_sql)
        email_id_list = execute_query(query)
        
        # Construct SQL query for actions
        action_sql = []
        
        if isinstance(actions,dict):
            
            if actions.get('move') in valid_folders:
                folder = actions.get('move')
                action_sql.append("folder='%s'" % folder)
                for email_id in email_id_list:
                    move_email_to_folder(message_id=email_id,folder_name=folder)
            
            if actions.get('mark'):
                if actions.get('mark') == 'read':
                    action_sql.append('is_read = 1')
                    for email_id in email_id_list:
                        mark_email_as_read(email_id=email_id)
                elif actions.get('mark') == 'unread':
                    action_sql.append('is_read = 0')
                    for email_id in email_id_list:
                        mark_email_as_unread(email_id=email_id)
        
        id_string = "'"+"','".join([id for id in email_id_list]) +"'"
        # Construct the final SQL query based on the predicate
        query = 'UPDATE emails SET ' + ', '.join(action_sql) + ' WHERE id in ({})'.format(id_string) 

        
        # Execute the SQL query
        execute_query(query=query)
        

    

# Main function
def main():
   
    
    create_database()
    
    update_db = input('Update database (Y,N)?')
    if update_db =='Y':
        fetch_emails()
        
    try:
        # Load rules from JSON file
        RULES_FILE = 'rules.json'
        with open(RULES_FILE) as file:
            rules = json.load(file)
            
            if len(rules)>=1:
                
                apply_rules(rules)
    except FileNotFoundError as f:
        print("Could not find rules file")
       



if __name__ == '__main__':
    main()
