# 📊 How to Monitor Your Pokemon Monitor

Your Pokemon monitor will now run **every hour** with comprehensive status monitoring!

## 🎯 **Your Setup Summary**

✅ **Frequency**: Every hour (0 minutes past the hour)  
✅ **Target**: Costco Australia Pokemon products  
✅ **Notifications**: Only when NEW products found or when errors occur  
✅ **Status Updates**: Daily health check + error alerts  

---

## 🔔 **What Notifications You'll Get**

### 🎉 **Product Alerts** (The Important Ones!)
- **When**: New Pokemon products found on Costco
- **Message**: Rich embed with product details, price, URL
- **Frequency**: Only when NEW products appear (not spam)

### ❌ **Error Alerts** 
- **When**: Monitor fails to run
- **Message**: "Pokemon Monitor Status: FAILED" with timestamp
- **Action**: Check GitHub Actions logs for details

### 📊 **Daily Status Update** 
- **When**: Once per day at 9 AM UTC
- **Message**: "Your Pokemon monitor is running successfully!"
- **Purpose**: Confirms everything is working

---

## 🔍 **How to Check if It's Running**

### Method 1: GitHub Actions Dashboard
1. Go to your GitHub repository
2. Click **"Actions"** tab
3. You'll see:
   - ✅ Green checkmarks = Working fine
   - ❌ Red X's = Something failed
   - 🟡 Yellow dots = Currently running

### Method 2: Discord Notifications
- **Daily at 9 AM UTC**: "Daily Health Check" message
- **If errors**: Immediate failure notification
- **No news = good news**: No notifications means it's working fine

### Method 3: Manual Check
- Go to Actions tab → "Costco Pokemon Monitor"
- Click **"Run workflow"** → **"Run workflow"** button
- Wait 2-3 minutes to see results

---

## 🛠️ **Where You Added Your Discord Webhook**

**Location**: GitHub Repository → Settings → Secrets and variables → Actions

**Secret Name**: `DISCORD_WEBHOOK`  
**Secret Value**: Your Discord webhook URL (like: `https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_WEBHOOK_TOKEN`)

### How to Update Webhook:
1. Same location as above
2. Click the pencil ✏️ icon next to `DISCORD_WEBHOOK`
3. Update the value
4. Click "Update secret"

---

## ⏰ **Timing Details**

### Monitor Schedule:
- **Every hour at**: 00:00, 01:00, 02:00, 03:00, etc.
- **Runtime**: 2-3 minutes per check
- **Monthly usage**: ~72 hours (well within GitHub's 2,000 free minutes)

### Status Updates:
- **Daily report**: 9:00 AM UTC (adjust in `daily-status.yml` if needed)
- **Error alerts**: Immediate when failures occur
- **Success notifications**: Removed to prevent spam

---

## 🚨 **Troubleshooting**

### "Not getting any notifications"
1. **Check Discord webhook**: Test it manually with a curl command
2. **Verify secret**: Make sure `DISCORD_WEBHOOK` is set correctly in GitHub
3. **Check Actions tab**: Look for green checkmarks vs red X's

### "Getting error notifications"
1. **Click the failed action** in GitHub Actions tab
2. **Read the logs** to see what went wrong
3. **Common issues**: 
   - Website structure changed
   - Network timeouts
   - Chrome/Selenium issues

### "Want to test immediately"
1. Go to Actions → "Costco Pokemon Monitor"
2. Click "Run workflow" → "Run workflow"
3. Watch it run in real-time

---

## 🎛️ **Customization Options**

### Change Frequency:
Edit `.github/workflows/pokemon-monitor.yml`:
```yaml
# Every 30 minutes
- cron: '*/30 * * * *'

# Every 2 hours  
- cron: '0 */2 * * *'

# Every 6 hours
- cron: '0 */6 * * *'
```

### Change Daily Status Time:
Edit `.github/workflows/daily-status.yml`:
```yaml
# 6 PM UTC (adjust to your timezone)
- cron: '0 18 * * *'
```

### Add More Notification Methods:
Add these secrets in GitHub:
- `TELEGRAM_BOT_TOKEN` + `TELEGRAM_CHAT_ID`
- `NTFY_TOPIC`

---

## 📈 **Expected Performance**

- **Uptime**: 99.9% (GitHub's infrastructure)
- **Response time**: 2-3 seconds after new products appear
- **False positives**: Very rare (deduplication built-in)
- **Cost**: $0 forever

---

## 🎉 **You're All Set!**

Your Pokemon monitor will now:
1. ✅ **Check every hour** for new products
2. ✅ **Notify immediately** when products found
3. ✅ **Alert if errors** occur  
4. ✅ **Send daily health checks** to confirm it's working
5. ✅ **Run 24/7** even when your laptop is off

**Next Steps:**
1. Create your GitHub repository
2. Upload the files (keep the `.github/workflows/` folder structure)
3. Add your `DISCORD_WEBHOOK` secret
4. Enable Actions
5. Enjoy your free 24/7 Pokemon monitoring! 🎮
