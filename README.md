# NYC Five Boroughs Address parser

The goal of this project is to be able to identify, parse and geo-encode
New York City postal addresses from a plaintext source.

## Dependencies

  * Pyhon 2.7.6
  * See [Requirements.txt](./requirements.txt)
  * Register your application with [NYC Developer Portal](https://developer.cityofnewyork.us/)
    and make sure that you check off access to the Geoclient API for
    the application. Take note of the Application's ID and key. You will not be
    able to use the ID and key until DoITT approves you -- this could take
    several days, and you will receive an email when this happens. There isn't
    any indication of your status on the dashboard, but all requests will
    return a 403.

## Local deployment (on UNIX/MAC)
 * ```pip install -r requirements.txt```
 * Set DOITT environment variables. One way is to create a file
   and sourcing it:
```
cat <<EOF > DOITT_ENV
export DOITT_CROL_APP_ID=Your_App_ID
export DOITT_CROL_APP_KEY=Your_App_KEY
EOF

source DOITT_ENV
```

* Run the Server
```
python webserver.py
```

* [Explore the api](http://localhost:5000/api)

## Testing

This project uses the [pytest](http://pytest.org/latest/) framework to drive code.

```
# run all tests
py.test -v

# run tests decorated as wip
py.test -m wip

# test an ad-hoc address from the commandline
python nyctext/adparse.py "Johnson Doe: 1802  OCEAN PARKWAY  BKLYN, NY"

# trace the same ad-hoc address to parsing journey
python nyctext/adparse.py --trace "Johnson Doe: 1802  OCEAN PARKWAY  BKLYN, NY"

```

## Team

* [Amal S](https://github.com/cds-amal)
* [Matthew A](https://github.com/mattalhonte)

## Note on Patches/Pull Requests

* Fork the project.
* Make your feature addition or bug fix.
* Add tests to verify your code.
* Pass your tests and old tests.
* Send a pull request. Bonus points for topic branches.

## Thanks

* [BetaNYC](http://betanyc.us/)
* [Datamade](http://datamade.us/) and their awesome [usaddress tagger](https://github.com/datamade/usaddress)

## License
[Apache License, Version 2.0](LICENSE)
