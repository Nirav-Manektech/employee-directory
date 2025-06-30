from sqlalchemy.orm import Session
from app.database import SessionLocal,sync_engine as engine, Base
from app.models.user import User
from app.models.organization import Organization
from app.models.department import Department
from app.models.user_org import UserOrg
from app.models.configuration import Configuration
import random


def seed_data():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    session: Session = SessionLocal()

    # Create organizations
    org1 = Organization(id=1, org_name="Acme Corp")
    org2 = Organization(id=2, org_name="Globex Ltd")
    session.add_all([org1, org2])
    session.commit()

    # Create departments
    dept1 = Department(id=1, name="Engineering", org_id=1)
    dept2 = Department(id=2, name="HR", org_id=1)
    dept3 = Department(id=3, name="Sales", org_id=2)
    dept4 = Department(id=4, name="Marketing", org_id=2)
    session.add_all([dept1, dept2, dept3, dept4])
    session.commit()

    # Create users
    users = [
        User(id=1, username="Alice", email="alice@acme.com", phone="1234567890", position="Engineer", department_id=1),
        User(id=2, username="Bob", email="bob@acme.com", phone="2234567890", position="HR Manager", department_id=2),
        User(id=3, username="Charlie", email="charlie@globex.com", phone="3234567890", position="Sales Executive", department_id=3),
        User(id=4, username="David", email="david@globex.com", phone="4234567890", position="Marketing Lead", department_id=4),
        User(id=5, username="Eva", email="eva@acme.com", phone="5234567890", position="Engineer", department_id=1),
        User(id=6, username="Frank", email="frank@acme.com", phone="6234567890", position="Recruiter", department_id=2),
        User(id=7, username="Grace", email="grace@globex.com", phone="7234567890", position="Sales Rep", department_id=3),
        User(id=8, username="Henry", email="henry@globex.com", phone="8234567890", position="Marketer", department_id=4),
        User(id=9, username="Irene", email="irene@acme.com", phone="9234567890", position="Engineer", department_id=1),
        User(id=10, username="Jack", email="jack@globex.com", phone="1012345678", position="Sales Lead", department_id=3),
    ]
    session.add_all(users)
    session.commit()

    # Link users to organizations (via UserOrg)
    user_orgs = [
        UserOrg(user_id=1, org_id=1),
        UserOrg(user_id=2, org_id=1),
        UserOrg(user_id=3, org_id=2),
        UserOrg(user_id=4, org_id=2),
        UserOrg(user_id=5, org_id=1),
        UserOrg(user_id=6, org_id=1),
        UserOrg(user_id=7, org_id=2),
        UserOrg(user_id=8, org_id=2),
        UserOrg(user_id=9, org_id=1),
        UserOrg(user_id=10, org_id=2),
    ]
    session.add_all(user_orgs)

    # Configuration per organization
    config1 = Configuration(org_id=1, user_search_columns=["username", "email", "department", "position"])
    config2 = Configuration(org_id=2, user_search_columns=["username", "position", "phone"])
    session.add_all([config1, config2])

    session.commit()
    session.close()
    print("✅ Seeded test data.")


if __name__ == "__main__":
    seed_data()
