class ShippingContainer:

    next_serial = 1337

    @classmethod
    def _generate_serial(cls):
        result = cls.next_serial
        cls.next_serial += 1
        return result

    @classmethod
    def _create_with_empty(cls, owner_code, contents=[]):
        return cls(owner_code, contents)

    @classmethod
    def _create_with_items(cls, owner_code, contents):
        return cls(owner_code, contents)

    def __init__(self, owner_code, contents):
        self.owner_code = owner_code
        self.contents = contents
        self.serial = self._generater_serial()
