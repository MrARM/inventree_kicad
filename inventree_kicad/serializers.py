from rest_framework import serializers
from rest_framework.reverse import reverse_lazy

from part.models import Part, PartCategory, PartParameterTemplate


class KicadDetailedPartSerializer(serializers.ModelSerializer):
    class Meta:
        """Metaclass defining serializer fields"""
        model = Part

        fields = [
            'pk',
            'value',
            'footprint',
            'datasheet',
            'symbol',
            'reference',
            'description',
            'keywords',
            'optional_fields',
        ]

    pk = serializers.SerializerMethodField('get_pk')
    value = serializers.SerializerMethodField('get_value')
    footprint = serializers.SerializerMethodField('get_footprint')
    datasheet = serializers.SerializerMethodField('get_datasheet')
    symbol = serializers.SerializerMethodField('get_symbol')
    reference = serializers.SerializerMethodField('get_reference')
    description = serializers.SerializerMethodField('get_description')
    keywords = serializers.SerializerMethodField('get_keywords')

    optional_fields = serializers.SerializerMethodField('get_kicad_optional_fields')

    def get_api_url(self):
        """Return the API url associated with this serializer"""
        return reverse_lazy('api-kicad-part-list')

    def get_pk(self, part):
        return f'{part.pk}'

    def get_value(self, part):
        value = part.full_name
        try:
            value = f'{part.full_name.split("_")[1]}'
        except:
            pass

        return value

    def get_footprint(self, part):
        footprint = ""
        try:
            part_type = part.full_name.split('_')[0]

            if part_type == 'R':
                if part.full_name.split('_')[2] == '0402':
                    footprint = 'Resistor_SMD:R_0402_1005Metric'

                if part.full_name.split('_')[2] == '0603':
                    footprint = "Resistor_SMD:R_0603_1608Metric"

                if part.full_name.split('_')[2] == '0805':
                    footprint = 'Resistor_SMD:R_0805_2012Metric'

            elif part_type == 'C':
                footprint = "Capacitor_SMD:C_0805_2012Metric"

                if part.full_name.split('_')[2] == '0402':
                    footprint = 'Capacitor_SMD:R_0402_1005Metric'

                if part.full_name.split('_')[2] == '0603':
                    footprint = "Capacitor_SMD:R_0603_1608Metric"

                if part.full_name.split('_')[2] == '0805':
                    footprint = 'Capacitor_SMD:R_0805_2012Metric'

        except:
            pass

        return footprint

    def get_datasheet(self, part):
        for p in part.get_parameters():
            if p.name.lower() == 'datasheet':
                return f'{p.data}'
        return ""

    def get_symbol(self, part):
        symbol = ""

        try:
            part_type = part.full_name.split('_')[0]

            if part_type == 'R':
                symbol = "Device:R"

            elif part_type == 'C':
                symbol = "Device:C"

        except:
            pass

        return symbol

    def get_reference(self, part):
        reference = "X"
        try:
            reference = part.full_name.split('_')[0]
            if len(part.full_name.split('_')) <= 1:
                reference = "X"
        except:
            pass

        return reference

    def get_description(self, part):
        return part.notes

    def get_keywords(self, part):
        return part.keywords

    def get_kicad_optional_fields(self, part):
        para = part.get_parameters()

        paras = {}
        for p in para:
            if f'{p.template.name}'.lower() == "footprint":
                continue
            if f'{p.template.name}'.lower() == "datasheet":
                continue
            if f'{p.template.name}'.lower() == "symbol":
                continue

            paras[str(p.template).capitalize()] = f'{p.data}'

        paras['Inventree'] = f'{part.pk}'

        try:
            paras['Size'] = part.full_name.split('_')[2]
        except:
            pass

        try:
            paras['Rating'] = part.full_name.split('_')[3]
        except:
            pass

        try:
            paras['Tolerance'] = part.full_name.split('_')[4]
        except:
            pass

        idx = 1
        for a in part.attachments.all():
            paras[f'attachments_{idx}'] = f'{a}'
            idx += 1

        return paras


class KicadPreViewPartSerializer(serializers.ModelSerializer):
    class Meta:
        """Metaclass defining serializer fields"""
        model = Part

        # fields = [f.name for f in Part._meta.fields]

        fields = [
            'pk',
            'value',
        ]

    pk = serializers.SerializerMethodField('get_pk')
    value = serializers.SerializerMethodField('get_value')

    def get_api_url(self):
        """Return the API url associated with this serializer"""
        return reverse_lazy('api-kicad-part-list')

    def get_value(self, part):
        return part.full_name

    def get_pk(self, part):
        return f'{part.pk}'


class KicadCategorySerializer(serializers.ModelSerializer):
    class Meta:
        """Metaclass defining serializer fields"""
        model = PartCategory
        fields = [
            'pk',
            'name',
        ]

    pk = serializers.SerializerMethodField('get_pk')
    name = serializers.SerializerMethodField('get_name')

    def get_name(self, category):
        name = f'{category.pathstring} ({category.description})' if category.description else category.pathstring

        return name

    def get_pk(self, category):
        return f'{category.pk}'


class KicadPartParameterTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        """Metaclass defining serializer fields"""
        model = PartParameterTemplate
        fields = [
            'name',
        ]


class KicadFieldsSerializer(serializers.ModelSerializer):
    class Meta:
        """Metaclass defining serializer fields"""
        model = PartParameterTemplate
        fields = [
            'name',
        ]
