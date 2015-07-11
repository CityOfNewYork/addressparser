# -*- coding: utf-8 -*-
__author__ = "C. Sudama, Matthew Alhonte"
__license__ = "Apache License 2.0: http://www.apache.org/licenses/LICENSE-2.0"

class RefLocation:

    def __init__(self, streetAddress, borough, zipcode, latitude, longitude):
        self.streetAddress = streetAddress
        self.borough = borough
        self.zipcode = zipcode
        self.latitude = latitude
        self.longitude = longitude


    def schema_object(self):
        return {
            "@type": "Place",
            "@context": "http://schema.org",
            "address": {
                "@type": "PostalAddress",
                "addressLocality": "New York City",
                "addressRegion": "NY",
                "postalCode": self.zipcode,
                "streetAddress": self.streetAddress.strip(),
                "borough": self.borough
            },

            "geo": {
                "@type": "GeoCoordinates",
                "latitude": self.latitude,
                "longitude": self.longitude
            }
        }
    
