# coding-utf-8
import shutil
import peewee
from peewee import *
from datetime import date

WORKER_PHOTO_PATH = 'C:\\Users\\rex38\\Desktop\\katorgaDB'
db = SqliteDatabase(':memory:')
GENDER = (
  (False , 'women' ),
  (True , 'man'),
)

def add_worker_photo(worker, file_path):
    shutil.copy2('C:\Users\\rex38\\Desktop\\chart.svg',WORKER_PHOTO_PATH+"\\{}.svg".format(worker.id))

class BaseModel(Model):
    class Meta:
        database = db

class City(BaseModel):
    id = IntegerField(primary_key = True)
    name = CharField()


    @staticmethod
    def add_new(name):
        City.create(name=name)
    def __repr__(self):
        return "{}".format(self.name)

class Post(BaseModel):
    id  = IntegerField(primary_key = True)
    type =  CharField()

    @staticmethod
    def add_new(post):
        Post.create(type=post)
    def __str__(self):
        return "{}".format(self.type)

class Address(BaseModel):
    id  = IntegerField(primary_key = True)
    city = ForeignKeyField(City, related_name ="alladdress")
    type = CharField()
    street = CharField()
    home = CharField()
    flat = IntegerField(null= True)


    @staticmethod
    def add_new(city,type,street,home,flat):
        Address.create(
            city=city,
            type = type,
            street=street,
            home=home,
            flat=flat
            )
    @staticmethod
    def self_update(addres,city,type,street,home,flat):
        addres.city = city
        addres.street = street
        addres.type = type
        addres.home = home
        addres.flat = flat
        addres.save()
    def __repr__(self):
        return "street: '{}' home: '{}' flat: '{}' ".format(self.street,self.home,self.flat)

class Department(BaseModel):
    id  = IntegerField(primary_key = True)
    address = ForeignKeyField( Address, related_name = "departments", unique = True)
    telephone = CharField()
    name = CharField()


    @staticmethod
    def add_new(name,telephone,address):
        Department.create(name=name,telephone=telephone,address=address)
    @staticmethod
    def self_update(department,name,telephone,address):
        department.name = name
        department.telephone =telephone
        department.address = address
        department.save()
    def __repr__(self):
        return "Department: '{}'".format(self.name)

class Worker(BaseModel):
    id = IntegerField(primary_key = True)
    name = CharField()
    surname = CharField()
    lastname = CharField()
    post = ForeignKeyField(Post,related_name = "workers")
    gender = BooleanField(choices = GENDER)
    telephone =  CharField(null = True)
    email =  CharField(null = True)
    photo = CharField(null = True)
    birthday = DateField()
    hiredate = DateField()
    salary = FloatField()
    legalprofit = FloatField()
    department  = ForeignKeyField(Department,related_name = "workers", unique = True)


    @staticmethod
    def add_new(name , surname , lastname ,post ,gender, birthday,hiredate,salary,legalprofit,department):
        Worker.create(
            name=name ,
            surname = surname ,
            lastname = lastname,
            post =post,
            gender = gender,
            birthday =  birthday,
            hiredate=hiredate,
            salary = salary,
            legalprofit = legalprofit,
            department = department
        )
    @staticmethod
    def self_update(this,name , surname , lastname ,post ,gender, birthday,hiredate,salary,legalprofit,department):
        this.name = name
        this.surname = surname
        this.lastname = lastname
        this.post = post
        this.gender =  gender
        this.birthday = birthday
        this.hiredate = hiredate
        this.salary = salary
        this.legalprofit = legalprofit
        this.department = department
        this.save()
    def __repr__(self):
        return "name : '{} {} {}' post : '{}' gender: {}".format(self.name,self.surname,self.lastname,self.post,self.gender)

class Workers_has_Address(BaseModel):
    worker_id = ForeignKeyField(Worker)
    addres_id = ForeignKeyField(Address)

class Vacation(BaseModel):
    worker = ForeignKeyField(Worker , related_name = "vacation")
    type  = CharField()
    start = DateField()
    finish = DateField()


    @staticmethod
    def add_new(worker,type,start,finish):
        Vacation.create(worker=worker,type=type,start=start,finish=finish)
    def __repr__(self):
        return "Vacation between {} and {}".format(self.start,self.finish)

def Workers_in_vacation():
    return Worker.select().join(Vacation).where(Vacation.start<=date.today(), Vacation.finish>=date.today())
def Working_woman():
    return Worker.select().where(Worker.gender == False)
def Working_man():
    return Worker.select().where(Worker.gender == True)

def overwrite_table():
    if Worker.table_exists():
        Worker.drop_table()
    Worker.create_table()
    if City.table_exists():
        City.drop_table()
    City.create_table()
    if Vacation.table_exists():
        Vacation.drop_table()
    Vacation.create_table()
    if Address.table_exists():
        Address.drop_table()
    Address.create_table()
    if Department.table_exists():
        Department.drop_table()
    Department.create_table()
    if Post.table_exists():
        Post.drop_table()
    Post.create_table()
    if Workers_has_Address.table_exists():
        Workers_has_Address.drop_table()
    Workers_has_Address.create_table()
def init_preview_db():
    overwrite_table()
    City.add_new("Odessa")
    odes = City.get()
    Post.add_new("Programmer")
    post = Post.get()
    Address.add_new(odes,"urta","ilpha i petrova","21/2",143)
    Address.add_new(odes,"barak","Slavianskaia","19",13)
    ad = Address.get()
    Department.add_new("kill Bill","3809512312",ad)
    dep = Department.get()
    Worker.add_new("qwe","hohland","pidrosovich",post,"man",date(1999,1,2),date(1999,1,2),100,200,dep)
    pers =  Worker.get()
    Vacation.add_new(pers,"mama ama criminal",date(2000,1,1),date(2202,1,1))
    Workers_has_Address.create(worker_id=1,addres_id=1)

if __name__ == "__main__":
    init_preview_db()
    for addr in Address.select(Address, Worker).join(Workers_has_Address).join(Worker).where(Worker.id == 1):
        print addr
