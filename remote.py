import web
import subprocess

urls = (
    '/(.*)', 'RemoteControl'
)

app = web.application(urls, globals())

allowed_commands = ['play', 'stop']

class RemoteControl:        
    def GET(self, command):
        if not command: 
            return Remote.Instance().status()
        elif command in allowed_commands:
            return self.run(command)
        else:
            return "Unknown command"

    def run(self, command):
        if command == 'play':
            Remote.Instance().play()
            return "Starting radio"
        elif command == 'stop':
            Remote.Instance().stop()
            return "Stopping radio"

        return command

class Singleton:
    def __init__(self, decorated):
        self._decorated = decorated

    def Instance(self):
        try:
            return self._instance
        except AttributeError:
            self._instance = self._decorated()
            return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through the `Instance` method.')


@Singleton
class Remote(object):
    player = None
    def play(self):
        "http://sverigesradio.se/topsy/direkt/164-hi-mp3.m3u"
        if self.player is None:
            self.player = subprocess.Popen(["vlc", "-I rc", "http://sverigesradio.se/topsy/direkt/164-hi-mp3.m3u"])

    def stop(self):
        if self.player is not None: 
            self.player.terminate()
            self.player = None
    
    def status(self):
        if self.player is None:
            return "Radio is not running"
        else:
            return "Radio is running"

if __name__ == "__main__":
    app.run()
