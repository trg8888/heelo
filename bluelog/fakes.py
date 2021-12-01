import random

from faker import Faker

from bluelog.extensions import db
from bluelog.models import Major,Subcategory,Picture,About,PrivacySecurity,PaymentMethods,ReturnPolicy,Faq,Subcategory_,\
basicsettings


fake = Faker()



def fake_major(count=10):
    for i in range(count):
        major = Major(
            name = fake.name() + str(random.randint(1,99)),
            exegesis = fake.text(),
            least = random.randint(1,10),
            maximum = random.randint(11,29),
            timestamp = fake.date_time(),
            frequency = random.randint(0,1)
        )
        db.session.add(major)
        db.session.commit()

def fake_subcategory(count=100):
    for i in range(count):
        subcategory = Subcategory(
            name = fake.name(),
            exegesis = fake.text(),
            timestamp=fake.date_time(),
            major_id = random.randint(1,Major.query.count())
        )
        db.session.add(subcategory)
    db.session.commit()

def fake_picture_management(count=1000):
    for i in range(count):
        picture = Picture(
            name = fake.name(),
            description = fake.text(),
            attribute = 's,m,x,l',
            color = 'red,yellow',
            picture = fake.text(),
            price = fake.random_number(),
            timestamp = fake.date_time(),
            subcategorys_id = random.randint(1,Subcategory.query.count())
        )
        db.session.add(picture)
    db.session.commit()
def fake_about(count=100):
    for i in range(count):
        about = About(
            name = fake.paragraph()
        )
        privacySecurity = PrivacySecurity(
            name = fake.paragraph()
        )
        paymentMethods = PaymentMethods(
            name = fake.paragraph()
        )
        returnPolicy = ReturnPolicy(
            name = fake.paragraph()
        )
        faq = Faq(
            name = fake.paragraph()
        )
        subcategory_ = Subcategory_(
            name = fake.paragraph()
        )
        basicsetting =basicsettings(
            title = fake.name(),
            Keyword = fake.paragraph(),
            description = fake.paragraph()
        )
        db.session.add(about)
        db.session.add(privacySecurity)
        db.session.add(paymentMethods)
        db.session.add(returnPolicy)
        db.session.add(faq)
        db.session.add(subcategory_)
        db.session.add(basicsetting)
    db.session.commit()
