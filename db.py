from peewee import *

db = SqliteDatabase('vetbot.db')


class BaseModel(Model):
    class Meta:
        database = db


class Client_info(BaseModel):
    client_id = IntegerField()
    ClientFullName = CharField()
    ClientPhoneNumber = CharField()
    ClientEmail = CharField()
    ClientTgUsername = CharField()


class Doctor_info(BaseModel):
    doctor_id = IntegerField(primary_key=True)
    DoctorFullName = CharField()
    DoctorInfo = CharField()
    Photo = CharField()


class Service_type(BaseModel):
    ServiceType = CharField()


class Service_info(BaseModel):
    ServiceType_fk = ForeignKeyField(Service_type, backref='ServiceTypeName')
    ServiceName = CharField()
    ServicePrice = IntegerField()

class Doctor_service(BaseModel):
    service_fk = ForeignKeyField(Service_info, backref='serviceid')
    doctor_fk = ForeignKeyField(Doctor_info, backref='doctorid')



class Sales_info(BaseModel):
    SaleName = CharField()
    SaleDescription = CharField()
    SaleStartDate = DateTimeField()
    SaleEndDate = DateTimeField()

class Coupon(BaseModel):
    CouponName = CharField()
    CouponDescription = CharField()
    CouponOwner_fk = ForeignKeyField(Client_info, backref='CouponOwner')
    CouponStartDate = DateTimeField()
    CouponEndDate = DateTimeField()


class Statistic(BaseModel):
    OrderNumber = BigAutoField(primary_key=True)
    client_fk = ForeignKeyField(Client_info, backref='clientid')
    service_fk = ForeignKeyField(Service_info, backref='serviceid')
    doctor_fk = ForeignKeyField(Doctor_info, backref='doctorid')
    DateOfApplication = DateTimeField()
    Coupon = IntegerField()
    Status = CharField()
    DateOfReceipt = DateTimeField()   #на когда заказан
    ProblemDescription = CharField()


if __name__ == '__main__':
    with db:
        db.create_tables([Statistic, Client_info, Doctor_info, Doctor_service,
                          Service_info, Service_type, Sales_info, Coupon])
    #odc = Doctor_info.create(DoctorFullName='док10', DoctorInfo='0', Photo='0')
    # odc.DoctorInfo = 'byaj8'
    # odc.save()
    # odc.Photo = 'ajnj8'
    # odc.save()
    # stm = Service_type.select()
    # stms = [stm.id for stm in stm]
    # for i in stms:
    #     Service_info.create(ServiceType_fk=i, ServiceName=f'имя услуги{i}', ServicePrice=i*10)
    # Service_info.create(ServiceType_fk=2, ServiceName=f'имя услуги5', ServicePrice=50)
    # Doctor_info.delete_instance()
    # t = Doctor_info.select().where(Doctor_info.doctor_id == 4).get()
    # t.DoctorFullName = 'сеня'
    # t.save()
