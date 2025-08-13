# 🚀 FREE 24/7 Pokemon Monitor Setup - GitHub Actions

This guide will help you set up your Pokemon monitor to run **completely FREE** in the cloud using GitHub Actions. Your laptop can be off and you'll still get notifications!

## 📋 What You'll Need
- GitHub account (free)
- 5 minutes to set up

## 🔧 Step-by-Step Setup

### 1. Create a GitHub Repository

1. Go to [GitHub.com](https://github.com) and log in
2. Click "New repository" (green button)
3. Name it `costco-pokemon-monitor` 
4. Make it **Public** (required for free GitHub Actions)
5. Click "Create repository"

### 2. Upload Your Files

1. In your new repository, click "uploading an existing file"
2. Drag and drop these files from your local folder:
   - `github_pokemon_monitor.py`
   - The `.github/workflows/pokemon-monitor.yml` file (keep the folder structure)

### 3. Set Up Notifications (Choose Your Preferred Method)

#### Option A: Discord (Recommended - Easiest)
1. Create a Discord server or use an existing one
2. Create these channels: `#new_products`, `#errors`, and `#status` (optional)
3. Go to Server Settings → Integrations → Webhooks
4. Create 3 separate webhooks (one for each channel):
   - **#new_products** webhook (for Pokemon product alerts)
   - **#errors** webhook (for error notifications)
   - **#status** webhook (for daily status updates - optional)
5. In your GitHub repo, go to Settings → Secrets and variables → Actions
6. Add these secrets:
   - `DISCORD_WEBHOOK_NEW_PRODUCTS`: Your #new_products webhook URL
   - `DISCORD_WEBHOOK_ERRORS`: Your #errors webhook URL
   - `DISCORD_WEBHOOK_STATUS`: Your #status webhook URL (optional)

#### Option B: Telegram
1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Send `/newbot` and follow instructions
3. Save your bot token
4. Message your bot, then go to `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates` to find your chat ID
5. Add two GitHub secrets:
   - `TELEGRAM_BOT_TOKEN`: Your bot token
   - `TELEGRAM_CHAT_ID`: Your chat ID

#### Option C: ntfy.sh (Push Notifications)
1. Download the ntfy app on your phone
2. Subscribe to a topic (make up a unique name like `your-pokemon-alerts-2024`)
3. Add GitHub secret:
   - `NTFY_TOPIC`: `https://ntfy.sh/your-unique-topic-name`

### 4. Enable GitHub Actions

1. In your repository, go to the "Actions" tab
2. Click "I understand my workflows, go ahead and enable them"
3. Your monitor will now run every hour automatically!

### 5. Test It Manually

1. Go to Actions → "Costco Pokemon Monitor"
2. Click "Run workflow" → "Run workflow" (green button)
3. Wait 2-3 minutes and check if you get a notification

## 🎯 How It Works

- **Completely FREE**: Uses GitHub's 2,000 free minutes per month
- **Runs every hour**: Checks Costco Australia for new Pokemon products
- **Zero maintenance**: Runs in the cloud, no need to keep your computer on
- **Instant notifications**: Get alerted on your phone the moment new products appear

## 📊 Usage Limits

- GitHub Actions: 2,000 minutes/month (about 66 hours)
- Each run takes ~2-3 minutes
- Running every hour = ~72 minutes/month
- You're well within the free limit!

## 🔧 Customization

Want to check more frequently? Edit `.github/workflows/pokemon-monitor.yml`:

```yaml
schedule:
  # Every 15 minutes
  - cron: '*/15 * * * *'
  
  # Every hour at minute 0
  - cron: '0 * * * *'
```

## 🐛 Troubleshooting

### No notifications?
1. Check Actions tab for error logs
2. Verify your webhook/token secrets are correct
3. Test your Discord/Telegram/ntfy setup manually

### Want to see what's happening?
1. Go to Actions → Latest run → Click on the job
2. View logs to see what products were found

## 🎉 That's It!

Your Pokemon monitor is now running 24/7 in the cloud for FREE! You'll get notified on your phone whenever Costco Australia adds new Pokemon products.

---

## Alternative FREE Options

### Option 2: Railway (15 Minutes Setup)
- Deploy directly from GitHub
- 500 hours free per month
- Persistent storage
- [Setup Guide](https://railway.app)

### Option 3: Render (Web Service)
- 750 hours free per month  
- Automatic deployments from GitHub
- [Setup Guide](https://render.com)

### Option 4: Fly.io
- Generous free tier
- Run 24/7 with good specs
- [Setup Guide](https://fly.io)

**GitHub Actions is recommended because it's the simplest and most reliable for this use case.**
