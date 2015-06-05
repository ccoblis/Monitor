## Monitor Project - CloudBase ![Project Status](http://img.shields.io/badge/status-beta-blue.svg)

**Table of Contents**

- [Requirements](#requirements)
- [Running Monitor](#running-monitor)

### Requirements

- [Python 2.7](https://www.python.org/download/releases/2.7/)
- [RabbitMQ 3.5.3 or newer](https://www.rabbitmq.com/download.html)
- [PIP](https://pip.pypa.io/en/latest/installing.html)
- [SQLAlchemy](#installing-sqlalchemy-and-pika-using-pip)
- [Pika](#installing-sqlalchemy-and-pika-using-pip)

**Installing SQLAlchemy and Pika using pip**

```bash
pip install -r requirements.txt
```

### Running Monitor

1. Run Controller.py. The controller will add or update any messages into a database received from the nodes where Agent.py is running.

```bash
python Controller.py
```

2. Run Agent.py on every nodes that you want to monitor.

```bash
python Agent.py
```

3. Run Monitor.py on the same machine with Controller.py. This app will display a table with some information about the available nodes.

```bash
python Monitor.py
```
