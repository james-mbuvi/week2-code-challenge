from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData,ForeignKey
from sqlalchemy.orm import validates,relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Sweet(db.Model, SerializerMixin):
    _tablename_ = 'sweets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)


    # Add relationship
    vendors = relationship('VendorSweet', back_populates='sweet')
    # Add serialization
    vendors_rel = association_proxy('vendors', 'vendor')

    
    def _repr_(self):
        return f'<Sweet {self.id}>'


class Vendor(db.Model, SerializerMixin):
    _tablename_ = 'vendors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    # Add relationship
    sweets = relationship('VendorSweet', back_populates='vendor')
    # Add serialization
    sweets_rel = association_proxy('sweets', 'sweet')

    
    def _repr_(self):
        return f'<Vendor {self.id}>'


class VendorSweet(db.Model, SerializerMixin):
    _tablename_ = 'vendor_sweets'

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)

    # Add relationships
    sweet_id = db.Column(db.Integer, ForeignKey('sweets.id', ondelete='CASCADE'), nullable=False)
    sweet = relationship('Sweet', back_populates='vendors')

    # Add serialization
    vendor_id = db.Column(db.Integer, ForeignKey('vendors.id', ondelete='CASCADE'), nullable=False)
    vendor = relationship('Vendor', back_populates='sweets')
    
    # Add validation
    @validates('price')
    def validate_price(self, key, price):
        if price is None:
            raise ValueError("Price cannot be None")
        if price < 0:
            raise ValueError("Price cannot be negative")
        return price

    def _repr_(self):
        return f'<VendorSweet {self.id}>'