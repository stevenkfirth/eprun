# -*- coding: utf-8 -*-


import json
import jsonpi
import os
import re
from uuid import uuid4
import collections.abc

#from .epinput_object import EPInputObject


def read_idf(idf,
             schema_epJSON):
    """Reads an EnergyPlus idf file.
    
    :param epJSON: The idf input file
    :type epJSON: filepath, string
    :param schema_epJSON: The EnergyPlus epJSON schema
    :type schema_epJSON: filepath, dict, JSONSchemaSchemaObject
    
    :returns: The equivalent epJSON file as a dictionary.
    :rtype: dict
    
    
    """
    
    # load idf
    try:
        with open(idf) as f:
            st=f.read()
    except FileNotFoundError:  # assume an idf string has been passed
        st=idf
    #print(st)
    
    # load schema_epJSON
    if isinstance(schema_epJSON,str):
        with open(schema_epJSON) as f:
            json_value=json.load(f)
        schema=jsonpi.JSONSchemaSchemaObject(json_value)
    elif isinstance(schema_epJSON,dict):
        schema=jsonpi.JSONSchemaSchemaObject(schema_epJSON)
    elif isinstance(schema_epJSON,jsonpi.JSONSchemaSchemaObject):
        schema=schema_epJSON
    #print(schema)
    
    # clean and format as a list
    st=_clean_and_format_idf_string(st)
    #print(st)
    
    # form epJSON dictionary
    epjson={}
    for object_type,*field_values in st:
        
        #print('object_type:',object_type)  # i.e. 'Version', 'Building' etc.
        
        # update object_type if not valid in schema
        if not object_type in schema.properties:  # object type not in schema
                                                  # in some cases they are in different case (e.g. all upper case)
            for name in schema.properties.names():
                if name.lower()==object_type.lower():
                    object_type=name
                    break
                
        object_epjson={}
        object_name=str(uuid4())
        
        # get schema objects
        object_schema=schema.properties[object_type]  # JSONSchemaSchemaObject
        #print('object_schema:', object_schema)  # i.e. {'patternProperties': {'.*':
        object_legacy_idd=object_schema.legacy_idd
        #print('object_legacy_idd:', object_legacy_idd)  # i.e. ['version_identifier']
        object_properties=object_schema.patternProperties.schemas()[0].properties
        #print('object_properties:', object_properties)
        
        # loop through non-extensible field values
        for i, field_value in enumerate(field_values[:len(object_legacy_idd.fields)]):
            
            #print('field_value:', field_value)
            
            field_name=object_legacy_idd.fields[i]
            #print('field_name:', field_name)
            
            if field_value=='':
                continue
            
            if i==0 and field_name=='name':
            
                object_name=field_value
                    
            else:
            
                field_type=object_legacy_idd.field_info[field_name].field_type
                #print('field_type:',field_type)
                
                enums=object_properties[field_name].get('enum')
                #print(enums)
                
                if field_type=='a':
                    
                    if enums:  # if an enum field exists
                        if field_value in enums:  #  if field value is in the enums list
                            epjson_value=field_value
                        else:  # if not see whether it exists with different case (Aa)
                            for enum in enums:
                                if field_value.lower()==enum.lower():
                                    epjson_value=enum
                                    break
                            else:
                                raise Exception
                    else:
                        epjson_value=field_value
                        
                elif field_type=='n':
                    try:
                        epjson_value=float(field_value)
                    except ValueError:
                        epjson_value=field_value
                else:
                    raise Exception
        
                object_epjson[field_name]=epjson_value
        
        # loop through extensible field values
        if 'extension' in object_legacy_idd:
            
            epjson_name=object_legacy_idd.extension
            epjson_subnames=object_legacy_idd.extensibles
            
            epjson_value=[]
            
            for i in range(len(object_legacy_idd.fields),
                           len(field_values),
                           len(epjson_subnames)):
                
                
                epjson_subobject={}
                for j,subname in enumerate(epjson_subnames):
                    
                    #print('subname:', subname)
                    
                    if i+j>=len(field_values):   # if end is reeached part way through a subnames iteration
                        break
                    
                    field_value=field_values[i+j]
                    #print('field_value:', field_value)
                    
                    field_type=object_legacy_idd.field_info[subname].field_type
                    #print('field_type:',field_type)
                    
                    if field_type=='a':
                        epjson_subvalue=field_value
                    elif field_type=='n':
                        try:
                            epjson_subvalue=float(field_value)
                        except ValueError:
                            epjson_subvalue=field_value
                    else:
                        raise Exception
            
                    epjson_subobject[subname]=epjson_subvalue
                    
                epjson_value.append(epjson_subobject)
            
            object_epjson[epjson_name]=epjson_value
        
        
        # add object epjson
        epjson.setdefault(object_type,{})[object_name]=object_epjson
        
    return epjson
        

        
