# pesu-auth

A simple API to authenticate PESU credentials using PESU Academy

The API is secure and protects user privacy by not storing any user credentials. It only validates credentials and
returns the user's profile information. No personal data is stored or logged.

### PESUAuth LIVE Deployment

* You can access the PESUAuth API endpoint [here](https://pesu-auth.onrender.com/).
* You can view the health status of the API on the [PESUAuth Health Dashboard](https://xzlk85cp.status.cron-job.org/).

> :warning: **Warning:** The live version is hosted on a free tier server, so you might experience some latency on the
> first request since the server might not be awake. Subsequent requests will be faster.

## How to run pesu-auth locally

Running the PESUAuth API locally is simple. Clone the repository and follow the steps below to get started.

### Running with Docker

This is the easiest and recommended way to run the API locally. Ensure you have Docker installed on your system. Run the
following commands to start the API.

1. Build the Docker image

  ```bash
  docker build . --tag pesu-auth
  ```

2. Run the Docker container

  ```bash
  docker run --name pesu-auth -d -p 5000:5000 pesu-auth
  ```

3. Access the API at `http://localhost:5000/`

### Running without Docker

If you don't have Docker installed, you can run the API using Python. Ensure you have Python 3.8 or higher installed on
your system.

1. Create a virtual environment using `conda` or any other virtual environment manager of your choice and activate it.
   Then, install the dependencies using the following command.

  ```bash
  pip install -r requirements.txt
  ```

2. Run the API using the following command.

  ```bash
  python app/app.py
  ```

3. Access the API at `http://localhost:5000/`

# How to use pesu-auth

You can send a request to the `/authenticate` endpoint with the user's credentials and the API will return a JSON
object,
with the user's profile information if requested.

### Request Parameters

| **Parameter**                 | **Optional** | **Type**    | **Default** | **Description**                                                                                 |
|-------------------------------|--------------|-------------|-------------|-------------------------------------------------------------------------------------------------|
| `username`                    | No           | `str`       |             | The user's SRN or PRN                                                                           |
| `password`                    | No           | `str`       |             | The user's password                                                                             |
| `profile`                     | Yes          | `boolean`   | `False`     | Whether to fetch profile information                                                            |
| `know_your_class_and_section` | Yes          | `boolean`   | `False`     | Whether to fetch Know Your Class and Section information                                        |
| `fields`                      | Yes          | `list[str]` | `None`      | Which fields to fetch from the profile information. If not provided, all fields will be fetched |

### Response Object

On authentication, it returns the following parameters in a JSON object. If the authentication was successful and
profile data was requested, the response's `profile` key will store a dictionary with a user's profile information.
**On an unsuccessful sign-in, this field will not exist**.

| **Field**                     | **Type**                        | **Description**                                                                             |
|-------------------------------|---------------------------------|---------------------------------------------------------------------------------------------|
| `status`                      | `boolean`                       | A flag indicating whether the overall request was successful                                |
| `profile`                     | `ProfileObject`                 | A nested map storing the profile information, returned only if requested                    |
| `know_your_class_and_section` | `KnowYourClassAndSectionObject` | A nested map storing the profile information from PESU's Know Your Class and Section Portal |
| `message`                     | `str`                           | A message that provides information corresponding to the status                             |
| `timestamp`                   | `datetime`                      | A timezone offset timestamp indicating the time of authentication                           |
| `error`                       | `str`                           | The error name and stack trace, if an application side error occurs                         |

#### Profile Object

| **Field**           | **Description**                                        |
|---------------------|--------------------------------------------------------|
| `name`              | Name of the user                                       |
| `prn`               | PRN of the user                                        |
| `srn`               | SRN of the user                                        |
| `program`           | Academic program that the user is enrolled into        |
| `branch_short_code` | Abbreviation of the branch that the user is pursuing   |
| `branch`            | Complete name of the branch that the user is pursuing  |
| `semester`          | Current semester that the user is in                   |
| `section`           | Section of the user                                    |
| `email`             | Email address of the user registered with PESU         |
| `phone`             | Phone number of the user registered with PESU          |
| `campus_code`       | The integer code of the campus (1 for RR and 2 for EC) |
| `campus`            | Abbreviation of the user's campus name                 |
| `error`             | The error name and stack trace, if an error occurs     |

#### KnowYourClassAndSectionObject

| **Field**        | **Description**                                                |
|------------------|----------------------------------------------------------------|
| `prn`            | PRN of the user                                                |
| `srn`            | SRN of the user                                                |
| `name`           | Name of the user                                               |
| `class`          | Current semester that the user is in                           |
| `section`        | Section of the user                                            |
| `cycle`          | Physics Cycle or Chemistry Cycle, if the user is in first year |
| `department`     | Abbreviation of the branch along with the campus of the user   |
| `branch`         | Abbreviation of the branch that the user is pursuing           |
| `institute_name` | The name of the campus that the user is studying in            |
| `error`          | The error name and stack trace, if an error occurs             |

## Integrating your application with pesu-auth

Here are some examples of how you can integrate your application with the PESUAuth API using Python and cURL.

### Python

#### Request

```python
import requests

data = {
    'username': 'your SRN or PRN here',
    'password': 'your password here',
    'profile': True,  # Optional, defaults to False
    'know_your_class_and_section': True,  # Optional, defaults to False
    'fields': None,  # Optional, defaults to None to represent all fields
}

response = requests.post("http://localhost:5000/authenticate", json=data)
print(response.json())
```

#### Response

```json
{
  "status": true,
  "profile": {
    "name": "Johnny Blaze",
    "prn": "PES1201800001",
    "srn": "PES1201800001",
    "program": "Bachelor of Technology",
    "branch_short_code": "CSE",
    "branch": "Computer Science and Engineering",
    "semester": "NA",
    "section": "NA",
    "email": "johnnyblaze@gmail.com",
    "phone": "1234567890",
    "campus_code": 1,
    "campus": "RR"
  },
  "message": "Login successful.",
  "know_your_class_and_section": {
    "prn": "PES1201800001",
    "srn": "PES1201800001",
    "name": "JOHNNY BLAZE",
    "class": "",
    "section": "",
    "cycle": "NA",
    "department": "",
    "branch": "CSE",
    "institute_name": ""
  },
  "timestamp": "2024-07-28 22:30:10.103368+05:30"
}
```

### cURL

#### Request

```bash
curl -X POST http://localhost:5000/authenticate \
-H "Content-Type: application/json" \
-d '{
    "username": "your SRN or PRN here",
    "password": "your password here"
}'
```

#### Response

```json
{
  "status": true,
  "message": "Login successful.",
  "timestamp": "2024-07-28 22:30:10.103368+05:30"
}
```