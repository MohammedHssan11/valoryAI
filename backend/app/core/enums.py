from enum import Enum


class PropertyType(str, Enum):
    APARTMENT = "Apartment"
    BUNGALOW = "Bungalow"
    BULK_RENT_UNIT = "Bulk Rent Unit"
    BULK_SALE_UNIT = "Bulk Sale Unit"
    CABIN = "Cabin"
    CAFETERIA = "Cafeteria"
    CHALET = "Chalet"
    CLINIC = "Clinic"
    CO_WORKING_SPACE = "Co-Working Space"
    DUPLEX = "Duplex"
    FACTORY = "Factory"
    FARM = "Farm"
    FULL_FLOOR = "Full Floor"
    HALF_FLOOR = "Half Floor"
    HOTEL_APARTMENT = "Hotel Apartment"
    IVILLA = "iVilla"
    LAND = "Land"
    MEDICAL_FACILITY = "Medical Facility"
    OFFICE_SPACE = "Office Space"
    PALACE = "Palace"
    PENTHOUSE = "Penthouse"
    RESTAURANT = "Restaurant"
    RETAIL = "Retail"
    ROOF = "Roof"
    SHOP = "Shop"
    SHOW_ROOM = "Show Room"
    STAFF_ACCOMMODATION = "Staff Accommodation"
    TOWNHOUSE = "Townhouse"
    TWIN_HOUSE = "Twin House"
    VILLA = "Villa"
    WAREHOUSE = "Warehouse"
    WHOLE_BUILDING = "Whole Building"


class ListingCategory(str, Enum):
    RENT = "rent"
    BUY = "buy"
    COMMERCIAL_RENT = "commercial_rent"
    COMMERCIAL_BUY = "commercial_buy"
    NEW_PROJECTS = "new_projects"


class PropertyCategory(str, Enum):
    RESIDENTIAL_RENT = "residential_rent"
    RESIDENTIAL_SALE = "residential_sale"
    VILLA_SALE = "villa_sale"
    OFFICE_RENT = "office_rent"
    RETAIL_RENT = "retail_rent"
    COMMERCIAL_RENT = "commercial_rent"
    LAND_SALE = "land_sale"


class RentalPeriod(str, Enum):
    MONTHLY = "monthly"
    SALE = "sale"


class ConfidenceLevel(str, Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class PriceFlag(str, Enum):
    INSUFFICIENT_DATA = "INSUFFICIENT_DATA"
    NO_TARGET = "NO_TARGET"
    TOO_HIGH = "TOO_HIGH"
    TOO_LOW = "TOO_LOW"
    OK = "OK"
