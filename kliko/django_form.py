
from django.forms import CharField, FloatField, FileField, BooleanField, IntegerField, ChoiceField
from form_utils.forms import BetterForm

field_map = {
    'char': CharField,
    'float': FloatField,
    'file': FileField,
    'bool': BooleanField,
    'int': IntegerField,
    'choice': ChoiceField,
}


def formClassFactory(parsed):
    all_fields = {}
    fieldsets = []
    for section in parsed['sections']:
        fields_in_section = []

        for field in section['fields']:
            kwargs = {}
            for kwarg in ('initial', 'max_length', 'label', 'help_text', 'file'):
                if kwarg in field:
                    kwargs[kwarg] = field[kwarg]
            if 'choices' in field:
                kwargs['choices'] = field['choices'].items()
            fields_in_section.append(field['name'])
            all_fields[field['name']] = field_map[field['type']](**kwargs)

        fieldsets.append((section['name'],
                          {'fields': fields_in_section,
                           'description': section['description']}
                          ))

    Meta = type('Meta', (), {'fieldsets': fieldsets})
    all_fields['Meta'] = Meta

    return type('Form', (BetterForm,), all_fields)


def generate_form(parsed):
    """
    Generate a django form from a parsed scientific compute string
    """
    return formClassFactory(parsed)
