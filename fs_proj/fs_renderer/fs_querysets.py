import local_settings
import sqlsoup
import datetime
from bunch import Bunch

db = sqlsoup.SQLSoup(local_settings.DATABASE)


class QuerySet(object):
    def __init__(self, query_dict={}, table_name='', sql='',
                 id_variable_value='', related_table='', related_field=''):
        self.query_dict = query_dict
        self.table_name = table_name
        self.sql = sql
        self.related_field = related_field
        self.related_table_name = related_table
        self.db = db
        self.data = None
        self.id_variable_value = id_variable_value
        if self.table_name:
            self.table = self.db.entity(self.table_name)
        else:
            self.table = None
        if self.related_table_name:
            self.related_table = self.db.entity(self.related_table_name)
        else:
            self.related_table = None
        self.objects = Bunch({'all': self.all, 'get': self.get,
                              'create': self.create,
                              'update': self.update, 'delete': self.delete,
                              'sql_execute': self.sql_execute, 'filter': self.filter,
                              'related_set': self.related_set})

    def all(self):
        records = self.table.all()
        result = []
        for record in records:
            rec = record.__dict__
            rec.pop('_sa_instance_state')
            result.append(rec)
        return result

    def get(self, id_variable_value=None):
        if id_variable_value is None:
            id_variable_value = self.id_variable_value
        data = self.table.get(int(id_variable_value)).__dict__
        data['id'] = id_variable_value
        self.id_variable_value = id_variable_value
        self.tidy(data)
        return data

    def create(self, query_dict):        
        data = self.table.insert(**query_dict).__dict__
        data.pop('_sa_instance_state')
        db.commit()
        self.id_variable_value = data[u'id']
        self.data = data
        return data
    
    def create_related(self, query_dict):
        data = self.related_table.insert(**query_dict).__dict__
        db.commit()
        data.pop('_sa_instance_state')
        self.data = data
        return data

    def update(self, query_dict, id_variable_value):
        relateds = []
        for key in query_dict.keys():
            if isinstance(query_dict[key], list):
                relateds = query_dict.pop(key)
        for related in relateds:
            related[self.related_field] = int(id_variable_value)
            if related.has_key('id'):
                self.update_related(related, related['id'])
            else:
                self.create_related(related)
        self.id_variable_value = int(id_variable_value)
        data = self.table.filter_by(id=int(id_variable_value)).update(query_dict)
        data = query_dict
        db.commit()
        self.data = data
        return
    
    def update_related(self, query_dict, id_variable_value):
        data = self.related_table.filter_by(id=int(id_variable_value)).update(query_dict)
        db.commit()
        return 

    def delete(self, id_variable_value):
        instance = self.table.get(int(id_variable_value))
        self.id_variable_value = id_variable_value
        db.delete(instance)
        db.commit()
        return

    def sql_execute(self, sql_string):
        rp = self.db.execute(sql_string)
        rows = rp.fetchall()
        result = []
        for row in rows:
            rec = self.row2dict(row)
            result.append(rec)
        return result

    def tidy(self, data):
        data.pop('_sa_instance_state')
        for k in data.keys():
            if isinstance(data[k], datetime.date):
                data[k] = str(data[k])
                
    def filter(self, field, like, order=None):
        result = self.sql_execute("""select * from %s where %s like '%%%s%%';""" % (self.table_name, field, like))
        return result
    
    def related_set(self, related_table=None, field='id'):
        if related_table == None:
            related_table = self.related_table_name
        if self.related_field:
            field = self.related_field     
        result = self.sql_execute("""select * from %s where %s = %s;""" % (related_table, field, int(self.id_variable_value)))
        return result

    def row2dict(self, row):
        d = {}
        for key, value in row.items():
            d[key] = value
        return d