def _clean_and_format_idf_string(st):
    """Cleans an idf string and reformats as a list.
    
    :rtype: str
    
    """
    # removes the comments
    st=re.sub(r'!.*\n','',st)
    #print(st)
    
    # split by ';'
    a=st.split(';')  # gives a list of object strings
    #print(a)
    
    # split by ','
    b=[a1.split(',') for a1 in a] # a list of object lists
    #print(b)
    
    # remove whitespace and empty objects
    b=[[b2.strip() for b2 in b1] for b1 in b if len(b1)>1]
    #print(b)
    
    return b
    


class EPJSON(jsonpi.JSONObject):
    """Represents the root object of an epJSON file.
    
    Subclass of jsonpi.JSONObject.
    
    :param epJSON: The epJSON input file
    :type epJSON: filepath, dict, JSONObject
    :param schema_epJSON: The EnergyPlus epJSON schema
    :type schema_epJSON: filepath, dict, JSONSchemaSchemaObject
    
    
    """
    
    def __init__(self,
                 epJSON,
                 schema_epJSON):
        ""
        
        # load epJSON
        if isinstance(epJSON,str):
            with open(epJSON) as f:
                json_value=json.load(f)
            self._dict=json_value
        elif isinstance(epJSON,dict):
            self._dict=epJSON
        elif isinstance(epJSON,jsonpi.JSONObject):
            self._dict=epJSON._dict
            
        # load schema_epJSON
        if isinstance(schema_epJSON,str):
            with open(schema_epJSON) as f:
                json_value=json.load(f)
            self._schema=jsonpi.JSONSchemaSchemaObject(json_value)
        elif isinstance(schema_epJSON,dict):
            self._schema=jsonpi.JSONSchemaSchemaObject(schema_epJSON)
        elif isinstance(schema_epJSON,jsonpi.JSONSchemaSchemaObject):
            self._schema=schema_epJSON
            
            
    
    
class EPJSONObject(jsonpi.JSONObject):
    """
    """
    
    
    
    





# class EPInput_old(collections.abc.MutableSequence):
#     """A class for an EnergyPlus .idf or .epJSON input file.
    
#     An EPInput object is a MutableSeqence, with methods similar to a list.
    
#     :param fp: The filepath of an .idf or .epJSON file.
#         This can be relative or absolute.
#         Optional, if not supplied then a blank EPInput object is returned.
#     :type fp: str
#     :param schema: The EnergyPlus schema for the .idf or .epJSON file. 
#         Required for parsing an .idf file.
#         Required for validation.
#     :type schema: EPSchema
        
#     .. rubric:: Code Example
        
#     .. code-block:: python
           
#        >>> from eprun import EPInput
#        >>> fp_idf='1ZoneUncontrolled.idf'
#        >>> schema=EPSchema('Energy+.schema.epJSON')
#        >>> epi_idf=EPInput(fp_idf,schema)
#        >>> print(type(epi_idf))
#        <class 'eprun.epinput.EPInput'>
#        >>> print(len(epi_idf))
#        53
       
#     .. seealso::
    
#        EnergyPlus Essentials, page 19.
#        https://energyplus.net/quickstart
       
#     """
    
#     def __delitem__(self,index):
#         ""
#         del self._epinputobjects[index]
        
#     def __init__(self,
#                  fp=None,
#                  schema=None):
#         ""
#         self._fp=fp
#         self._schema=schema
#         self._epinputobjects=[]
            
#         # read file
#         if os.path.splitext(fp)[1]=='.epJSON':
#             with open(fp,'r') as f:
#                 d=json.load(f)
        
