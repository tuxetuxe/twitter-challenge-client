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


class BaseTwitterChallengeCmd(cmd.Cmd):

    def get_args_list(self,arg,expected_args_count):
        args_list = arg.split()
        if len( args_list ) != expected_args_count:
            raise Exception("Invalid number of arguments. Expecting " + str( expected_args_count ) +" but got " + str( len( args_list ) ) )
            return
        return args_list
     
    def validate_token_existence(self):
    
	    is_token_valid = authentication_token is not None
	    if not is_token_valid:
		    raise Exception("You need to login before using this action")
	    return is_token_valid
    
    def precmd(self, line):
        try:
            if not ( line.startswith("login") or line.startswith("users") or line.startswith("tweets") or line.startswith("back") or line.startswith("exit") ) :
                self.validate_token_existence()
            return cmd.Cmd.precmd(self,line)
        except Exception, e:
            print str(e)
        
    def onecmd(self, line):
        try:
            return cmd.Cmd.onecmd(self,line)
        except Exception, e:
            print str(e)
        
class UserCmd(BaseTwitterChallengeCmd):

    def do_add(self, arg):
        print "do_user_add"
    def do_followers(self, arg):
        arg_list = self.get_args_list(arg, 1)
        timeline = doGet("users/"+arg_list[0]+"/followers")
    def do_following(self, arg):
        arg_list = self.get_args_list(arg, 1)
        timeline = doGet("users/"+arg_list[0]+"/following")
    def do_follow(self, arg):
        print "do_tweet_follow"
    def do_unfollow(self, arg):
        print "do_tweet_follow"
                         
    def do_back(self, arg):
        return "stop"
        
class TweetCmd(BaseTwitterChallengeCmd):

    def do_add(self, arg):
        print "do_tweet_add"
    def do_timeline(self, arg):
        arg_list = self.get_args_list(arg, 1)
        timeline = doGet("tweets/"+arg_list[0]+"/timeline")
	
    def do_back(self, arg):
        return "stop"
        
class TwitterChallengeClient(BaseTwitterChallengeCmd):

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
	