doge
====
"Why are you shib(e)?"

```
        leee / shibboleth / achernya + 2016-11-16 21:12:45
            Why are you shib
        leee / shibboleth / leee + 2016-11-16 21:13:03
            why not doge
```

Shibboleth is a very wonderful federated identity/single sign-on project, but is
just terrible to deal with when trying to access resources on a Service Provider
(SP) web server that has Shibboleth content protection enabled.

In the past, I had juggled header dumps and cookie jars and begged and pleaded
[`curl`](https://curl.haxx.se/) with a variety of shell scripts, only to keep
running into changes in the WAYF (Where Are You From) or IdP (Identity Provider)
services breaking my terrible string manipulation techniques.

In 2014, [MIT IS&T](https://ist.mit.edu/) began exploring and eventually rolled
out two-factor authentication with the [Duo Security](https://duo.com/) Trusted
Access platform, tying it in with many services, including MIT's branded
IdP, [Touchstone](https://ist.mit.edu/touchstone). It was no longer possible to
such clunky tooling.

I am a fan of keeping things simple. Unfortunately, trying to perform witchcraft
on shell scripts to make it talk Shib(e), and _then_ Duo? That way lies madness.

Therefore, I present to you a [Python](https://www.python.org/) script that uses
[`mechanize`](https://pypi.python.org/pypi/mechanize) to act as a browser to go
through the log in process.

At the moment, `doge` uses a Touchstone Collaboration account to log in, but it
is very much feasible to use certificates with `mechanize` and then teach the
script how to fire off a Duo Push, prompt for a passcode, or perhaps with enough
abuse, do OTP within the script.

Some working example scripts are provided in `examples/`. You must have an
account to proceed beyond this point - as noted before, `doge` uses Touchstone
Collaboration accounts - use of Athena accounts is possible only after getting
certificate (yes, stored passwords work and we do it, but is less than ideal)
and Duo support.

Use `doge` at your own risk. If you are using this for something related to MIT,
please, ___very - carefully - read___ the following documents:
- [Athena Rules of Use](https://ist.mit.edu/athena/olh/rules)
- [MITnet Rules of Use](https://ist.mit.edu/network/rules)

If you are using this elsewhere, please make sure that you are operating within
the bounds of any agreements you've made.

```sh
leee@null ~/doge> cat secrets.py
# MIT's Touchstone Collaboration account
cams_username = "user@mit.edu"
cams_password = "hunter2"
leee@null ~/doge> python doge.py https://shibe.mit.edu/desired-webpage
# ...html for that webpage...
leee@null ~/doge> cd examples/
leee@null ~/doge/examples> python cogen.py # obtains MIT Cogeneration Project \
                                           # public (to MIT) sensor data. \
                                           # I use this to get local weather.
+--------------------+--------------------------------+--------------+-------+
| tag                | desc                           | value        | unit  |
+--------------------+--------------------------------+--------------+-------+
| ppj13total         | Current MIT Load               | 20.627729    | MW    |
| gt1ji370           | Current MIT Gas Turbine Output | 0            | MW    |
| ppj13utautb        | Current Import from NSTAR      | 20.627729    | MW    |
| ms6fstot           | Total MIT Steam Load           | 180.25244    | ?     |
| ms6fi01            | Heat Recovery Steam Generation | 1.8310547E-2 | ?     |
| totaltns           | Total MIT Chilling Load        | 3002.1934    | ?     |
| WS:OutsideTemp     | Outside Temperature            | 49           | degF  |
| WS:DewPoint        | Dew Point                      | 40           | degF  |
| WS:InsideTemp      | Rack Room Temperature          | 68           | degF  |
| WS:WindSpeed       | Wind Speed                     | 0            | mph   |
| WS:WindDirection   | Wind Direction                 | 3            | deg   |
| WS:Barometer       | Barometric Pressure            | 30           | in Hg |
| WS:InsideHumidity  | Rack Room Humidity             | 30           | pct   |
| WS:OutsideHumidity | Outside Relative Humidity      | 70           | pct   |
| WS:TotalRain       | Total Rainfall                 | 295          | in    |
| WS:WindChill       | Wind Chill                     | 49           | degF  |
| WS:Barometer:SI    | Barometric Pressure            | 1,013        | mb    |
| WS:DewPoint:SI     | Dew Point                      | 4            | C     |
| WS:OutsideTemp:SI  | Outside Temperature            | 9            | C     |
+--------------------+--------------------------------+--------------+-------+
leee@null ~/doge/examples> python listmaker.py shib # Use at your own risk. \
                                                    # Provided as proof of \
                                                    # concept. Read MITnet and \
                                                    # Athena Rules of Use over \
                                                    # and over and over.
List: shib
Description:
Flags: active, private, and visible
shib is not a maillist and is not a group
Owner: USER leee
Last modified by daemon/listmaker.mit.edu@ATHENA.MIT.EDU with Python on 17-nov-2016 05:53:15
leee@null ~/doge/examples>
```