#         elif os.path.splitext(fp)[1]=='.idf':
#             with open(fp,'r') as f:
#                 st=f.read()
#                 d=self._parse_idf(st)
    
#         # convert epjson dict to list of epinputobjects
#         for object_type,objects_dict in d.items():
#             #print(object_type)
#             for object_id,property_dict in objects_dict.items():
#                 #print(object_id)
#                 o=EPInputObject(object_type=object_type,
#                                 name=object_id,
#                                 schema=self._schema,
#                                 **property_dict)
#                 #o.__dict__['epinput']=self
#                 #o.__dict__['object_type']=object_type
#                 #o.__dict__['name']=object_id
#                 #o.__dict__.update(property_dict)
#                 self._epinputobjects.append(o)
                  
        
#     def __getitem__(self,index):
#         """Returns the objects with object_type = key
        
#         :rtype: dict (str,EPInputObject)
        
#         """
#         try:
#             return self._epinputobjects[index]
#         except TypeError:  # index is a string?
#             return self.get_objects(object_type=index)
        
    
#     def __len__(self):
#         ""
#         return len(self._epinputobjects)
    
    
#     def __setitem__(self,index,value):
#         ""
#         self._epinputobjects[index]=value
    
    
#     def _parse_idf(self,st):
#         """Parses an idf string and returns a dictionary equivalent to the .epJSON dict
        
#         :param st: A string of the entire .idf file
#         :type st: str
        
#         :rtype: dict
        
#         """
#         def _convert_arg_to_value(arg,schema_property_object):
#             ""
#             p=schema_property_object
#             try:
#                 type_=p['type'] # schema property has a 'type' property
            
#                 if type_=='number':
                    
#                     if arg=='':
#                         raise ValueError()
#                     else:
#                         value=float(arg)
                
#                 elif type_=='string':
                    
#                     value=arg
                    
#                 else:
                    
#                     raise Exception()
                
                
#             except KeyError: # schema property does not have a 'type' property
                
#                 if 'anyOf' in p:
                    
#                     try:
#                         value=float(arg)
#                     except ValueError:
#                         value=arg
                        
#                 else:
                    
#                     raise Exception()
                
#             return value
        
#         #print(st.encode())
        
#         # removes the comments
#         st=re.sub(r'!.*\n','',st)
#         #print(st)
        
#         # split by ';'
#         a=st.split(';')  # gives a list of object strings
#         #print(a)
        
#         # split by ','
#         b=[a1.split(',') for a1 in a] # a list of object lists
#         #print(b)
        
#         # remove whitespace and empty objects
#         b=[[b2.strip() for b2 in b1] for b1 in b if len(b1)>1]
#         #print(b)
        
#         # form dictionary
#         d={}
#         for object_type,*args in b:
            
#             print('object_type:',object_type)
            
#             # get schema objects
#             schema_object_type=self._schema.get_object_type(object_type)
#             legacy_idd_fields=schema_object_type.legacy_idd_fields
#             property_names=schema_object_type.property_names
            
#             # adjustments if object has a defined name in the schema
#             if 'name' in schema_object_type:
#                 object_name=args[0]
#                 args=args[1:]
#                 legacy_idd_fields=legacy_idd_fields[1:]
#             else:
#                 object_name=uuid4()
                
#             #print('object_name',object_name)
#             #print('args',args)
#             #print('fields',fields)
#             #print('property_names',property_names)
            
#             # create the object properties dictionary
#             properties={}
#             i=0
#             while i<len(args):
                
#                 try:
                    
#                     # get property value and key
#                     arg=args[i]
#                     legacy_idd_field=legacy_idd_fields[i] # this will raise the IndexError is the object is 'extensible'
                    
#                     #print('arg:',arg)
#                     #print('legacy_idd_field:',legacy_idd_field)
                    
#                     # get schema property object
#                     p=schema_object_type.get_property(legacy_idd_field)
                    
#                     try:
#                         value=_convert_arg_to_value(arg, p)
#                         properties[legacy_idd_field]=value
#                     except ValueError:
#                         pass
                    
#                     i+=1
                    
                    
#                 except IndexError: # if the object includes extensible properties
                    
#                     # get extensible property name
#                     property_name=property_names[-1] 
                
