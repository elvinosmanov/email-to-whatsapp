# Fix Email Going to Spam

## Immediate Solutions:

### 1. Mark as Not Spam (One-time fix)
1. Open Gmail
2. Go to **Spam** folder
3. Find the "Shift Schedule" emails
4. Select them
5. Click **"Not spam"** button
6. Gmail will learn and move future emails to inbox

### 2. Create a Gmail Filter (Permanent fix)
1. Open Gmail Settings (gear icon → **See all settings**)
2. Go to **Filters and Blocked Addresses** tab
3. Click **Create a new filter**
4. Fill in:
   - **From:** (the sender email address)
   - **Subject:** Shift Schedule
5. Click **Create filter**
6. Check these boxes:
   - ✅ **Never send it to Spam**
   - ✅ **Always mark it as important**
   - ✅ **Categorize as: Primary**
7. Click **Create filter**

### 3. Add Sender to Contacts
1. Open any email from the sender
2. Hover over sender's email
3. Click **"Add to contacts"**
4. Gmail trusts emails from contacts

### 4. Whitelist the sender domain
If emails come from a company domain:
1. Gmail Settings → Filters
2. Create filter with **From:** contains `@company-domain.com`
3. Never send to spam

## Update the Script to Check Spam Folder Too:

I can modify the script to check BOTH inbox and spam folder.
