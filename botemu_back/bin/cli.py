import cmd

class Cli(cmd.Cmd):
    def __init__(self,app):
        cmd.Cmd.__init__(self)
        self.app=app
        self.prompt = "Command ?>"
    def do_setMoto(self, arg):
        try:
            moto = int(arg.split()[0])
            speed = int(arg.split()[1])
        except IndexError:
            print "Not enough arguments, Except 2 but given %d" % len(arg.split())
            return
        except ValueError:
            self.help_setMoto()
        try:
            self.app.bot.set_moto(moto, speed)
        except IndexError:
            print "No such moto"
            return
    def help_setMoto(self):
        print "Usage: setMoto moto speed"

    def do_AI(self, arg):
        try:
            AI = int(arg)
        except ValueError:
            self.help_AI()
            return
        try:
            print self.app.bot.get_sensor(AI)
        except IndexError:
            print "No such AI"
            return
    def help_AI(self):
        print "Usage: AI number"
        
class MyCli(object):
    pass