#                     #print('property_name', property_name)
                    
#                     # get schema property object
#                     p=schema_object_type.get_property(property_name)
                    
#                     d1=properties.setdefault(p.name,[])
                    
#                     d2={}
#                     for k,v in p['items']['properties'].items():
                        
#                         #print(k,v)
                        
#                         if 'type' in v:
#                             t=v['type']
#                             if t=='number':
#                                 value=float(args[i])  
#                             elif t=='string':
#                                 value=args[i]
#                             else:
#                                 raise Exception()
                                
#                         elif 'anyOf' in v:
#                             types=[x['type'] for x in v['anyOf']]
#                             if 'number' in types:
#                                 try:
#                                     value=float(args[i])  
#                                 except ValueError:
#                                     value=args[i]
#                             elif 'string' in types:
#                                 value=args[i]
#                             else:
#                                 raise Exception()
                                
#                         else:
#                             raise Exception()
#                         #print('value',value)
                        
                        
#                         d2[k]=value
#                         i+=1
                    
#                     d1.append(d2)
                
                     
#             #print('properties',properties)
            
#             # get (or create) the object_type_dict
#             obj_type_dict=d.setdefault(object_type,{})
            
#             # add object item to object_type_dict
#             obj_type_dict[object_name]=properties
            
#         #print('d',d)
        
#         return d
        
    
#     def get_object(self,
#                    name):
#         """Returns the first EPInputObject with a name of 'name'
        
#         :param name: The object name.
#         :type name: str
        
#         :raises KeyError: If object does not exist .
        
#         :rtype: EPInputObject        
        
#         .. rubric:: Code Example
        
#         .. code-block:: python
               
#            >>> from eprun import EPInput
#            >>> fp_idf='1ZoneUncontrolled.idf'
#            >>> schema=EPSchema('Energy+.schema.epJSON')
#            >>> epi=EPInput(fp_idf,schema)
#            >>> obj=epi.get_object('Simple One Zone (Wireframe DXF)')
#            >>> print(obj)
#            <EPInputObject (Building, Simple One Zone (Wireframe DXF))>
            
#         """
#         for o in self:
#             if o.name==name:
#                 return o
#         raise KeyError
        
    
#     def get_objects(self,
#                     **kwargs):
#         """Returns a list of EPInputObjects.
        
#         :param kwargs: A keyword argument set to filter on.
        
#         :rtype: list
        
#         .. rubric:: Code Example
        
#         .. code-block:: python
               
#            >>> from eprun import EPInput
#            >>> fp_idf='1ZoneUncontrolled.idf'
#            >>> schema=EPSchema('Energy+.schema.epJSON')
#            >>> epi=EPInput(fp_idf,schema)
#            >>> objs=epi.get_objects(surface_type='Floor')
#            >>> print(objs)
#            [<EPInputObject (BuildingSurface:Detailed, Zn001:Flr001)>]
        
#         """
        
#         if not kwargs:
#             return list(self)
        
#         result=[]
#         for o in self:
#             #print(o)
#             for k,v in kwargs.items():
#                 if getattr(o,k,None)==v:
#                     result.append(o)
#                     break
#         return result
        
    
    
#     def insert(self,index,value):
#         "(Required by abstract base case)"
#         return self._epinputobjects.insert(index,value)
    
    
#     def summary(self):
#         """A count of each object type in the .epJSON file.
        
#         :rtype: dict

#         """
#         d={}
#         for o in self:
#             if not o.object_type in d:
#                 d[o.object_type]=1
#             else:
#                 d[o.object_type]+=1
#         return d
        
        
#         return {k:len(v.keys()) for k,v in self._dict.items()}
        
    
#     def validate(self):
#         """Validates the .epJSON file against the schema.
        
#         :raises Exception: If no schema is present to validate against.
#         :raises jsonschema.exceptions.ValidationError: If the EPInput object is not valid against the schema.
        
#         """
#         schema=self.schema
#         schema.validate_epjson(self._dict)
        
        
#     def write_json(self,fp):
#         """Writes an .epJSON file.
        
#         :param fp: The filename including the .epJSON extension.
#             This can be relative or absolute.
#         :type fp: str
        
