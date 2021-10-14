
class Parameter(object):

    @classmethod
    def from_kwargs(self, **kwargs):
        obj = self()
        obj.fields = []
        for (field, value) in kwargs.items():
            obj.fields.append((field, value))
            setattr(obj, field, value)
        return obj

    def __repr__(self):
        obj = self
        fmt = [f'{__class__.__name__}(']
        size = len(obj.fields)
        for i, item in enumerate(obj.fields):
            fmt.append(f'{item[0]}={item[1]}')
            if i < size-1:
                fmt.append(', ')
        fmt.append(')')
        return ''.join(fmt)
