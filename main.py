from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.RunScriptAction import RunScriptAction
import os

class BudgieSessionExtension(Extension):

    def __init__(self):
        super(BudgieSessionExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        items = []
    	options = ['logout', 'restart', 'reboot', 'shutdown', 'halt']
        myList = event.query.split(" ")
        if len(myList) == 1:
            items.append(ExtensionResultItem(icon='images/reboot.png',
                                            name='Reboot',
                                            description='Reboot computer',
                                            on_enter=RunScriptAction("systemctl reboot", None)))
            items.append(ExtensionResultItem(icon='images/shutdown.png',
                                            name='Shutdown',
                                            description='Power off computer',
                                            on_enter=RunScriptAction("systemctl poweroff", None)))
            items.append(ExtensionResultItem(icon='images/logout.png',
                                            name='Logout',
                                            description='Logout from session',
                                            on_enter=RunScriptAction("systemctl restart display-manager", None)))

            return RenderResultListAction(items)
        else:
            myQuery = myList[1]
            included = []
            for option in options:
                if myQuery in option:
                    if option in ['shutdown', 'halt'] and 'shutdown' not in included:
                        items.append(ExtensionResultItem(icon='images/shutdown.png',
                                                        name='Shutdown',
                                                        description='Power off computer',
                                                        on_enter=RunScriptAction("systemctl poweroff", None)))
                        included.append('shutdown')
                    elif option in ['restart', 'reboot'] and 'reboot' not in included:
                        items.append(ExtensionResultItem(icon='images/reboot.png',
                                                    name='Reboot',
                                                    description='Reboot computer',
                                                    on_enter=RunScriptAction("systemctl reboot", None)))
                        included.append('reboot')
                    elif option in ['logout']:
                        items.append(ExtensionResultItem(icon='images/logout.png',
                                                    name='Logout',
                                                    description='Logout from session',
                                                    on_enter=RunScriptAction("systemctl restart display-manager", None)))

            return RenderResultListAction(items)

if __name__ == '__main__':
    BudgieSessionExtension().run()