#         """
#         with open(fp,'w') as f:
#             f.write(json.dumps(self._dict,indent=4))
            
            
#     def write_idf(self,fp):
#         """Writes an .idf file.
        
#         :param fp: The filename including the .idf extension.
#             This can be relative or absolute.
#         :type fp: str
        
#         """
#         idf=''
        
#         for o in self.objects.values():
            
#             print(o)
            
#             # object type
#             schema_object_type=self.schema.get_object_type(o.object_type)
#             idf+='%s, ' % o.object_type
            
#             # object name
#             legacy_idd_fields=schema_object_type.legacy_idd_fields
#             i=0
#             print(legacy_idd_fields)
#             if len(legacy_idd_fields)>0:
#                 if legacy_idd_fields[0]=='name':
#                     idf+='%s, ' % o.name
#                     i=1
                    
#             # legacy_idd_fields properties
#             if len(legacy_idd_fields)>0:
#                 for field in legacy_idd_fields[i:]:
#                     try:
#                         idf+='%s, ' % o.get_property_value(field)
#                     except KeyError: # if property is not present, output ', '
#                         idf+=', '
                    
#             # extension properties
#             try:
#                 extension=schema_object_type.legacy_idd_extension
#             except KeyError:
#                 extension=None
#             if extension:
#                 extensibles=schema_object_type.legacy_idd_extensibles
#                 for value in o.get_property_value(extension):
#                     for extensible in extensibles:
#                         idf+='%s, ' % value[extensible]
                
#             idf=idf[:-2]+';\n'
        
#         print(idf)
        
#         # write to file
#         with open(fp,'w') as f:
#             f.write(idf)
        
        
    
    

#     # def _get_object_type(self,object_name):
#     #     ""
#     #     for object_type in self.object_types:
#     #         object_type_dict=self._get_object_type_dict(object_type)
#     #         if object_name in object_type_dict:
#     #             return object_type
#     #     raise KeyError('The object name does not exist in the EPInput object')
    
    
#     # def _get_object_type_dict(self,object_type):
#     #     ""
#     #     return self._dict[object_type]
    
    
    
#     # def get_object(self,
#     #                name,
#     #                object_type=None):
#     #     """Returns an EPInputObject from the EPInput object.
        
#     #     .. note::
            
#     #        Specifying the 'object_type' will reduce the execution time of 
#     #        this method.    
        
#     #     :param name: The name of the EPInputObject.
#     #     :type name: str
#     #     :param object_type: The object type of the EPInputObject.
#     #         Optional. 
#     #     :type object_type: str
        
#     #     :raises KeyError: If an EPInputObject with 'name' 
#     #         (and with 'object_type_name' if specified)
#     #         does not exist in the EPInput object.
        
#     #     :rtype: EPInputObject
        
#     #     """
    
#     #     if object_type is None:
            
#     #         try:
#     #             object_type=self._get_object_type(name)
#     #         except KeyError:
#     #             raise KeyError('There is no EPInputObject with name "%s" in the EPInput object' % (name))
    
#     #     else:
            
#     #         object_type_dict=self._get_object_type_dict(object_type)
            
#     #         if not name in object_type_dict:
                
#     #             raise KeyError('There is no EPInputObject with name "%s" and object_type "%s"' % (name,object_type))
        
        
#     #     o=EPInputObject()
#     #     o.__dict__['_epinput']=self
#     #     o.__dict__['_object_type']=object_type
#     #     o.__dict__['_name']=name
#     #     return o    
    
    
#     # def get_object_names(self,object_type):
#     #     """Returns the object names for the specified object_type in the EPInput object.
        
#     #     :param object_type: The object type name.
#     #     :type object_type: str
        
#     #     :rtype: list
        
#     #     """
#     #     object_type_dict=self._get_object_type_dict(object_type)
#     #     return list(object_type_dict.keys())
    
    
#     # def get_objects(self,object_type):
#     #     """Returns all EPInputObject instances for the specified object_type in the EPInput object.
        
#     #     :param object_type: The object_type of the EPInputObjects.
#     #         :type object_type: str
        
#     #     :returns: A dictionary keyed by the object name
#     #     :rtype: dict (str,EPInputObject)
        
