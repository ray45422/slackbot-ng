from abc import ABCMeta, abstractmethod
from slack_bolt import App
from pathlib import Path
import importlib
import re
import modules.g as g

class MsgHandler(metaclass=ABCMeta):
    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def eventType(self):
        pass

    @abstractmethod
    def description(self):
        pass

    @abstractmethod
    def descriptionDetail(self):
        pass

    @abstractmethod
    def author(self):
        pass

    @abstractmethod
    def canProcess(self):
        return True

    @abstractmethod
    def process(self, event, say):
        pass

    @abstractmethod
    def isPublic(self):
        pass

handlers = []
def onEvent(event, say):
    handled = []
    g.bot_token = say.client.token
    for h in handlers:
        et = h.eventType()
        if(et == None):
            if(h.canProcess(event)):
                handled.append(h)
                h.process(event, say)
            break
        for k in et.keys():
            etv = et[k]
            hasKey = k in event.keys()
            if(not hasKey and etv == None):
                continue
            if(not hasKey):
                break
            if(event[k] != et[k]):
                break
        else:
            if(h.canProcess(event)):
                handled.append(h)
                h.process(event, say)
    if(len(handled) == 0):
        print(event)
    else:
        print(f"{len(handled)} handlers processed")

def init(app: App):
    app.event(re.compile('.*'))(onEvent)
    for f in Path(__file__).parent.iterdir():
        name = f.stem
        if name[0] == '_':
            continue
        m = importlib.import_module('modules.handlers.' + name)
        print(f"loading module: {name}")
        hs = m.init()
        for h in hs:
            handlers.append(h)
