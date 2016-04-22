__kupfer_name__ = _("Pass Manager")
__kupfer_sources__ = ("PassSource", )
__description__ = _("Passwords to clipboard")
__version__ = ""
__author__ = "Christopher Freeman <christopher.p.freeman@gmail.com"

from kupfer.objects import Action, Source, Leaf
from kupfer import utils
import os

class Password (Leaf):
    rank_adjust = 5
    def __init__(self, password):
        self.password = password
        Leaf.__init__(self, password, password)

    def get_actions(self):
        yield OpenPass()
    def get_icon_name(self):
        return "dialog-password"

class OpenPass (Action):
    rank_adjust = 5
    def __init__(self, name=None):
        super(OpenPass, self).__init__(name or _("Open Password"))

    def activate(self, leaf):
        utils.spawn_async(["pass", "-c", leaf.password])
        return

class PassSource (Source):
    def __init__(self):
        Source.__init__(self, name=_("Passwords"))

    def get_rank(self):
        return 5

    def is_dynamic(self):
        return True

    def get_items(self):
        root = os.environ['HOME'] + "/.password-store/"
        for path, subdirs, files in os.walk(root):
            for name in files:
                yield Password(os.path.splitext(os.path.relpath(os.path.join(path, name), root))[0])

    def get_icon_name(self):
        return "dialog-password"

    def provides(self):
        yield Password
