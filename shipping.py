import iso6346


class ShippingContainer:

    HEIGHT_FT = 8.5
    WIDTH_FT = 8.0

    next_serial = 1337

    @classmethod
    def _generate_serial(cls):
        result = cls.next_serial
        cls.next_serial += 1
        return result

    @staticmethod
    def _make_bic_code(owner_code, serial):
        return iso6346.create(
            owner_code=owner_code,
            serial=str(serial).zfill(6)
        )

    @classmethod
    def _create_empty(cls, owner_code, length_ft, contents=[], **kwargs):
        return cls(owner_code, length_ft, contents, **kwargs)

    @classmethod
    def _create_with_items(cls, length_ft, owner_code, items, **kwargs):
        return cls(owner_code, length_ft, contents=list(items), **kwargs)

    def __init__(self, owner_code, length_ft, contents, **kwargs):
        self.owner_code = owner_code
        self.contents = contents
        self.length_ft = length_ft
        self.bic = self._make_bic_code(
            owner_code=owner_code,
            serial=ShippingContainer._generate_serial()
        )

    @property
    def volume_ft3(self):
        return self._calc_volume()

    def _calc_volume(self):
        return ShippingContainer.HEIGHT_FT * ShippingContainer.WIDTH_FT * self.length_ft


class RefrigeratorShippingContainer(ShippingContainer):
    MAX_CELSIUS = 4.0

    FRIDGE_VOLUME = 100

    def __init__(self, owner_code, length_ft, contents, *, celsius, **kwargs):
        super().__init__(owner_code, length_ft, contents, **kwargs)
        if celsius > RefrigeratorShippingContainer.MAX_CELSIUS:
            raise ValueError("Temperature too hot")
        self.celsius = celsius

    @staticmethod
    def _c_to_f(value):
        return value * 9/5 + 32

    @staticmethod
    def _f_to_c(value):
        return (value - 32) * 5/9

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        self._set_celsius(value)

    def _set_celsius(self, value):
        if value > RefrigeratorShippingContainer.MAX_CELSIUS:
            raise ValueError("Temperature too hot")
        self._celsius = value

    def _calc_volume(self):
        return super()._calc_volume - RefrigeratorShippingContainer.FRIDGE_VOLUME

    @property
    def fahrenheit(self):
        return RefrigeratorShippingContainer._c_to_f(self.celsius)

    @fahrenheit.setter
    def fahrenheit(self, value):
        self.celsius = RefrigeratorShippingContainer._f_to_c(value)

    @staticmethod
    def _make_bic_code(owner_code, serial):
        return iso6346.create(
            owner_code=owner_code,
            serial=str(serial).zfill(6),
            category="R"
        )


class HeadRefrigeratorShippingContainer(RefrigeratorShippingContainer):

    MIN_CELSIUS = -20

    def celsius(self, value):
        if HeadRefrigeratorShippingContainer.MIN_CELSIUS >= value:
            raise ValueError("Temperature is out of range")
        super()._set_celsius(value)
