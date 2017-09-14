import pymysql
class MYSQL:
    connect_num=0
    def __init__(self,username,password,url,basename):#input information for mysql login
        self.username=username
        self.password=password
        self.url=url
        self.database=basename
        self.max_connect_num=20


    def get_curser(self):#to get a cursor
        self.connect=pymysql.connect(self.url,self.username,self.password,self.database,charset='utf8')
        MYSQL.connect_num=MYSQL.connect_num+1
        return self.connect.cursor()

    def query(self,mysql):#use mysql sentense to search
        cursor=self.get_curser()
        cursor.execute(mysql) #execute mysql
        result_set=cursor.fetchall() #get all results
        count=cursor.rowcount
        cursor.close()
        self.connect.close()
        return result_set,count

    def data_update(self,mysql_list):#excute a set of mysql sentense
        cursor=self.get_curser()
        try:
            for mysql in mysql_list:
                cursor.execute(mysql)
            self.connect.commit()
        except Exception:
            self.connect.rollback()
        cursor.close()
        self.connect.close()

class datadeal:   #a class use for dealing with Object
    def __init__(self):
        self.connect=MYSQL('root','tanyao','localhost','worn')
        self.event_list=list()

    def insert(self,Object):
        dic=Object.__dict__
        sql='insert into '+Object.__str__()
        column=''
        values=''
        for (key,value) in dic.items():
            if value is not None:
                column=column+','+key
                values=values+",'"+value+"'"
        c_size=int(len(column))
        v_size=int(len(values))
        column=column[1:c_size]
        values=values[1:v_size]
        sql=sql+"("+column+") values"+"("+values+");"
        print(sql)
        self.event_list.append(sql)


    def search(self,Object):
        sql="select * from "+Object.__str__()+" where "
        condition=''
        dic=Object.__dict__
        for (key,value) in Object.__dict__.items():
            if value is not None:
                condition=key+"='"+value+"' and "
        condition=condition[0:len(condition)-4]
        sql=sql+condition
        print(sql)
        result,count=self.connect.query(sql)
        l=list()
        for r in result:
            s=BaseObject()
            s.set_dict(dic,r)
            l.append(s)
        return l

    def delete_data(self,Object):
        sql = "delete from " + Object.__str__() + " where "
        condition = ''
        dic = Object.__dict__
        for (key, value) in Object.__dict__.items():
            if value is not None:
                condition = key + "='" + value + "' and "
        condition = condition[0:len(condition) - 4]
        sql = sql + condition
        print(sql)
        self.event_list.append(sql)

    def excute_event(self):
        self.connect.data_update(mysql_list=self.event_list)



class Node:
    def __init__(self,col_name,data_kind='varchar(32)'):
        self.col_name=col_name
        self.data_kind=data_kind
        self.notnull=''

    def set_varchar(self,length):
        self.data_kind='varchar('+length+')'

    def get_NodeName(self):
        return  self.col_name

    def get_NodeDataKind(self):
        return  self.data_kind

    def get_subsql(self):
        self.sql=self.col_name+" "+self.data_kind+self.notnull+self.primarykey+self.auto_increment
        return self.sql

    def set_int(self):
        self.col_name='int'

    def set_not_null(self):
        self.notnull=' not null'

    def set_autoincrement(self):
        if self.data_kind in ['int','interger']:
            self.auto_increment=' auto_increment'


    def set_primarykey(self):
        self.primarykey=' primary key'

class Node_list:
    def __init__(self,table_name=None):
        self.table_name=table_name
        self.col_dic=dict()

    def set_table_name(self,tablename):
        self.table_name=tablename

    def add_node(self,node):
        self.col_dic.setdefault(node.data_kind,node)

    def get_node_type(self,col_name):
        return self.col_dic[col_name].get_NodeDataKind()

    def get_create_mysql(self):
        sql='create table  IF NOT EXISTS '+self.table_name+'('
        t_sql=''
        for node in self.col_list:
            t_sql=node.get_subsql()+' ,'
        t_sql=t_sql[0:len(t_sql)-1]
        sql=sql+t_sql+')'

    def sql_check(self):
        pass



class BaseObject:
    node_dict=Node_list()
    @staticmethod
    def get_create_sql():
        return BaseObject.node_dict.get_create_mysql()


    def set_dict(self,dict,values):
        t_dict=dict.copy()
        i=0
        for (key,value) in dict.items():
            t_dict[key]=values[i]
            i=i+1
        self.__dict__=t_dict



class User(BaseObject):
    super.node_dict=Node_list()
    node0=Node('id')
    node0.set_int()
    node0.set_autoincrement()
    node0.set_primarykey()
    super.node_dict.add_node(node0)
    node1=Node('username')
    super.node_dict.add_node(node1)
    node2=Node('password')
    super.node_dict.add_node(node2)
    node3=Node('role')
    super.node_dict.add_node(node3)

    def __init__(self,username=None,password=None,role=None,id=None):
        self.id=id
        self.username=username
        self.password=password
        self.role=role
        self.__dict__={'username':username,'password':password,'role':role,'id':id}

    def __str__(self):
        return 'user'


