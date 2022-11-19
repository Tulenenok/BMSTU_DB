""" СТРУКТУРА КЛАССОВ ДЛЯ ЗАДАНИЙ 1-2 """


class Person:
    """ Структура класса соответствует структуре таблицы persons """

    LIST_SCHEMA = [int, str, str, str, str, str]
    FIELD_SCHEMA = ['person_id', 'name', 'sub_name', 'pat_name', 'inp_date', 'notes']
    DICT_SCHEMA = {field: type_field for field, type_field in zip(FIELD_SCHEMA, LIST_SCHEMA)}

    def __init__(self, p_id: int, name: str, sub_name: str, pat_name: str, input_date: str, notes: str):
        self.person_id = p_id
        self.name = name
        self.sub_name = sub_name
        self.pat_name = pat_name
        self.inp_date = input_date
        self.notes = notes

    def get(self) -> dict:
        return {
            'person_id': self.person_id,
            'name': self.name,
            'sub_name': self.sub_name,
            'pat_name': self.pat_name,
            'inp_date': self.inp_date,
            'notes': self.notes
        }

    def __str__(self) -> str:
        return f'person_id: {self.person_id}, ' \
               f'name: {self.name}, ' \
               f'sub_name: {self.sub_name}, ' \
               f'pat_name: {self.pat_name}, ' \
               f'inp_date: {self.inp_date}, ' \
               f'notes: {self.notes}\n'


class Order:
    """ Структура класса соответствует структуре таблицы orders """

    LIST_SCHEMA = [int, str, int, int, str, int, int, str, str, int]
    FIELD_SCHEMA = ['order_id', 'order_date', 'order_no', 'order_state', 'shipment_date', 'price',
                    'shipment_price', 'note', 'inp_date', 'person_id']
    DICT_SCHEMA = {field: type_field for field, type_field in zip(FIELD_SCHEMA, LIST_SCHEMA)}

    def __init__(self, order_id: int, order_date: str, order_no: int, order_state: int, shipment_date: str,
                 price: int, shipment_price: int, note: str, inp_date: str, person_id: int):
        self.order_id = order_id
        self.order_date = order_date
        self.order_no = order_no
        self.order_state = order_state
        self.shipment_date = shipment_date
        self.price = price
        self.shipment_price = shipment_price
        self.note = note
        self.inp_date = inp_date
        self.person_id = person_id

    def get(self) -> dict:
        return {
            'order_id': self.order_id,
            'order_date': self.order_date,
            'order_no': self.order_no,
            'order_state': self.order_state,
            'shipment_date': self.shipment_date,
            'price': self.price,
            'shipment_price': self.shipment_price,
            'note': self.note,
            'inp_date': self.inp_date,
            'person_id': self.person_id,
        }

    def __str__(self):
        return f'order_id: {self.order_id}, '               \
               f'order_date: {self.order_date}, '           \
               f'order_no: {self.order_no}, '               \
               f'order_state: {self.order_state}, '         \
               f'shipment_date: {self.shipment_date}, '     \
               f'price: {self.price}, '                     \
               f'shipment_price: {self.shipment_price}'     \
               f'note: {self.note}, '                       \
               f'inp_date: {self.inp_date}, '               \
               f'person_id: {self.person_id}\n '


class OrderDetail:
    """ Структура класса соответствует структуре таблицы order_details """

    LIST_SCHEMA = [int, int, int, int, int, str]
    FIELD_SCHEMA = ['id', 'order_id', 'mat_id', 'quant', 'price', 'inp_date']
    DICT_SCHEMA = {field: type_field for field, type_field in zip(FIELD_SCHEMA, LIST_SCHEMA)}

    def __init__(self, id: int, order_id: int, mat_id: int, quant: int, price: int, inp_date: str):
        self.id = id
        self.order_id = order_id
        self.mat_id = mat_id
        self.quant = quant
        self.price = price
        self.inp_date = inp_date

    def get(self) -> dict:
        return {
            'id': self.id,
            'order_id': self.order_id,
            'mat_id': self.mat_id,
            'quant': self.quant,
            'price': self.price,
            'inp_date': self.inp_date
        }

    def __str__(self) -> str:
        return f'id: {self.order_id}, '        \
               f'id: {self.id}, '              \
               f'order_id: {self.order_id}, '  \
               f'mat_id: {self.mat_id}, '      \
               f'quant: {self.quant}, '        \
               f'price: {self.price}'          \
               f'inp_date: {self.inp_date}\n'


class Material:
    """ Структура класса соответствует структуре таблицы building_materials """

    LIST_SCHEMA = [int, int, str, str, int, int, str, str]
    FIELD_SCHEMA = ['mat_id', 'code', 'title', 'material', 'price', 'min_quant', 'is_deleted', 'inp_date']
    DICT_SCHEMA = {field: type_field for field, type_field in zip(FIELD_SCHEMA, LIST_SCHEMA)}

    def __init__(self, mat_id: int, code: int, title: str, material: str,
                 price: int, min_quant: int, is_deleted: str, inp_date: str):
        self.mat_id = mat_id
        self.code = code
        self.title = title
        self.material = material
        self.price = price
        self.min_quant = min_quant
        self.is_deleted = is_deleted
        self.inp_date = inp_date

    def get(self) -> dict:
        return {
            'mat_id': self.mat_id,
            'code': self.code,
            'title': self.title,
            'material': self.material,
            'price': self.price,
            'min_quant': self.min_quant,
            'is_deleted': self.is_deleted,
            'inp_date': self.inp_date,
        }

    def __str__(self) -> str:
        return f'mat_id: {self.mat_id}, '           \
               f'code: {self.code}, '               \
               f'title: {self.title}, '             \
               f'material: {self.material}, '       \
               f'price: {self.price}, '             \
               f'min_quant: {self.min_quant}'       \
               f'is_deleted: {self.is_deleted}'     \
               f'inp_date: {self.inp_date}\n'


