from marshmallow import Schema, fields

class PaletteSchema(Schema):
    hex = fields.Str(required=True)
    rgb = fields.Str(required=True)
    role = fields.Str(required=True)

# You can now use this to validate/format data before returning it