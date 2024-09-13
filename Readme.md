Here are some example usage scenarios. These examples illustrate how to interact with the `FGT` class using the provided methods (`login`, `get`, `post`, `put`, `delete`, and `logout`) and handle the structured responses that contain `status`, `message`, and `data`.

---

### **Initialization**

#### Log in

```python
from FortigateAPI import FGT

# Initialize with just the host
fgt = FGT(host="firewall_host")
# Login after initialization
fgt.login(key="firewall_key")  # default name="admin"
fgt.login(name="admin", key="firewall_key")
```
#### Log in with default name/password
```python

# Initialize with host and login credentials
fgt = FGT(host="firewall_host", key="firewall_key")  # default name="admin"
fgt = FGT(host="firewall_host", name="admin", key="firewall_key")
```

#### Using token
```python
# Initialize with host and token
fgt = FGT(host="firewall_host", token="firewall_token")
```
#### Content manager
```python
# Using the FGT class with a context manager
# It is possible to use all of the above configurations login/token
with FGT(host="firewall_host", key="firewall_key") as fgt:
    # Perform GET request
    get_response = fgt.get("/api/v1/content")
    if get_response["status"] == "success":
        print("Content retrieved:", get_response["data"])
    else:
        print("Error:", get_response["message"], get_response["data"])

    # Define new content data
    new_content = {"title": "New Article", "body": "Content body"}
    
    # Perform POST request
    post_response = fgt.post("/api/v1/content", data=new_content)
    if post_response["status"] == "success":
        print("Content created:", post_response["data"])
    else:
        print("Error:", post_response["message"], post_response["data"])

# No need to explicitly call logout; it's handled automatically
```
### Response format
#### Successful response

```python
{
    "status": "success",
    "message": "Request successful",
    "data": {...}  # JSON data from the response
}
```

#### Error response

```python
{
    "status": "error",
    "message": "Error type",
    "data": "Error details"  # e.g., exception message or a custom error message
}
```
#### Response processing
```python
response = fgt.get("/firewall_endpoint")
if response["status"] != "success":
    print("Error:", response["message"], response["data"])

print("Content retrieved:", response["data"])
```
---
### **Sending requests**

### Initiliazation and Log In
```python
#Import module
from FortigateAPI import FGT

# Create an instance of the FGT class
fgt = FGT(host="firewall_host", name="admin", key="firewall_key")

# Log in to the content manager
login_response = fgt.login()

# Check if the login was successful
if login_response["status"] == "success":
    print("Login successful")
else:
    print("Login failed:", login_response["message"], "Error details:", login_response["data"])


```
#### **GET**

```python
# Send a GET request to fetch some configuration data
get_response = fgt.get("/api/v2/cmdb/firewall/address")

# Handle the response
if get_response["status"] == "success":
    print("GET request successful. Data:", get_response["data"])
else:
    print("GET request failed:", get_response["message"], "Error details:", get_response["data"])
```

**Expected Output (Success):**
```plaintext
GET request successful. Data: {...}  # JSON data from the response
```

**Expected Output (Failure):**
```plaintext
GET request failed: Request failed Error details: 404 Client Error: Not Found for URL: https://firewall.example.com/api/v2/cmdb/firewall/address
```

---

#### **POST**

```python
# Send a POST request to create a new firewall address object
post_data = {
    "name": "example-address",
    "subnet": "192.168.1.0 255.255.255.0",
    "type": "ipmask"
}
post_response = fgt.post("/api/v2/cmdb/firewall/address", data=post_data)

# Handle the response
if post_response["status"] == "success":
    print("POST request successful. Data:", post_response["data"])
else:
    print("POST request failed:", post_response["message"], "Error details:", post_response["data"])
```

**Expected Output (Success):**
```plaintext
POST request successful. Data: {...}  # JSON response confirming the object creation
```

**Expected Output (Failure):**
```plaintext
POST request failed: Request failed Error details: 400 Bad Request: Invalid parameters
```

---

#### **PUT**

```python
# Send a PUT request to update an existing firewall address object
put_data = {
    "subnet": "192.168.2.0 255.255.255.0"
}
put_response = fgt.put("/api/v2/cmdb/firewall/address/example-address", data=put_data)

# Handle the response
if put_response["status"] == "success":
    print("PUT request successful. Data:", put_response["data"])
else:
    print("PUT request failed:", put_response["message"], "Error details:", put_response["data"])
```

**Expected Output (Success):**
```plaintext
PUT request successful. Data: {...}  # JSON response confirming the update
```

**Expected Output (Failure):**
```plaintext
PUT request failed: Request failed Error details: 404 Not Found: The specified object does not exist
```

---

#### **DELETE**

```python
# Send a DELETE request to remove a firewall address object
delete_response = fgt.delete("/api/v2/cmdb/firewall/address/example-address")

# Handle the response
if delete_response["status"] == "success":
    print("DELETE request successful.")
else:
    print("DELETE request failed:", delete_response["message"], "Error details:", delete_response["data"])
```

**Expected Output (Success):**
```plaintext
DELETE request successful.
```

**Expected Output (Failure):**
```plaintext
DELETE request failed: Request failed Error details: 404 Not Found: The specified object does not exist
```

---

### **Logging Out**

```python
# Log out from the firewall
fgt.logout()
print("Logged out successfully.")
```

**Expected Output:**
```plaintext
Logged out successfully.
```

---
