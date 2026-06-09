# Black Market

## Challenge Info

| Field | Details |
|-------|---------|
| **Name** | Black Market |
| **Category** | Web Exploitation |
| **Difficulty** | Easy |
| **Points** | 150 |
| **Flag Format** | `blackperl{...}` |
| **Access** | http://localhost:5001 |
| **Technologies** | Python, Flask, SQLite |

## Description

A web store with a search box vulnerable to SQL injection. Use UNION SELECT to extract the flag from a hidden table.

## Objective

Exploit SQL injection to extract a flag from the secrets table.

## What You Will Learn

- How to test for SQL injection
- How to determine the number of columns using UNION SELECT NULL
- How to extract data from other tables using UNION SELECT

## Skills Required

- Basic web browsing
- Understanding of SQL SELECT and UNION statements

## Hints

1. Try searching for `' OR '1'='1` to confirm SQL injection.
2. Use `' UNION SELECT NULL,NULL,NULL--` to test how many columns exist.
3. Once you know the column count, use `' UNION SELECT id, flag, 1 FROM secrets--` to extract the flag.

## Tools Required

- A web browser

## Setup

```bash
docker build -t black-market .
docker run -d -p 5001:5000 --name black-market black-market
```

## Files Provided

- Access to the web application at the given URL
