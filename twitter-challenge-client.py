import sys, getopt
import cmd
import string, sys
import httplib2
import time
import datetime

#python debugger
#    pip install pudb
#import pudb; pu.db
	
NOT_LOGEDIN_PROMPT="[########-####-####-####-############]" + ':'

# host to connect to
host="localhost:8080"

# authentication token holder
authentication_token = None

def base_url():
    return "http://"+host+"/rest/"

    
def validateTokenExistence():
	is_token_valid = authentication_token is not None
	if not is_token_valid:
		print "You need to login before using this action"
	return is_token_valid

def doPost(request_url,content_type="application/json"):
    return doHttpRequest(request_url,"POST",content_type)
    
def doGet(request_url,content_type="application/json"):
    return doHttpRequest(request_url,"GET",content_type)
    
def doHttpRequest(request_url, method, content_type="application/json"):
    global authentication_token
    
    url = base_url() + request_url 

    if authentication_token is not None:
        url = url + "?token=" + authentication_token

    headers = {"Content-Type": content_type}
    
    print "\tURL: " + url
           
    # Get the HTTP object
    h = httplib2.Http(".cache")
    resp, content = h.request(url, method, headers=headers)
	
    print content;
    
    return content;

class UserCmd(cmd.Cmd):

    def do_add(self, arg):
        print "do_user_add"
        if not validateTokenExistence():
            return   
    def do_followers(self, arg):
        print "do_user_add"
        if not validateTokenExistence():
            return
    def do_following(self, arg):
        print "do_user_add"
        if not validateTokenExistence():
            return
    def do_follow(self, arg):
        print "do_tweet_follow"
        if not validateTokenExistence():
            return
    def do_unfollow(self, arg):
        print "do_tweet_follow"
        if not validateTokenExistence():
            return
                         
    def do_back(self, arg):
        return "stop"
        
class TweetCmd(cmd.Cmd):

    def do_add(self, arg):
        print "do_tweet_add"
        if not validateTokenExistence():
            return
    def do_timeline(self, arg):
        print "do_user_add"
        if not validateTokenExistence():
            return
	
    def do_back(self, arg):
        return "stop"
        
class TwitterChallengeClient(cmd.Cmd):

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = NOT_LOGEDIN_PROMPT

    def postcmd(self, stop, line):
        global authentication_token
        if authentication_token is None :
            self.prompt = NOT_LOGEDIN_PROMPT
        else:
            self.prompt = "[" + str(authentication_token) + "]" + ':'
        return cmd.Cmd.postcmd(self,stop,line)

	# commands
    def do_login(self, arg):
        global authentication_token
        if authentication_token is not None:
        	print "Already loggedin. Logout first"
        	return
        	
        token = doPost("security/login")
        if not token:
            token = None
        authentication_token = token

    def help_login(self):
        print "syntax: login",
        print "-- Login into the system"

    def do_logout(self, arg):
        global authentication_token
        
        if not validateTokenExistence():
            return
        
        token = doPost("security/logout")
        authentication_token = None

    def help_logout(self):
        print "syntax: logout",
        print "-- Logouts, after this you need to login again or exit"

    def do_exit(self, arg):
    	self.do_logout(arg)
    	sys.exit(1)
    	
    def help_exit(self):
        print "syntax: exits the client",
        print "-- Exits into the system"

    def do_users(self, arg):
        i = UserCmd()
        i.prompt = self.prompt[:-1]+'#Users:'
        i.cmdloop()
        
    def do_tweets(self, arg):
        i = TweetCmd()
        i.prompt = self.prompt[:-1]+'#Tweets:'
        i.cmdloop()        

    # shortcuts
    def do_quit(self, arg):
    	self.do_exit(arg)

def main(argv):
    global host
    
    opts, args = getopt.getopt(argv,"h",["host="])
        
    for opt, arg in opts:
        if opt  in ("-h", "--host"):
        	host = arg
        	print "Using host at: " + host
    
    console = TwitterChallengeClient()
    console.cmdloop()
	 
# The main entry point    
if __name__ == '__main__':
    main(sys.argv[1:])    
	