#     #     """
#     #     result={}
#     #     for object_name in self.get_object_names(object_type):
#     #         result[object_name]=self.get_object(object_name,object_type)
#     #     return result
    
    
#     # @property
#     # def object_names(self):
#     #     """The object names in the EPInput object.
        
#     #     :rtype: list (str)
        
#     #     """
#     #     result=[]
#     #     for object_type in self.object_types:
#     #         result+=self.get_object_names(object_type)
#     #     return result
        
    
#     # @property
#     # def objects(self):
#     #     """The EPInputObject objects in the EPInput object.
        
#     #     :returns: A dictionary keyed by the object name
#     #     :rtype: dict (str,EPInputObject)
        
#     #     """
#     #     result={}
#     #     for object_type in self.object_types:
#     #         result.update(self.get_objects(object_type))
#     #     return result
        

#     # @property
#     # def object_types(self):
#     #     """The object type names in the EPInput object.
        
#     #     :rtype: list
        
#     #     """
#     #     return list(self._dict.keys())
    
    
#     # def remove_object(self,
#     #                   name,
#     #                   object_type=None):
#     #     """Removes an EPInputObject from the EPInput object.
        
#     #     .. note::
            
#     #        Specifying the 'object_type' will reduce the execution time of 
#     #        this method. 
           
#     #     :param name: The name of the EPInputObject.
#     #     :type name: str
#     #     :param object_type: The object type of the EPInputObject.
#     #         Optional. 
#     #     :type object_type: str
        
#     #     :raises KeyError: If an EPInputObject with 'name' 
#     #         (and with 'object_type_name' if specified)
#     #         does not exist in the EPInput object.
        
#     #     """
    
#     #     if object_type is None:
            
#     #         try:
#     #             object_type=self._get_object_type(name)
#     #         except KeyError:
#     #             raise KeyError('There is no EPInputObject with name "%s" in the EPInput object' % (name))
    
#     #     # remove object
#     #     object_type_dict=self._get_object_type_dict(object_type)
#     #     del object_type_dict[name]
        
#     #     # if object was the last one of the object_type, then remove the 
#     #     #    object_type from the json dict.
#     #     if len(object_type_dict)==0:
#     #         del self._dict[object_type]
            
            
#     # def set_object(self,
#     #                name,
#     #                object_type,
#     #                validate=True,
#     #                **kwargs):
#     #     """Adds a new EPInputObject to the EPInput object.
        
#     #     :param name: The name of the EPInputObject.
#     #     :type name: str
#     #     :param object_type: The object type of the EPInputObject.
#     #     :type object_type: str
#     #     :param validate: If True then validation of the new EPInputObject is 
#     #         carried out using the schema.
#     #     :type validation: bool
#     #     :param kwargs: The key:value properties of the EPInputObject.
        
#     #     :returns: The newly created EPInputObject instance.
#     #     :rtype: EPInputObject
        
#     #     """
#     #     if validate:
            
#     #         # validate the object_type name
#     #         self.schema.validate_object_type_name(object_type)
        
#     #         # # validate the object properties
#     #         # obj_dict={name:kwargs}
#     #         # self.schema.get_object_type(object_type).validate_object(obj_dict)
        
        
#     #     object_type_dict=self._dict.setdefault(object_type,{})
#     #     object_type_dict[name]={}
        
#     #     o=self.get_object(name,object_type)
        
#     #     try:
#     #         for k,v in kwargs.items():
#     #             o.set_property_value(k,v,validate=validate)
#     #     except ValueError as err:
#     #         self.remove_object(name,object_type)
#     #         raise ValueError(err)
        
        
    
#     # @property
#     # def schema(self):
#     #     """The schema for the EnergyPlus input file.
        
#     #     :raises Exception: If the schema has not been defined for the EPInput object.
        
#     #     :rtype: EPSchema
        
#     #     """
#     #     if self._schema is None:
#     #         raise Exception('This operation requires an EPSchema to be defined. '
#     #                         'This is done by supplying the "schema" argument or setting the .schema attribute')
#     #     else:
#     #         return self._schema
    
    
#     # @schema.setter
#     # def schema(self,value):
#     #     """
#     #     :param value:
#     #     :type value: EPSchema

#     #     """
#     #     self._schema=value
        
    
    
        
        
        
        
        
        
        
        
        
        
    