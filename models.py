"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.

You'll edit this file in Task 1.
"""
from helpers import cd_to_datetime, datetime_to_str
from math import isnan


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional), diameter
    in kilometers (optional - sometimes unknown), and whether it's marked as
    potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """

    def __init__(self, designation,  name, diameter, hazardous):
        """Create a new `NearEarthObject`.

        :param designation: The primary designation of this NEO (unique identifier)
        :type designation: str
        :param name: The International Astronomical Union (IAU) name of this NEO
        :type name: str
        :param diameter: The diameter of this NEO in kilometers
        :type diameter: str
        :param hazardous: whether NASA has marked the NEO as a "Potentially Hazardous Asteroid"
        :type hazardous: str
        """
        self.designation = designation
        self.name = name if name != '' else None
        self.diameter = float(diameter) if diameter != '' else float('nan')
        self.hazardous = hazardous == 'Y'

        # Create an empty initial collection of linked approaches.
        self.approaches = []

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        fullname = self.designation if not self.name else f"{self.designation} ({self.name})"
        return fullname

    def __str__(self):
        """Return `str(self)`."""
        if isnan(self.diameter):
            diameter_info = "has unknown diameter"
        else:
            diameter_info = f"has a diameter of {self.diameter:.3f} km"
        hazard_info = f"{'is' if self.hazardous else 'is not'} potentially hazardous"
        return f"NEO {self.fullname} {diameter_info} and {hazard_info}."

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return (f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, "
                f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})")

    def serialize(self):
        """Return serialized representation of this object."""
        return {
            'designation': self.designation,
            'name': self.name,
            'diameter_km': self.diameter,
            'potentially_hazardous': self.hazardous
        }


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach to
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initally, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """

    def __init__(self, designation, time, distance, velocity):
        """Create a new `CloseApproach`.

        :param designation: The primary designation of the close approach's NEO
        :type designation: str
        :param time: The UTC date and time at which the NEO passes closest to Earth in YYYY-bb-DD hh:mm format
        :type time: str
        :param distance: The nominal approach distance of the NEO to Earth at the closes point in astronomical units
        :type distance: str
        :param velocity: The velocity of the NEO relative to Earth at the closes point in kilometers per second
        :type velocity: str
        """
        self._designation = designation
        self.time = cd_to_datetime(time)
        self.distance = float(distance)
        self.velocity = float(velocity)

        # Create an attribute for the referenced NEO, originally None.
        self.neo = None

    @property
    def time_str(self):
        """Return a formatted representation of this `CloseApproach`'s approach time.

        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation, the default representation
        includes seconds - significant figures that don't exist in our input
        data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """
        return datetime_to_str(self.time)

    def __str__(self):
        """Return `str(self)`."""
        return f"On {self.time_str} '{self._designation}' approaches Earth at a distance of {self.distance:.2f} au" \
               f" and a velocity of {self.velocity:.2f} km/s."

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return (f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, "
                f"velocity={self.velocity:.2f}, neo={self.neo!r})")

    def serialize(self):
        """Return serialized representation of this object."""
        return {
            'datetime_utc': self.time_str,
            'distance_au': self.distance,
            'velocity_km_s': self.velocity,
            'neo': self.neo.serialize()
        }
