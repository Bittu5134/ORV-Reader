const { chromium } = require('playwright');

// Config
const TARGET_URL = 'https://orv.pages.dev/stories/orv/read/ch_8';
const DISCORD_WEBHOOK = process.env.DISCORD_WEBHOOK_URL;

(async () => {
  if (!DISCORD_WEBHOOK) {
    console.error('Error: DISCORD_WEBHOOK_URL environment variable is not defined.');
    process.exit(1);
  }

  console.log(`Launching headless browser to check: ${TARGET_URL}...`);
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();

  let rateLimitError = false;

  // Listen to console warnings and errors
  page.on('console', msg => {
    const text = msg.text();
    if (text.includes('rate limit exceeded') || text.includes('API rate limit already exceeded') || text.includes('rate-limited')) {
      rateLimitError = true;
    }
  });

  try {
    // Navigate to page
    await page.goto(TARGET_URL, { waitUntil: 'load', timeout: 30000 });

    // Scroll to the bottom to trigger Giscus loading checks
    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));

    // Wait 6 seconds for eager load and iframe handshakes
    await page.waitForTimeout(6000);

    // Check if the rate-limit warning banner is present in the DOM
    const bannerExists = await page.evaluate(() => {
      return !!document.getElementById('giscus-auth-banner');
    });

    if (rateLimitError || bannerExists) {
      console.warn('⚠️ Giscus Rate Limit detected!');
      
      const payload = {
        username: 'Giscus Status Bot',
        content: `🚨 **Giscus Rate Limit Warning!**\nThe comments section on ORV-Reader is failing to load due to GitHub API rate limits.\n\n**Details:**\n- **URL Checked**: ${TARGET_URL}\n- **Warning Banner Displayed**: ${bannerExists}\n- **Rate-limit Logs Detected**: ${rateLimitError}\n\nReaders are currently prompted to log in to view comments.`,
        avatar_url: 'https://giscus.app/yinyang.svg'
      };

      // Send to Discord Webhook using global fetch
      const res = await fetch(DISCORD_WEBHOOK, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      
      if (res.ok) {
        console.log('Discord notification sent successfully.');
      } else {
        console.error('Failed to send Discord notification:', res.statusText);
      }
    } else {
      console.log('✅ Giscus loaded successfully with no rate limits.');
    }

  } catch (err) {
    console.error('Error running check:', err);
  } finally {
    await browser.close();
  }
})();
