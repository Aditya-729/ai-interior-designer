# 🔐 Updating Password in .env

## Your Password
**Password**: `cuetpass#123`

## ⚠️ Important: Special Character Warning

Your password contains the `#` character, which is **special** in `.env` files because it's used for comments.

### ✅ Correct Format for .env File

You **MUST** use quotes around the password in the `.env` file:

```bash
SUPABASE_DB_PASSWORD="cuetpass#123"
```

**NOT:**
```bash
SUPABASE_DB_PASSWORD=cuetpass#123  # ❌ This won't work - # starts a comment
```

---

## How to Update

### Option 1: Manual Edit (Recommended)

1. Open `.env` file:
   ```powershell
   notepad .env
   ```

2. Find line 11:
   ```
   SUPABASE_DB_PASSWORD=REPLACE_WITH_YOUR_ACTUAL_PASSWORD
   ```

3. Replace with (note the quotes):
   ```
   SUPABASE_DB_PASSWORD="cuetpass#123"
   ```

4. Save the file

### Option 2: PowerShell Command

```powershell
(Get-Content .env) -replace 'SUPABASE_DB_PASSWORD=REPLACE_WITH_YOUR_ACTUAL_PASSWORD', 'SUPABASE_DB_PASSWORD="cuetpass#123"' | Set-Content .env
```

---

## Connection String Format

If you need to use this password in a connection string, it should be URL-encoded:

**Original:**
```
postgresql://postgres:cuetpass#123@db.pzsdvpemnroxylbhjirr.supabase.co:5432/postgres
```

**URL-encoded (correct):**
```
postgresql://postgres:cuetpass%23123@db.pzsdvpemnroxylbhjirr.supabase.co:5432/postgres
```

Note: `#` becomes `%23` in URL encoding.

---

## Test After Updating

After updating the password, test the connection:

```bash
bash scripts/supabase-init.sh
```

---

## Why Quotes Are Needed

In `.env` files:
- `#` starts a comment
- Everything after `#` is ignored
- So `PASSWORD=cuetpass#123` would be read as `PASSWORD=cuetpass` (the `#123` is treated as a comment)

Using quotes: `PASSWORD="cuetpass#123"` ensures the entire password including `#` is read correctly.

---

## Security Note

✅ Your password format is valid - PostgreSQL accepts `#` in passwords.  
✅ Just make sure to quote it in `.env` file!
