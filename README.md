# oscal-exchange-protocol

## *Live demo*

[live demo](https://oxp-swagger.nsn35y94ms7.us-south.codeengine.appdomain.cloud/docs)

## *Install locally*

**Check Python version**

It should be 3.9 or greater.

```
$ python -V
Python 3.9.9
```

**Clone the project**

```
$ cd
$ mkdir sandbox
$ cd sandbox
$ git clone https://github.com/degenaro/oscal-exchange-protocol.git
$ cd oscal-exchange-protocol
```

**Install prereqs and launch webserver**

```
$ make run
```

**Visit website**

```
Enter URL in browser http://127.0.0.1:8000/docs
```

**Setup to issue curl commands**

In new terminal window:

```
$ cd sandbox
$ cd oscal-exchange-protocol
```

**Using command line, post OSCAL Profile (Lifecycle)**

```
$ curl -X 'POST' 'http://localhost:8000/profiles' -H 'accept: application/json' -H 'Authorization: Bearer cc3b58d7-44c0-4b82-b7d3-2a7acad97ccd' -H 'Content-Type: multipart/form-data'  -F 'profile=@trestle.workspace/profiles/osco.0.1.39.checks.0.1.58/profile.json;type=application/json'
```

**Using command line, fetch OSCAL Profile (Validation)**


```
curl -X 'POST' 'http://localhost:8000/profile/component/pvp-component-id?pvp_component_id=roks-cis-node' -H 'accept: application/json' -H 'Content-Type: multipart/form-data' -F 'system_security_plan='
```