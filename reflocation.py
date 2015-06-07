class RefLocation:

    def __init__(self, streetAddress, borough, zipcode, latitude, longitude):
        self.streetAddress = streetAddress
        self.borough = borough
        self.zipcode = zipcode
        self.latitude = latitude
        self.longitude = longitude


    def schema_object(self):
        return {
        "refLocation": [{
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
            }}]
    }
