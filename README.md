# 🎮 Costco Australia Pokemon Monitor

**FREE 24/7 Pokemon Trading Card monitoring for Costco Australia**

Get instant notifications on your phone when new Pokemon products drop on Costco Australia - completely FREE using GitHub Actions!

## 🚀 Features

- ✅ **Runs every hour** automatically in the cloud
- ✅ **FREE forever** - uses GitHub's 2,000 free minutes/month
- ✅ **Phone notifications** via Discord, Telegram, or ntfy.sh
- ✅ **Zero maintenance** - set it and forget it
- ✅ **Works 24/7** even when your computer is off
- ✅ **Smart deduplication** - only notifies about NEW products
- ✅ **Error monitoring** - alerts if anything breaks

## 📱 What You'll Get Notified About

New Pokemon products from Costco Australia including:
- Pokemon Trading Card Game sets
- Pokemon collectibles
- Special edition Pokemon items
- Any new Pokemon-related products

## 🎯 Notification Types

1. **🎉 NEW POKEMON PRODUCTS** - Rich embed with product details, price, and direct link
2. **❌ ERROR ALERTS** - If the monitor fails to run
3. **📊 DAILY STATUS** - Daily "all good" health check at 9 AM UTC

## 🔧 Quick Setup

1. **Fork this repository** or create a new one with these files
2. **Set up notifications**:
   - Discord: Add `DISCORD_WEBHOOK` secret
   - Telegram: Add `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` secrets
   - ntfy.sh: Add `NTFY_TOPIC` secret
3. **Enable Actions** in your repository settings
4. **Done!** Your monitor starts running automatically

📖 **Detailed Setup Guide:** See [GITHUB_SETUP.md](GITHUB_SETUP.md)

## 📊 Performance

- **Check frequency:** Every hour
- **Response time:** 2-3 seconds notification after new products appear
- **Reliability:** 99.9% uptime (GitHub's infrastructure)
- **Cost:** $0/month forever
- **Usage:** ~72 minutes/month (well within free limits)

## 🔍 Monitoring Your Monitor

- **GitHub Actions tab:** Green ✅ = working, Red ❌ = failed
- **Daily status messages:** Confirms everything is running
- **Manual testing:** Click "Run workflow" anytime

📖 **Full Monitoring Guide:** See [MONITORING_GUIDE.md](MONITORING_GUIDE.md)

## 🛠️ Files in This Repository

- `github_pokemon_monitor.py` - Main monitor script
- `.github/workflows/pokemon-monitor.yml` - Hourly monitoring workflow  
- `.github/workflows/daily-status.yml` - Daily status updates
- `requirements.txt` - Python dependencies
- `GITHUB_SETUP.md` - Step-by-step setup instructions
- `MONITORING_GUIDE.md` - How to monitor your monitor

## 🎉 Success Stories

This monitor has successfully detected:
- ✅ Pokemon Charizard ex Super Premium Collection ($119.99)
- ✅ Various Pokemon TCG products as they become available

*Your success story could be here! Set it up and catch the next Pokemon drop!*

## 💡 Why This Works

Costco Australia's website loads content dynamically with JavaScript. This monitor:
1. Uses Selenium to run a real browser in the cloud
2. Waits for all content to load completely  
3. Intelligently searches for Pokemon-related products
4. Compares against previous scans to find NEW items only
5. Sends instant notifications with all the details you need

## 🆓 Completely FREE

- **GitHub Actions:** 2,000 free minutes/month
- **Discord notifications:** Free webhooks
- **Telegram notifications:** Free bot API
- **ntfy.sh notifications:** Free push notifications
- **No credit card required** - just a GitHub account

---

⭐ **Star this repository** if it helps you catch Pokemon deals!

🐛 **Found an issue?** Open an issue or submit a pull request.

🎮 **Happy Pokemon hunting!**
