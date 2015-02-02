# Scrapy settings for transactions_explorer project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'transactions_explorer'

DOWNLOAD_DELAY = 0.25

SPIDER_MODULES = ['transactions_explorer.spiders']
NEWSPIDER_MODULE = 'transactions_explorer.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'transactions_explorer (+http://www.yourdomain.com)'
