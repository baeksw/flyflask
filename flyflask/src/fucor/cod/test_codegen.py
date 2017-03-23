# -*- coding: utf-8 -*-
from fucor.application import *
from fucor.cod.models import *

from xml.etree.ElementTree import Element, SubElement, Comment, tostring
import xml.dom.minidom as md

from codecs import open
import json
import codecs

def addElementCoder(obj, root):
    tag = SubElement(root,'coder')
    SubElement(tag, 'desc').text = obj.descr
    SubElement(tag, 'name').text = obj.author
    SubElement(tag, 'since').text = obj.since
    SubElement(tag, 'version').text = obj.version


def searchCmTableByName(table_name):
    try:
        oTable = db.session.query(CM_TABLE) \
                .filter(CM_TABLE.name == table_name) \
                .one()
        return oTable 
    except Exception as e:
        return None
        

def addElementClass(obj, root):
    tag = SubElement(root,'class')
    tag.attrib['code'] = obj.cls_name
    tag.attrib['base_package'] = obj.package
    methods = obj.cm_method.all()
    if methods:
        for x in methods:
            m = SubElement(tag, 'method')
            m.attrib['name'] = x.name
            descr = SubElement(m, 'descr')
            SubElement(descr, 'pre').text =  x.descr 
            SubElement(descr, 'param').text = 'PARAM' 
            SubElement(descr, 'return').text = x.returning 
            SubElement(descr, 'exception').text = x.exception
            oTable = searchCmTableByName(x.table_name) 
            if oTable:
                cols = oTable.cm_column.all()
                if cols and len(cols) > 0:
                    tbl = SubElement(m, 'table')
                    tbl.attrib['name'] = oTable.name
                    for c in cols:
                        col = SubElement(tbl, 'column')
                        col.attrib['name'] = c.name
                        col.attrib['alias'] = c.name.lower()
                        col.attrib['comment'] = c.descr
                        pass
                pass
        
    print(methods)

def asXml(obj):
    builder = Element('builder')
    output = SubElement(builder, 'output')
    SubElement(output, "base_dir").text = "D:/output/"
    SubElement(output, "sqlmap_dir").text = "D:/output/"
    addElementCoder(obj, builder)
    addElementClass(obj, builder)
    return md.parseString(tostring(builder)).toprettyxml(indent='    ')

def string2file(body):
    import io
    return io.StringIO(body)


from koma.io import *
from koma.jinja import *

def build_source(xmlfile):
    model = read_xml_model(xmlfile)
    o = Outputter(model)
    print("\t create controller - "+o.get_controller_dir())
    print("\t create service - "+o.get_service_dir())
    print("\t - "+o.get_service_impl_dir())
    print("\t - "+o.get_sqlmap_dir())

    o.out_controller()  
    o.out_service()  
    o.out_service_impl()  
    o.out_dao()  
    o.out_sqlmap()   


if __name__ == '__main__':
    coder = db.session.query(CM_CODER).filter(CM_CODER.package == 'ktr.cot').one()
    body = asXml(coder)
    build_source(string2file(body))
    

