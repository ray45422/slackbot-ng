from abc import ABCMeta, abstractmethod
from slack_bolt import App
from pathlib import Path
import importlib

class MsgHandler(metaclass=ABCMeta):
    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def eventType(self):
        pass

    @abstractmethod
    def matchers(self):
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
    def process(self, event, say):
        pass

    @abstractmethod
    def isPublic(self):
        pass

handlers = {}

def init(app: App):
    for f in Path(__file__).parent.iterdir():
        name = f.stem
        if name[0] == '_':
            continue
        m = importlib.import_module('modules.handlers.' + name)
        handlers[name] = m.Handler()
    for n in handlers.keys():
        h = handlers[n]
        app.event(h.eventType())(h.process)
