# Creating Supabase Project and Database Setup

## Step 1: Create Supabase Project

1. Go to [supabase.com](https://supabase.com)
2. Sign up or log in
3. Click "New Project"
4. Fill in:
   - **Name**: AI Interior Designer (or your choice)
   - **Database Password**: Generate a strong password (save it!)
   - **Region**: Choose closest to your GPU VM
   - **Pricing Plan**: Free tier is sufficient for MVP

5. Wait for project to be created (2-3 minutes)

## Step 2: Get Database Credentials

1. In your Supabase project dashboard:
2. Go to **Settings** → **Database**
3. Scroll to **Connection string** section
4. Select **URI** format
5. Copy the connection string (looks like):
   ```
   postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:5432/postgres
   ```

## Step 3: Extract Connection Details

From the connection string, extract:

- **Host**: `db.xxxxx.supabase.co` (the part after `@`)
- **Port**: `5432` (usually)
- **Database**: `postgres` (usually)
- **User**: `postgres` (usually)
- **Password**: The password you set

## Step 4: Configure Environment Variables

Add to your `.env` file:

```bash
# Supabase Database
SUPABASE_DB_HOST=db.xxxxx.supabase.co
SUPABASE_DB_PORT=5432
SUPABASE_DB_NAME=postgres
SUPABASE_DB_USER=postgres
SUPABASE_DB_PASSWORD=your-password-here
```

## Step 5: Allow External Connections

Supabase allows external connections by default, but verify:

1. Go to **Settings** → **Database**
2. Check **Connection pooling** is enabled
3. Note the **Connection string** uses port `5432` for direct connections

## Step 6: Test Connection

Run the initialization script:

```bash
./scripts/supabase-init.sh
```

This will:
- Test the connection
- Run all migrations
- Create required tables

## Step 7: Verify Tables

In Supabase dashboard:
1. Go to **Table Editor**
2. You should see:
   - `users`
   - `projects`
   - `images`
   - `versions`
   - `edit_history`
   - `usage_stats`

## Troubleshooting

### Connection Refused

- Check firewall rules on your GPU VM
- Verify Supabase project is active
- Check password is correct

### SSL Required

Supabase requires SSL. The connection string should include `?sslmode=require` or use the connection pooler.

Update your connection string if needed:
```
postgresql://user:pass@host:port/db?sslmode=require
```

### Migration Errors

- Ensure you're using the correct database name
- Check user has CREATE TABLE permissions
- Verify Alembic is using the correct connection string

## Security Notes

- Never commit `.env` file
- Rotate database password regularly
- Use connection pooling for production
- Enable Supabase's built-in security features

## Next Steps

After Supabase is configured:

1. Update `DATABASE_URL` in `.env` (optional, config will use Supabase vars)
2. Run migrations: `alembic upgrade head`
3. Test with a simple query
4. Proceed with deployment