'''

 table = Element('table')

        table.attrib['name'] = model['name']
#         columns = SubElement(table, 'columns')
        for x in model['columns']:
            name = x['name']
            alias = x['name'] if x['name'] else None 
            comment = cmts.get(x['name']) if x['name'] in cmts else x['name']
            attrib = { 'name' : name, 'alias' : alias , 'comment' : comment } if alias and self.alias_yn else { 'name' : name, 'comment' : comment } 
#             col = SubElement(columns, 'column', attrib)
            col = SubElement(table, 'column', attrib)




class TableMeta(EngineFactory):

    def __init__(self, engineType):
        super().__init__(engineType)
        self.engine = self.asEngine()
        self.session = SessionFactory(self.engine).asSession()
        self.s = self.session()
        self.meta = MetaData()
        self.outXml = []
        self.filename = 'table_meta.txt'
        self.console_on = False
        self.alias_yn = True
    
    def disable_alias(self):
        self.alias_yn = False

    def enable_alias(self):
        self.alias_yn = True

    def output(self,filename):    
        self.filename = filename
        return self
    
    def console(self,mode=True):
        self.console_on = mode
        return self

    def get_table_meta(self, table_name):
        ret = {}
        table = Table(table_name, self.meta, autoload=True, autoload_with=self.engine)
        ret['name'] = table.name
        ret['columns'] = []
        for i , x in enumerate(table.columns):
            d = {}
            d['order'] = i
            d['name'] = str(x.key).upper()
            d['type'] = str(x.type)
            d['primary_key'] = str(x.primary_key)
            d['nullable'] = str(x.nullable)
            ret['columns'].append(d)
        return ret

    def __enter__(self):
        return self

    def __exit__(self,*args):
        if self.console_on:
            print("\n".join(self.outXml))
        else:
            f = open(self.filename,'w')
            f.write("\n".join(self.outXml))
            f.close()
        try:
            if self.engine:
                self.engine.dispose()
        except:
            pass
    
    def buildXml(self,table_name):
        xml = self.asXml(table_name)
        self.outXml.append(xml)

    def asXml(self, table_name):
        cmts = query_col_comments(self.s, table_name)
        model = self.get_table_meta(table_name)
        table = Element('table')

        table.attrib['name'] = model['name']
#         columns = SubElement(table, 'columns')
        for x in model['columns']:
            name = x['name']
            alias = x['name'] if x['name'] else None 
            comment = cmts.get(x['name']) if x['name'] in cmts else x['name']
            attrib = { 'name' : name, 'alias' : alias , 'comment' : comment } if alias and self.alias_yn else { 'name' : name, 'comment' : comment } 
#             col = SubElement(columns, 'column', attrib)
            col = SubElement(table, 'column', attrib)

        return md.parseString(tostring(table)).toprettyxml(indent='    ')
    
'''


'''
class CodeBuilder:
    def __init__(self,model):
        self.model = model

    def controller(self):
        tpl = get_template('controller.tpl')
        return tpl.render(**self.model)

    def service(self):
        tpl = get_template('service.tpl')
        return tpl.render(**self.model)

    def service_impl(self):
        tpl = get_template('service_impl.tpl')
        return tpl.render(**self.model)
    
    def dao(self):
        tpl = get_template('dao.tpl')
        return tpl.render(**self.model)

    def sqlmap(self):
        tpl = get_template('sqlmap.tpl')
        return tpl.render(**self.model)
    
    def get_controller_dir(self):
        return self.model.get('output').get('base_dir') + '/web'

    def get_service_dir(self):
        return self.model.get('output').get('base_dir') + '/service'

    def get_service_impl_dir(self):
        return self.model.get('output').get('base_dir') + '/service/impl'

    def get_sqlmap_dir(self):
        return self.model.get('output').get('sqlmap_dir') 
    
    

class Outputter(CodeBuilder):
    def __init__(self,model):
        super().__init__(model)
        
    def out_controller(self):
        dir = self.get_controller_dir()
        source = self.controller()
        fname = self.model.get('class').get('code') + 'Controller.java'
        with codecs.open(dir+'/'+fname,'w','utf8') as f:
            f.write(source)
        print(fname + '- done.')

    def out_service(self):
        dir = self.get_service_dir()
        source = self.service()
        fname = self.model.get('class').get('code') + 'Service.java'
        with codecs.open(dir+'/'+fname,'w','utf8') as f:
            f.write(source)
        print(fname + '- done.')
        
    def out_service_impl(self):
        dir = self.get_service_impl_dir()
        source = self.service_impl()
        fname = self.model.get('class').get('code') + 'ServiceImpl.java'
        with codecs.open(dir+'/'+fname,'w','utf8') as f:
            f.write(source)
        print(fname + '- done.')

    def out_dao(self):
        dir = self.get_service_impl_dir()
        source = self.dao()
        fname = self.model.get('class').get('code') + 'Dao.java'
        with codecs.open(dir+'/'+fname,'w','utf8') as f:
            f.write(source)
        print(fname + '- done.')
        
    def out_sqlmap(self):
        dir = self.get_sqlmap_dir()
        source = self.sqlmap()
        fname = self.model.get('class').get('code') + '_Oracle.xml'
        with codecs.open(dir+'/'+fname,'w','utf8') as f:
            f.write(source)
        print(fname + '- done.')        
        
        
'''