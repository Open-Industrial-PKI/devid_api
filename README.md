# IEEE 802.1 AR Python REST API

<br />

## IEEE 802.1 AR in a nutshell

IEEE 802.1 AR is a standard that defines a framework for secure device identity and authentication in a network. It provides a way for devices to securely and reliably establish their identity and authenticate with other devices in the network. The standard specifies the use of digital certificates and a public key infrastructure (PKI) to achieve this goal. The standard also defines a set of protocols and procedures for managing the digital certificates and ensuring their integrity. Overall, IEEE 802.1 AR is a crucial standard for ensuring the security and trustworthiness of devices in a networked environment.

## API Definition

| Route                | Verb       | Info | Status | 
|----------------------|------------| --- | --- | 
| `/mgmt/dev-id-cert/` | **POST**   | return all items  | ✔️ | 
|                      | **POST**   | create a new item | ✔️ |
| `/datas:id`          | **GET**    | return one item   | ✔️ | 
|                      | **PUT**    | update item       | ✔️ |
|                      | **DELETE** | delete item       | ✔️ |

<br />

## Docker config

> Get the code

```bash
$ git clone https://github.com/app-generator/flask-api-sample.git
$ cd flask-api-sample
```

> Start the app in Docker

```bash
$ docker-compose up --build  
```

The API server will start using the PORT `5000`.

<br />

## Using the code

> **Step #1** - Clone the project

```bash
$ git clone https://github.com/app-generator/flask-api-sample.git
$ cd flask-api-sample
```

<br />

> **Step #2** - create virtual environment using python3 and activate it 

```bash
$ virtualenv env
$ source env/bin/activate
$
$ # Virtualenv modules installation (Windows based systems)
$ # virtualenv env
$ # .\env\Scripts\activate
```

<br />

> **Step #3** - Install dependencies in virtualenv

```bash
$ pip install -r requirements.txt
```

<br />

> **Step #4** - setup `flask`

```bash
$ export FLASK_APP=run.py
$ export FLASK_ENV=development
```
<br />

> **Step #5** - start test APIs server at `localhost:5000`

```bash
$ flask run --host=0.0.0.0 --port=5000
```

Swagger API documentation is available at http://YOUR_HOST_NAME:5000/v1/

<br />

## ✨ Project Structure

```bash
api-server-flask/
├── api
│   ├── __init__.py
│   ├── apis
│   │   ├── __init__.py
│   │   ├── highlevel_idev_service_interface.py
│   │   ├── highlevel_ldev_service_interface.py
│   │   ├── Idev_cert_service_interface.py
│   │   ├── Idev_chain_service_interface.py
│   │   ├── Idev_key_service_interface.py
│   │   ├── Ldev_cert_service_interface.py
│   │   ├── Ldev_chain_service_interface.py
│   │   ├── Ldev_key_service_interface.py
│   │   ├── management_interface.py
│   ├── adapters
│   │   ├── __init__.py
│   │   ├── ...
├── README.md
├── requirements.txt
└── run.py
```
<br />

