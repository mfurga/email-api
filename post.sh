#!/bin/bash
# Small script for sending an HTTP POST request to the API server.

curl -X POST -H "Content-Type: application/json; indent=4" -u root:password \
     -d '{"mailbox": "883732a7-a744-4e77-9b8b-0d55eb90d3e6", "template": "01a8f374-f0d4-4c4f-b2f5-0f2327ff971f", "to": ["user@example.com"], "cc": ["user@example.com"], "bcc": ["user@example.com"], "reply_to": "user@example.com"}' \
      http://localhost:8000/api/email/
