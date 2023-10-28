class FACINGS:
    N = "N"
    S = "S"
    E = "E"
    W = "W"
    NE = "NE"
    NW = "NW"
    SE = "SE"
    SW = "SW"
    facing_choices = (
        ("N", "North"),
        ("S", "South"),
        ("E", "East"),
        ("W", "West"),
        ("NE", "North East"),
        ("NW", "North West"),
        ("SE", "South East"),
        ("SW", "South West"),
    )


class PropertyTypes:
    GroupAppart = "Group Appartment"
    GroupVilla = "Group Villa"
    GroupPlot = "Group Plot"
    Flat = "Flat"
    Building = "Building"
    Villa = "Villa"
    OpenPlot = "Open Plot"
    PG = "PG"
    Rent = "Rent"
    Commercial = "Commercial"

    property_type_choices = (
        (GroupAppart, "Group Appartment"),
        (GroupVilla, "Group Villa"),
        (GroupPlot, "Group Plot"),
        (Flat, "Flat"),
        (Building, "Building"),
        (Villa, "Villa"),
        (OpenPlot, "Open Plot"),
        (PG, "PG"),
        (Rent, "Rent"),
        (Commercial, "Commercial"),
    )


class FursnihingTypes:
    NonFurnished = "Non Furnished"
    SemiFurnished = "Semi Furnished"
    FullyFurnished = "Fully Furnished"

    furnished_choices = (
        (NonFurnished, "Non Furnished"),
        (SemiFurnished, "Semi Furnished"),
        (FullyFurnished, "Fully Furnished"),
    )
