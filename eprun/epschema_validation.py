# -*- coding: utf-8 -*-

def string_property_validation(value,schema_dict):
    ""
    
def number_property_validation(value,schema_dict):
    ""
    
def array_property_validation(value,schema_dict):
    ""
    


def property_validation(value,
                        type_=None,
                        enum=None,
                        minimum=None,
                        exclusive_minimum=False,
                        maximum=None,
                        exclusive_maximum=False):
    """Performs validation of a value against a schema.epJSON Property attributes.
    
    :param value: A value.
    :type value: Any.
    :param enum: The schema.epJSON enum.
    :type enum: list
    
    :returns: True if the value is valid against the schema.epJSON Property;
        otherwise False.
    :rtype: bool
        
    """

    return ((type_validation(value,type_) if type_ else True) and
            (enum_validation(value,enum) if enum else True) and
            (minimum_validation(value,minimum,exclusive_minimum) if minimum else True) and 
            (maximum_validation(value,maximum,exclusive_maximum) if maximum else True)
            )


def enum_validation(value,enum):
    """Performs validation of a value against a schema.epJSON enum.
    
    :param value: A value.
    :type value: Any.
    :param enum: The schema.epJSON enum.
    :type enum: list
    
    :returns: True if the value is valid against the schema.epJSON enum;
        otherwise False.
    :rtype: bool
        
    """
    return value in enum


def maximum_validation(value,maximum,exclusive_maximum):
    """Performs validation of a value against a schema.epJSON maximum.
    
    :param value: A value.
    :type value: Any.
    :param maximum: The schema.epJSON minimum.
    :type maximum: int or float
    :param exclusive_maximum: If True then the test is for values less than the maximum.
        If False then the test if for values less than or equal to the maximum.
        Default is False
    :type exclusive_maximum: True
    
    :returns: True if the value is 'less than' or 'less than or equal to' the schema.epJSON maximum;
        otherwise False.
    :rtype: bool
        
    """
    return value <= maximum


def minimum_validation(value,minimum,exclusive_minimum):
    """Performs validation of a value against a schema.epJSON minimum.
    
    :param value: A value.
    :type value: Any.
    :param minimum: The schema.epJSON minimum.
    :type minimum: int or float
    :param exclusive_minimum: If True then the test is for values greater than the minimum.
        If False then the test if for values greater than or equal to the minimum.
    :type exclusive_minimum: True
    
    
    :returns: True if the value is either 'greater than' or 'greater than and equal to' the schema.epJSON minimum;
        otherwise False.
    :rtype: bool
        
    """
    if exclusive_minimum:
        return value > minimum
    else:
        return value >= minimum


def type_validation(value,type_):
    """Performs validation of a value against a schema.epJSON type.
    
    :param value: A value.
    :type value: Any.
    :param type_: The schema.epJSON type.
    :type type_: str
    
    :returns: True if the value is valid against the schema.epJSON type;
        otherwise False.
    :rtype: bool
        
    """
    
    if type_=='string':
        return isinstance(value,str)
            
    elif type_=='number':
        return isinstance(value,int) or isinstance(value,float)
            
    elif type_=='array':
        return isinstance(value,list)
            
    else:
        raise Exception()