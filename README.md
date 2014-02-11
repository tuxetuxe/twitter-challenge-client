twitter-challenge-client
========================

# Requirements
* urllib
	+ pip install urllib
* httplib2
	+ pip install httplib2
* pudb (just for debugging)
	+ pip install pudb
	
# Usage

```
    # python twitter-challenge-client.py
```

# Available Commands

* **login**
    - Login in the service, retrieving the correct token.
* **logout**
    - Clears the authentication token. To proced you must login again
* **exit** | **quit**
    - Exits the client (and logsout, it not done yet1)

* **users**
    + Goes into the users section
    * **add <username> <name>**
        * Creates a new user
    * **follow <user> <user to follow>**
        * The user will follow the other user
    * **unfollow <user> <user to unfollow>**
        * The user will unfollow the other user
    * **following <user>**
        * Ouputs a list of who a user is following
    * **followers <user>**
        * Ouputs a list the followers of a user
        * 
* **tweets**
    + Goes into the users section
    * **add <username> <contents>**
        * Adds a new tweet to the user timeline
    * **timeline <username>**
        * Ouputs the timeline of a user

