from sqlalchemy import (
    Column, String, Boolean, DateTime, Date, Time, Text, 
    Enum, ForeignKey, DECIMAL, Integer, JSON, func
)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.dialects.mysql import CHAR
import uuid

Base = declarative_base()

def generate_uuid():
    return str(uuid.uuid4())


class User(Base):
    __tablename__ = "users"

    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(150), nullable=False)
    role = Column(Enum("admin", "doctor", "staff", "receptionist"), default="staff")
    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    user_id = Column(CHAR(36), ForeignKey("users.id"), nullable=True)
    name = Column(String(150), nullable=False)
    specialization = Column(String(150))
    phone = Column(String(20))
    email = Column(String(255))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)


class Patient(Base):
    __tablename__ = "patients"

    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=True)
    phone = Column(String(20), unique=True, index=True, nullable=False)
    email = Column(String(255))
    age = Column(Integer, nullable=True)
    date_of_birth = Column(Date, nullable=True)
    gender = Column(Enum("male", "female", "other", "unknown"), default="unknown")
    complaints = Column(Text)
    allergies = Column(Text)
    medical_notes = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)

    appointments = relationship("Appointment", back_populates="patient")
    prescriptions = relationship("Prescription", back_populates="patient")
    call_logs = relationship("CallLog", back_populates="patient")


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    patient_id = Column(CHAR(36), ForeignKey("patients.id"), nullable=False)
    doctor_id = Column(CHAR(36), ForeignKey("doctors.id"), nullable=True)
    appointment_date = Column(Date, nullable=False, index=True)
    appointment_time = Column(Time, nullable=True)
    status = Column(Enum("scheduled", "confirmed", "completed", "cancelled", "no_show"), default="scheduled")
    reason = Column(Text)
    notes = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)

    patient = relationship("Patient", back_populates="appointments")


class Prescription(Base):
    __tablename__ = "prescriptions"

    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    patient_id = Column(CHAR(36), ForeignKey("patients.id"), nullable=False)
    doctor_id = Column(CHAR(36), ForeignKey("doctors.id"), nullable=True)
    prescribed_date = Column(Date, nullable=False)
    medicines = Column(JSON)          # list of medicines
    notes = Column(Text)
    status = Column(Enum("active", "completed", "cancelled"), default="active")
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)

    patient = relationship("Patient", back_populates="prescriptions")


class CallLog(Base):
    __tablename__ = "call_logs"

    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    patient_id = Column(CHAR(36), ForeignKey("patients.id"), nullable=True)
    phone_number = Column(String(20), nullable=False, index=True)
    call_direction = Column(Enum("incoming", "outgoing"), nullable=False)
    call_status = Column(Enum("answered", "missed", "voicemail", "failed"), nullable=False)
    duration_seconds = Column(Integer, default=0)
    transcript = Column(Text)
    ai_summary = Column(Text)
    started_at = Column(DateTime, nullable=False, index=True)
    ended_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=func.now())

    patient = relationship("Patient", back_populates="call_logs")


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    user_id = Column(CHAR(36), nullable=True)
    action = Column(String(100), nullable=False)
    table_name = Column(String(100))
    record_id = Column(CHAR(36))
    old_values = Column(JSON)
    new_values = Column(JSON)
    ip_address = Column(String(45))
    created_at = Column(DateTime, default=func.now(), index=True)
