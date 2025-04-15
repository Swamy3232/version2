from ... import Command


class SetScaleTimeType(Command):
    # Type : 0 absolute, 1 relative, 2 auto
    # SaveAsUserPreference : 0 don't save, 1 save
    def __init__(self, window, type = 2, save_as_user_preference = 0):
        super().__init__(name=None, parameters=[window, str(type), str(save_as_user_preference)])
        return
