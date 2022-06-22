# OSCAL Exchange Protocol

![OSCAL Exchange Protocol use cases](./images/oxp.drawio.png)

OSCAL Exchange 
Protocol enables integration of 
various assessment tools with 
a cloud provider’s security and 
compliance engine 
(Complaince Automation Center) 
in a standardized manner.

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

## *Tutorials*

##### Post OSCAL Profile using Lifecycle endpoint and get list of OSCAL Profiles using Validation endpoint

<hr>
<details>
<summary>
tutorial: using command line 
</summary>

**0. Setup to issue curl commands**

In new terminal window:

```
$ cd sandbox
$ cd oscal-exchange-protocol
```

**1. Obtain bearer token**

```
$ curl -X 'POST'   'http://localhost:8000/token'   -H 'accept: application/json'   -H 'Content-Type: application/x-www-form-urlencoded'   -d 'grant_type=&username=oxp-user&password=123&scope=&client_id=&client_secret='
```

<details>
<summary>result</summary>

```
{"access_token":"fc54ac91-f674-46b9-bb1d-4da2a169218d","token_type":"bearer"}degenaro:oscal-exchange-protocol
```
</details>

Use the `access_token` value (e.g. fc54ac91-f674-46b9-bb1d-4da2a169218d) for authorization below.

**2. Post OSCAL Profile (Lifecycle)**

```
$ curl -X 'POST' 'http://localhost:8000/profiles' -H 'accept: application/json' -H 'Authorization: Bearer fc54ac91-f674-46b9-bb1d-4da2a169218d' -H 'Content-Type: multipart/form-data'  -F 'profile=@trestle.workspace/profiles/osco.0.1.39.checks.0.1.58/profile.json;type=application/json'

```

Note: use the bearer token obtained in Step 1 above.

<details>
<summary>result</summary>

```
"f342c103-5fb0-4a6e-9bbb-fafb593f9036"
```

</details>

The uuid of the created Profile.

**3. Fetch OSCAL Profile (Validation)**


```
curl -X 'POST' 'http://localhost:8000/profile/component/pvp-component-id?pvp_component_id=roks-cis-node' -H 'accept: application/json' -H 'Content-Type: multipart/form-data' -F 'system_security_plan='
```

<details>
  <summary>result</summary>

```
[
	{
		"profile": {
			"uuid": "31182b1c-32b3-422d-a366-62b39272058c",
			"metadata": {
				"title": "Tailored Profile",
				"last-modified": "2021-08-06T13:25:50.741+00:00",
				"version": "1.0",
				"oscal-version": "1.0.0",
				"props": [
					{
						"name": "profile_mnemonic",
						"ns": "https://my.github.io/compliance-trestle/schemas/oscal/my-cloud",
						"value": "roks-cis-node",
						"class": "scc_profile_mnemonic"
					},
					{
						"name": "base_profile_mnemonic",
						"ns": "https://my.github.io/compliance-trestle/schemas/oscal/my-cloud",
						"value": "ocp4-cis-node",
						"class": "scc_base_profile_mnemonic"
					},
					{
						"name": "osco_version",
						"value": "0.1.39"
					}
				]
			},
			"imports": [
				{
					"href": "https://github.com/ComplianceAsCode/content/blob/master/products/ocp4/profiles/cis-node.profile",
					"exclude-controls": [
						{
							"with-ids": [
								"xccdf_org.ssgproject.content_rule_file_permissions_kube_apiserver",
								"xccdf_org.ssgproject.content_rule_file_owner_kube_apiserver",
								"xccdf_org.ssgproject.content_rule_file_permissions_kube_controller_manager"
							]
						}
					]
				}
			],
			"modify": {
				"set-parameters": [
					{
						"param-id": "kubelet_eviction_thresholds_set_soft_memory_available",
						"values": [
							"500Mi"
						]
					},
					{
						"param-id": "kubelet_eviction_thresholds_set_soft_nodefs_available",
						"values": [
							"10%"
						]
					},
					{
						"param-id": "kubelet_eviction_thresholds_set_soft_nodefs_inodesfree",
						"values": [
							"5%"
						]
					},
					{
						"param-id": "kubelet_eviction_thresholds_set_soft_imagefs_available",
						"values": [
							"15%"
						]
					},
					{
						"param-id": "kubelet_eviction_thresholds_set_soft_imagefs_inodesfree",
						"values": [
							"10%"
						]
					},
					{
						"param-id": "kubelet_eviction_thresholds_set_hard_memory_available",
						"values": [
							"200Mi"
						]
					},
					{
						"param-id": "kubelet_eviction_thresholds_set_hard_nodefs_available",
						"values": [
							"5%"
						]
					},
					{
						"param-id": "kubelet_eviction_thresholds_set_hard_nodefs_inodesfree",
						"values": [
							"4%"
						]
					},
					{
						"param-id": "kubelet_eviction_thresholds_set_hard_imagefs_available",
						"values": [
							"10%"
						]
					},
					{
						"param-id": "kubelet_eviction_thresholds_set_hard_imagefs_inodesfree",
						"values": [
							"5%"
						]
					}
				]
			}
		}
	}
]
```

</details>

The list of profiles corresponding to the specified `pvp_component_id`.

</details>

<hr>
<details>
<summary>
tutorial: using browser
</summary>

**1. Obtain bearer token**

1.1 Select `Authorize`.

![Authorize](./images/authorize.drawio.png)

1.2 Enter user name and password. Select `'Authorize`. Select `Close`.

![Authorize Data](./images/authorize-data.drawio.png)

**2. Post OSCAL Profile (Lifecycle)**

2.1 Select `Add Profile`.

![Profile Add](./images/profile-add.drawio.png)

2.2 Select `Try it out`.

![Profile Try](./images/profile-add-try.drawio.png)

2.3 Select `Choose file`. Navigate to `oscal-exchange-protocol.public/trestle.workspace/profiles/osco.0.1.39.checks.0.1.58/profile.json`. Select `Open`. Select `Execute`.

![Profile Execute](./images/profile-add-execute.drawio.png)

2.4 Note Code 200 and response body UUID (e.g. "31182b1c-32b3-422d-a366-62b39272058c").

![Profile Response](./images/profile-add-response.drawio.png)

**3. Fetch OSCAL Profile (Validation)**

3.1 Select `Policy Validation Point Driven: Get Profiles By Checks`.

![Profile Validate](./images/profile-validate.drawio.png)

3.2 Select `Try it out`.

![Profile Validate Try](./images/profile-validate-try.drawio.png)

3.2 Enter `roks-cis-node`. Select `Execute`.

![Profile Validate Execute](./images/profile-validate-execute.drawio.png)

3.4 Note Code 200 and response body.

![Profile Validate Response](./images/profile-validate-response.drawio.png)

</details>

<hr>