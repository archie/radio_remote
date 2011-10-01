import web

urls = (
    '/(.*)', 'RemoteControl'
)

app = web.application(urls, globals())

allowed_commands = ['play', 'stop']

class RemoteControl:        
    state = ""
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
            "http://sverigesradio.se/topsy/direkt/164-hi-mp3.m3u"
            return "starting to play"
        elif command == 'stop':
            return "stopping radio"

        return command

    def get_status(self):
        return "currently " + self.state

if __name__ == "__main__":
    app.run()
