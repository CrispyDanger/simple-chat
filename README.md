
# Simple Chat

[![Django CI](https://github.com/CrispyDanger/simple-chat/actions/workflows/django.yml/badge.svg)](https://github.com/CrispyDanger/simple-chat/actions/workflows/django.yml)




## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`SECRET_KEY`


## Run Locally

Clone the project

```bash
  git clone https://github.com/CrispyDanger/simple-chat
```

Go to the project directory

```bash
  cd simple-chat
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Get Data from db.json
```bash
  python manage.py loaddata db.json
```


Start the server

```bash
  python manage.py runserver
```


## Credentials

Login Credentials For Test Users are:

username: admin
password: admin

username: user1
password: notpassword123

username: user2
password: notpassword123

username: user3
password: notpassword123

username: user4
password: notpassword123

## API Reference

#### Login and Get JWT Token

```http
  POST /api/login/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `username` | `string` | **Required**. Your username |
| `password`| `string` | **Required**, Your password|

#### Get Threads

```http
  GET /api/threads/
```

#### Create New Thread/Get existing thread

```http
  POST /api/threads/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `username` | `string` | **Required**. username of other thread participant |

### Get List of Messages from Thread

```http
  GET /api/threads/{thread_id}/messages/
```
| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `thread_id` | `integer` | **Required**. id of a thread

## Create New Message

```http
  POST /api/threads/{thread_id}/messages/new/
```
| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `thread_id` | `integer` | **Required**. id of a thread
| `text`| `string` | **Required**, Text for Message|


## Mark Message as Read/DetailView for Message

```http
  GET /api/threads/{thread_id}/messages/{message_id}/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `thread_id` | `integer` | **Required**. id of a thread
| `message_id`| `integer` | **Required**, id of a message|


# Retrieve a number of unread messages

```http
  GET /api/messages/unread/
```
