from mailru_im_async_bot.filter import Filter, MessageFilter

class chaoticFilter(MessageFilter):
    def __init__(self, list_argz):
          self.list_argz = list_argz

    def filter(self, event):
        for c in self.list_argz:
            if isinstance(c, list):
                for j in c:
                    if j in event.data.get('text', '').lower().split():
                        is_command = True
                        break
                    else:
                        is_command = False
                if not(is_command):
                    return False
            else:
                if not(c in event.data.get('text', '').lower().split()):
                    return False
        return True

Filter.chaotic_args = chaoticFilter