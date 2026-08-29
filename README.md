# HookBox

HookBox is a simple webhook inspection and debugging tool built with Django and Django REST Framework.

It lets you create temporary webhook endpoints, capture incoming HTTP requests, inspect their contents, and review request history from an authenticated API.

## Features

- Create unique webhook endpoints
- Capture GET, POST, PUT, PATCH, and DELETE requests
- Store headers, query parameters, body, method, and timestamp
- View request history for each endpoint
- Filter and order captured requests
- Pagination support
- User-based endpoint ownership
- Rate limiting for burst and sustained traffic
- Public webhook capture URLs
- Protected management API

## Example

Create an endpoint through the API and you’ll receive a unique webhook URL:

```text
http://localhost:3000/api/webhook/<token>/
