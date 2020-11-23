from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
import requests
import subprocess
import os

#Proxies = {"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"}


class Extension(Extension):

    def __init__(self):
        super(Extension, self).__init__()
        self.preferences = {}
        
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        # events risen when the preferences change (on boot and on change)
        self.subscribe(PreferencesEvent, PreferencesEventListener())
        self.subscribe(PreferencesUpdateEvent, PreferencesEventListener())

        
class PreferencesEventListener(EventListener):
    """
    On boot and on preferences changes, update the preferences in the extension instance.
    """
    def on_event(self, event, extension):
        if hasattr(event, 'preferences'):
            extension.preferences = event.preferences
        else:
            extension.preferences[event.id] = event.new_value

            
class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        query = event.get_argument() or str()
        aur_helper = extension.preferences.get('aur_helper')
        if aur_helper is not None:
            try:
                aur_helper = str(aur_helper)
            except ValueError:
                pass

        always_use_helper = extension.preferences.get('always_use_helper') == 'Yes'
        
        if len(query.strip()) == 0:
            return RenderResultListAction([
                ExtensionResultItem(icon='icon.png',
                                    name='No input',
                                    on_enter=HideWindowAction())
            ])
        else:
            data = subprocess.Popen([aur_helper, "-Ss", str(query)], stdout = subprocess.PIPE)
            cmd = str(data.communicate())

            packages = [] # List of packages
            pkg_num = 0 # Number of packages
            i = 3 # Character index
            while i < len(cmd):
                packages.append([])
                repo = ""
                name = ""
                description = ""
                while i < len(cmd) and cmd[i] != '/':
                    repo += cmd[i]
                    i += 1
                i += 1
                while i < len(cmd) and cmd[i] != ' ':
                    name += cmd[i]
                    i += 1
                while i < len(cmd) and cmd[i] != '\\':
                    i += 1
                i += 6
                while i < len(cmd) and cmd[i] != '\\':
                    description += cmd[i]
                    i += 1
                packages[pkg_num].append(name)
                packages[pkg_num].append(description)
                packages[pkg_num].append(repo)
                pkg_num += 1
                i += 2

            del packages[len(packages) - 1]

            items = []
            for q in packages:
                if always_use_helper == true or q[2] == "aur":
                    items.append(ExtensionResultItem(icon='icon.png',
                                                     name=q[0] + "  (" + q[2] + ")",
                                                     description=q[1],
                                                     on_enter=CopyToClipboardAction("yay -S " + q[0])))
                else:
                    items.append(ExtensionResultItem(icon='icon.png',
                                                     name=q[0] + "  (" + q[2] + ")",
                                                     description=q[1],
                                                     on_enter=CopyToClipboardAction("sudo pacman -S " + q[0])))

            return RenderResultListAction(items)


if __name__ == '__main__':
    Extension().run()
