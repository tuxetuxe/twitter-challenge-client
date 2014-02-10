import cmd
import string, sys

#python debugger
#    pip install pudb
#import pudb; pu.db
	
NOT_LOGEDIN_PROMPT="[########-####-####-####-############]" + ':'

class UserCmd(cmd.Cmd):

    def do_add(self, arg):
        print "do_user_add"   
    def do_followers(self, arg):
        print "do_user_add"
    def do_following(self, arg):
        print "do_user_add"
    def do_follow(self, arg):
        print "do_tweet_follow"
    def do_unfollow(self, arg):
        print "do_tweet_follow"
                         
    def do_back(self, arg):
        return "stop"
        
class TweetCmd(cmd.Cmd):

    def do_add(self, arg):
        print "do_tweet_add"   
    def do_timeline(self, arg):
        print "do_user_add"
	
    def do_back(self, arg):
        return "stop"
        
class TwitterChallengeClient(cmd.Cmd):

    # authentication token holder
    authentication_token = None
    
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = NOT_LOGEDIN_PROMPT

    def postcmd(self, stop, line):
        if self.authentication_token is None :
            self.prompt = NOT_LOGEDIN_PROMPT
        else:
            self.prompt = "[" + str(self.authentication_token) + "]" + ':'
        return cmd.Cmd.postcmd(self,stop,line)

	# commands
    def do_login(self, arg):
        print "do_login"
        token = "1234"
        self.authentication_token = token

    def help_login(self):
        print "syntax: login",
        print "-- Login into the system"

    def do_logout(self, arg):
        self.authentication_token = None

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

# The main entry point    
if __name__ == '__main__':
	console = TwitterChallengeClient()
	console.cmdloop() 