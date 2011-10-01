import web
import subprocess

urls = (
    '/(.*)', 'RemoteControl'
)

app = web.application(urls, globals())

allowed_commands = ['play', 'stop']

class RemoteControl:        
    state = ""
    remote = None

    def __init__(self):
        self.state = "stopped"

    def GET(self, name):
        if not name: 
            return self.get_status()
        elif name in allowed_commands:
            return self.run_command(name)
        else:
            return "Unknown command"

    def run_command(self, command):
        if command == 'play':
            Remote.Instance().play()
            return "starting to play"
        elif command == 'stop':
            Remote.Instance().stop()
            return "stopping radio"

        return command

    def get_status(self):
        return "currently " + self.state

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
            self.player = subprocess.Popen(["vlc", "http://sverigesradio.se/topsy/direkt/164-hi-mp3.m3u"])

    def stop(self):
        if self.player is not None: 
            self.player.terminate()

if __name__ == "__main__":
    app.run()
