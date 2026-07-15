#!/usr/bin/env python3
"""
India Market News Fetcher
Fetches and categorizes Indian stock market news from RSS feeds.

Usage:
    # Daily briefing from all sources
    python3 news_fetcher.py

    # Stock-specific news
    python3 news_fetcher.py --stock RELIANCE

    # Sector news
    python3 news_fetcher.py --sector banking

    # Custom date range (days back)
    python3 news_fetcher.py --days 7

    # Output as JSON
    python3 news_fetcher.py --format json

    # Save to file
    python3 news_fetcher.py --output reports/daily_briefing.md
"""

import argparse
import json
import re
import sys
from datetime import datetime, timedelta
from typing import Optional
from dataclasses import dataclass, field, asdict

try:
    import feedparser
    HAS_FEEDPARSER = True
except ImportError:
    HAS_FEEDPARSER = False

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

try:
    import yfinance as yf
    HAS_YFINANCE = True
except ImportError:
    HAS_YFINANCE = False


# ──────────────────────────────────────────────
# RSS Feed Sources
# ──────────────────────────────────────────────

RSS_FEEDS = {
    "moneycontrol_markets": {
        "url": "https://www.moneycontrol.com/rss/marketreports.xml",
        "source": "MoneyControl",
        "category": "Markets",
        "tier": 2,
    },
    "moneycontrol_news": {
        "url": "https://www.moneycontrol.com/rss/latestnews.xml",
        "source": "MoneyControl",
        "category": "General",
        "tier": 2,
    },
    "moneycontrol_business": {
        "url": "https://www.moneycontrol.com/rss/business.xml",
        "source": "MoneyControl",
        "category": "Business",
        "tier": 2,
    },
    "moneycontrol_buzzing": {
        "url": "https://www.moneycontrol.com/rss/buzzingstocks.xml",
        "source": "MoneyControl",
        "category": "Stocks",
        "tier": 2,
    },
    "moneycontrol_ipo": {
        "url": "https://www.moneycontrol.com/rss/iponews.xml",
        "source": "MoneyControl",
        "category": "IPO",
        "tier": 2,
    },
    "moneycontrol_economy": {
        "url": "https://www.moneycontrol.com/rss/economy.xml",
        "source": "MoneyControl",
        "category": "Macro",
        "tier": 2,
    },
    "moneycontrol_results": {
        "url": "https://www.moneycontrol.com/rss/results.xml",
        "source": "MoneyControl",
        "category": "Earnings",
        "tier": 2,
    },
    "et_markets": {
        "url": "https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms",
        "source": "Economic Times",
        "category": "Markets",
        "tier": 2,
    },
    "et_stocks": {
        "url": "https://economictimes.indiatimes.com/markets/stocks/rssfeeds/2146842.cms",
        "source": "Economic Times",
        "category": "Stocks",
        "tier": 2,
    },
    "livemint_markets": {
        "url": "https://www.livemint.com/rss/markets",
        "source": "LiveMint",
        "category": "Markets",
        "tier": 2,
    },
    "livemint_companies": {
        "url": "https://www.livemint.com/rss/companies",
        "source": "LiveMint",
        "category": "Companies",
        "tier": 2,
    },
    "business_standard": {
        "url": "https://www.business-standard.com/rss/markets-106.rss",
        "source": "Business Standard",
        "category": "Markets",
        "tier": 2,
    },
    "ndtv_business": {
        "url": "https://feeds.feedburner.com/ndtvprofit-latest",
        "source": "NDTV Profit",
        "category": "Business",
        "tier": 3,
    },
}

# ──────────────────────────────────────────────
# Event Classification Keywords
# ──────────────────────────────────────────────

EVENT_KEYWORDS = {
    "Earnings": [
        "quarterly results", "Q1", "Q2", "Q3", "Q4", "earnings", "profit",
        "revenue", "net income", "PAT", "EBITDA", "results declared",
        "topline", "bottomline", "YoY growth", "QoQ", "guidance",
    ],
    "Corporate Action": [
        "dividend", "bonus", "stock split", "buyback", "rights issue",
        "face value", "record date", "ex-date", "ex-dividend",
    ],
    "M&A": [
        "acquisition", "merger", "demerger", "takeover", "stake sale",
        "buyout", "amalgamation", "joint venture", "strategic investment",
    ],
    "Management": [
        "CEO", "MD", "chairman", "appointed", "resigned", "board",
        "managing director", "CFO", "key managerial",
    ],
    "Regulatory": [
        "SEBI", "RBI", "circular", "regulation", "compliance", "penalty",
        "norm", "guideline", "framework", "notification",
    ],
    "Institutional": [
        "FII", "FPI", "DII", "mutual fund", "bulk deal", "block deal",
        "institutional", "promoter", "insider trading", "SAST",
    ],
    "IPO": [
        "IPO", "initial public offering", "listing", "subscription",
        "allotment", "DRHP", "RHP", "anchor investor", "OFS",
    ],
    "Macro": [
        "GDP", "inflation", "CPI", "WPI", "IIP", "PMI", "trade deficit",
        "fiscal deficit", "current account", "unemployment",
    ],
    "Global": [
        "Fed", "US market", "Wall Street", "Nasdaq", "S&P 500", "Dow Jones",
        "crude oil", "dollar", "tariff", "global", "China", "recession",
    ],
    "Rating": [
        "upgrade", "downgrade", "target price", "outperform", "underperform",
        "buy rating", "sell rating", "hold rating", "analyst",
    ],
}

# ──────────────────────────────────────────────
# Sentiment Keywords
# ──────────────────────────────────────────────

BULLISH_KEYWORDS = [
    "rally", "surge", "soar", "gain", "jump", "rise", "bullish", "record high",
    "breakout", "upgrade", "outperform", "beat estimate", "strong results",
    "positive", "boom", "recovery", "expansion", "growth", "optimistic",
    "buying", "accumulate", "all-time high",
]

BEARISH_KEYWORDS = [
    "crash", "plunge", "sink", "fall", "drop", "decline", "bearish", "low",
    "breakdown", "downgrade", "underperform", "miss estimate", "weak results",
    "negative", "slump", "contraction", "slowdown", "pessimistic",
    "selling", "exit", "52-week low", "correction", "panic",
]

# ──────────────────────────────────────────────
# Sector Keywords
# ──────────────────────────────────────────────

SECTOR_KEYWORDS = {
    "Banking": ["bank", "HDFC", "ICICI", "SBI", "Kotak", "Axis", "NPA", "NIM", "credit growth", "deposit"],
    "IT": ["IT", "TCS", "Infosys", "Wipro", "HCL", "Tech Mahindra", "software", "digital", "AI", "cloud"],
    "Pharma": ["pharma", "drug", "FDA", "ANDA", "API", "hospital", "healthcare", "Sun Pharma", "Dr Reddy"],
    "Auto": ["auto", "Maruti", "Tata Motors", "Bajaj", "Hero", "EV", "electric vehicle", "sales data"],
    "FMCG": ["FMCG", "HUL", "ITC", "Nestle", "Britannia", "consumer", "rural demand"],
    "Realty": ["real estate", "realty", "DLF", "Godrej Properties", "housing", "RERA"],
    "Metal": ["metal", "steel", "Tata Steel", "JSW", "Hindalco", "aluminium", "iron ore", "copper"],
    "Energy": ["oil", "gas", "ONGC", "Reliance", "BPCL", "IOC", "crude", "refining", "energy"],
    "Infra": ["infra", "L&T", "construction", "highway", "railway", "smart city", "cement"],
    "Telecom": ["telecom", "Airtel", "Jio", "Vodafone", "5G", "spectrum", "ARPU", "subscriber"],
    "Power": ["power", "NTPC", "electricity", "renewable", "solar", "wind", "grid", "transmission"],
    "Defence": ["defence", "defense", "HAL", "BEL", "BDL", "missile", "military", "arms"],
}

# ──────────────────────────────────────────────
# NSE Stock Symbols (Common)
# ──────────────────────────────────────────────

STOCK_NAME_TO_SYMBOL = {
    "reliance": "RELIANCE", "tcs": "TCS", "infosys": "INFY", "infy": "INFY",
    "hdfc bank": "HDFCBANK", "hdfcbank": "HDFCBANK", "icici bank": "ICICIBANK",
    "icicibank": "ICICIBANK", "sbi": "SBIN", "state bank": "SBIN",
    "kotak": "KOTAKBANK", "axis bank": "AXISBANK", "wipro": "WIPRO",
    "hcl": "HCLTECH", "tech mahindra": "TECHM", "bharti airtel": "BHARTIARTL",
    "airtel": "BHARTIARTL", "itc": "ITC", "hindustan unilever": "HINDUNILVR",
    "hul": "HINDUNILVR", "larsen": "LT", "l&t": "LT", "bajaj finance": "BAJFINANCE",
    "maruti": "MARUTI", "tata motors": "TATAMOTORS", "sun pharma": "SUNPHARMA",
    "titan": "TITAN", "asian paints": "ASIANPAINT", "adani": "ADANIENT",
    "mahindra": "M&M", "m&m": "M&M", "power grid": "POWERGRID", "ntpc": "NTPC",
    "ultratech": "ULTRACEMCO", "nestle": "NESTLEIND", "bajaj auto": "BAJAJ-AUTO",
    "hero motocorp": "HEROMOTOCO", "dr reddy": "DRREDDY", "cipla": "CIPLA",
    "divis": "DIVISLAB", "grasim": "GRASIM", "britannia": "BRITANNIA",
    "godrej": "GODREJCP", "tata steel": "TATASTEEL", "jsw steel": "JSWSTEEL",
    "hindalco": "HINDALCO", "coal india": "COALINDIA", "ongc": "ONGC",
    "bpcl": "BPCL", "ioc": "IOC", "gail": "GAIL", "dlf": "DLF",
    "hal": "HAL", "bel": "BEL",
}


@dataclass
class NewsItem:
    """Represents a single news item."""
    title: str
    source: str
    published: str
    link: str
    category: str = "General"
    event_type: str = "Uncategorized"
    sentiment: str = "Neutral"
    impact_score: int = 3
    sectors: list = field(default_factory=list)
    stocks_mentioned: list = field(default_factory=list)
    summary: str = ""


def classify_event(title: str, summary: str = "") -> str:
    """Classify news into event type based on keywords."""
    text = (title + " " + summary).lower()
    scores = {}
    for event_type, keywords in EVENT_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw.lower() in text)
        if score > 0:
            scores[event_type] = score
    if scores:
        return max(scores, key=scores.get)
    return "General"


def detect_sentiment(title: str, summary: str = "") -> str:
    """Detect sentiment from title and summary."""
    text = (title + " " + summary).lower()
    bull_score = sum(1 for kw in BULLISH_KEYWORDS if kw in text)
    bear_score = sum(1 for kw in BEARISH_KEYWORDS if kw in text)
    if bull_score > bear_score and bull_score >= 2:
        return "Bullish"
    elif bear_score > bull_score and bear_score >= 2:
        return "Bearish"
    elif bull_score > 0 and bear_score == 0:
        return "Bullish"
    elif bear_score > 0 and bull_score == 0:
        return "Bearish"
    return "Neutral"


def detect_sectors(title: str, summary: str = "") -> list:
    """Detect which sectors are mentioned."""
    text = (title + " " + summary).lower()
    sectors = []
    for sector, keywords in SECTOR_KEYWORDS.items():
        for kw in keywords:
            if kw.lower() in text:
                sectors.append(sector)
                break
    return sectors


def detect_stocks(title: str, summary: str = "") -> list:
    """Detect stock symbols mentioned in the text."""
    text = (title + " " + summary).lower()
    stocks = []
    for name, symbol in STOCK_NAME_TO_SYMBOL.items():
        if name in text and symbol not in stocks:
            stocks.append(symbol)
    return stocks


def score_impact(item: NewsItem) -> int:
    """Score the market impact of a news item (1-10)."""
    score = 3  # baseline

    # Event type scoring
    high_impact = ["M&A", "Regulatory", "Macro", "IPO"]
    medium_impact = ["Earnings", "Institutional", "Rating", "Global"]
    if item.event_type in high_impact:
        score += 2
    elif item.event_type in medium_impact:
        score += 1

    # Sentiment strength
    if item.sentiment in ("Bullish", "Bearish"):
        score += 1

    # Nifty 50 stocks get a boost
    nifty50_stocks = {
        "RELIANCE", "TCS", "HDFCBANK", "INFY", "ICICIBANK", "HINDUNILVR",
        "SBIN", "BHARTIARTL", "ITC", "KOTAKBANK", "LT", "AXISBANK",
        "BAJFINANCE", "MARUTI", "TATAMOTORS", "SUNPHARMA", "TITAN",
        "ASIANPAINT", "HCLTECH", "WIPRO", "NTPC", "POWERGRID",
    }
    if any(s in nifty50_stocks for s in item.stocks_mentioned):
        score += 1

    # Multiple sectors affected
    if len(item.sectors) >= 2:
        score += 1

    return min(10, max(1, score))


def fetch_rss_feeds(
    days_back: int = 1,
    stock_filter: Optional[str] = None,
    sector_filter: Optional[str] = None,
) -> list[NewsItem]:
    """Fetch news from RSS feeds."""
    if not HAS_FEEDPARSER:
        print("ERROR: feedparser not installed. Run: pip install feedparser")
        sys.exit(1)

    cutoff = datetime.now() - timedelta(days=days_back)
    all_items = []

    for feed_name, feed_info in RSS_FEEDS.items():
        try:
            feed = feedparser.parse(feed_info["url"])
            for entry in feed.entries[:20]:  # limit per feed
                # Parse published date
                published = ""
                if hasattr(entry, "published"):
                    published = entry.published
                elif hasattr(entry, "updated"):
                    published = entry.updated

                title = entry.get("title", "").strip()
                summary = entry.get("summary", "").strip()
                # Strip HTML tags from summary
                summary = re.sub(r"<[^>]+>", "", summary)[:300]
                link = entry.get("link", "")

                if not title:
                    continue

                item = NewsItem(
                    title=title,
                    source=feed_info["source"],
                    published=published,
                    link=link,
                    category=feed_info["category"],
                    summary=summary,
                )

                # Classify
                item.event_type = classify_event(title, summary)
                item.sentiment = detect_sentiment(title, summary)
                item.sectors = detect_sectors(title, summary)
                item.stocks_mentioned = detect_stocks(title, summary)
                item.impact_score = score_impact(item)

                # Apply filters
                if stock_filter:
                    stock_upper = stock_filter.upper()
                    stock_lower = stock_filter.lower()
                    if (
                        stock_upper not in item.stocks_mentioned
                        and stock_lower not in title.lower()
                        and stock_lower not in summary.lower()
                    ):
                        continue

                if sector_filter:
                    sector_lower = sector_filter.lower()
                    if not any(s.lower() == sector_lower for s in item.sectors):
                        # Also check title/summary for sector keyword
                        if sector_lower not in title.lower() and sector_lower not in summary.lower():
                            continue

                all_items.append(item)

        except Exception as e:
            print(f"Warning: Failed to fetch {feed_name}: {e}", file=sys.stderr)

    # Sort by impact score (descending), then by source tier
    all_items.sort(key=lambda x: (-x.impact_score, x.source))

    # Deduplicate by similar titles
    seen_titles = set()
    unique_items = []
    for item in all_items:
        # Simple dedup: normalize title
        normalized = re.sub(r"[^a-z0-9]", "", item.title.lower())[:50]
        if normalized not in seen_titles:
            seen_titles.add(normalized)
            unique_items.append(item)

    return unique_items


def get_stock_price(symbol: str) -> Optional[dict]:
    """Fetch current stock price using yfinance."""
    if not HAS_YFINANCE:
        return None
    try:
        ticker = yf.Ticker(f"{symbol}.NS")
        info = ticker.fast_info
        return {
            "symbol": symbol,
            "price": round(info.get("lastPrice", 0), 2),
            "change_pct": round(
                ((info.get("lastPrice", 0) - info.get("previousClose", 0))
                 / info.get("previousClose", 1)) * 100, 2
            ) if info.get("previousClose") else 0,
        }
    except Exception:
        return None


def format_sentiment_icon(sentiment: str) -> str:
    """Return emoji icon for sentiment."""
    icons = {
        "Bullish": "🟢",
        "Bearish": "🔴",
        "Neutral": "🟡",
    }
    return icons.get(sentiment, "⚪")


def format_markdown(items: list[NewsItem], stock_filter: Optional[str] = None,
                     sector_filter: Optional[str] = None) -> str:
    """Format news items as markdown."""
    now = datetime.now()
    lines = []

    if stock_filter:
        lines.append(f"# 📰 News Report — {stock_filter.upper()}")
    elif sector_filter:
        lines.append(f"# 📰 Sector News — {sector_filter.title()}")
    else:
        lines.append(f"# 📊 Daily Market News Briefing")

    lines.append(f"\n**Generated:** {now.strftime('%A, %d %B %Y %I:%M %p IST')}")
    lines.append(f"**Total Items:** {len(items)}")
    lines.append("")

    if not items:
        lines.append("No news items found for the given filters.")
        return "\n".join(lines)

    # High impact items (score >= 6)
    high_impact = [i for i in items if i.impact_score >= 6]
    if high_impact:
        lines.append("---")
        lines.append(f"\n## 🔥 High Impact News ({len(high_impact)} items)\n")
        for idx, item in enumerate(high_impact[:10], 1):
            icon = format_sentiment_icon(item.sentiment)
            lines.append(f"### {idx}. {item.title} — [{item.impact_score}/10] {icon}")
            lines.append(f"- **Source:** {item.source} | {item.published}")
            lines.append(f"- **Type:** {item.event_type} | **Sentiment:** {item.sentiment}")
            if item.sectors:
                lines.append(f"- **Sectors:** {', '.join(item.sectors)}")
            if item.stocks_mentioned:
                lines.append(f"- **Stocks:** {', '.join(item.stocks_mentioned)}")
            if item.summary:
                lines.append(f"- {item.summary[:200]}")
            lines.append(f"- [Read more]({item.link})")
            lines.append("")

    # Medium impact items (score 4-5)
    medium_impact = [i for i in items if 4 <= i.impact_score <= 5]
    if medium_impact:
        lines.append("---")
        lines.append(f"\n## 📰 Notable News ({len(medium_impact)} items)\n")
        for idx, item in enumerate(medium_impact[:15], 1):
            icon = format_sentiment_icon(item.sentiment)
            lines.append(f"**{idx}. {item.title}** [{item.impact_score}/10] {icon}")
            lines.append(f"   {item.source} | {item.event_type} | {', '.join(item.sectors) if item.sectors else 'General'}")
            if item.stocks_mentioned:
                lines.append(f"   Stocks: {', '.join(item.stocks_mentioned)}")
            lines.append("")

    # Low impact items (score 1-3)
    low_impact = [i for i in items if i.impact_score <= 3]
    if low_impact:
        lines.append("---")
        lines.append(f"\n## 📋 Other News ({len(low_impact)} items)\n")
        for item in low_impact[:10]:
            icon = format_sentiment_icon(item.sentiment)
            lines.append(f"- {icon} {item.title} — *{item.source}*")
        lines.append("")

    # Sector summary
    sector_counts = {}
    for item in items:
        for sector in item.sectors:
            sector_counts[sector] = sector_counts.get(sector, 0) + 1
    if sector_counts:
        lines.append("---")
        lines.append("\n## 📊 Sector Activity\n")
        lines.append("| Sector | News Count | Sentiment |")
        lines.append("|--------|-----------|-----------|")
        for sector, count in sorted(sector_counts.items(), key=lambda x: -x[1]):
            sector_items = [i for i in items if sector in i.sectors]
            bull = sum(1 for i in sector_items if i.sentiment == "Bullish")
            bear = sum(1 for i in sector_items if i.sentiment == "Bearish")
            if bull > bear:
                sent = "🟢 Bullish"
            elif bear > bull:
                sent = "🔴 Bearish"
            else:
                sent = "🟡 Mixed"
            lines.append(f"| {sector} | {count} | {sent} |")
        lines.append("")

    # Stocks mentioned
    stock_counts = {}
    for item in items:
        for stock in item.stocks_mentioned:
            stock_counts[stock] = stock_counts.get(stock, 0) + 1
    if stock_counts:
        lines.append("---")
        lines.append("\n## 🏢 Most Mentioned Stocks\n")
        lines.append("| Stock | Mentions | Price (Rs.) | Change |")
        lines.append("|-------|----------|-------------|--------|")
        for stock, count in sorted(stock_counts.items(), key=lambda x: -x[1])[:15]:
            price_info = get_stock_price(stock)
            if price_info:
                change_str = f"{price_info['change_pct']:+.2f}%"
                lines.append(f"| {stock} | {count} | {price_info['price']} | {change_str} |")
            else:
                lines.append(f"| {stock} | {count} | — | — |")
        lines.append("")

    # Event type distribution
    event_counts = {}
    for item in items:
        event_counts[item.event_type] = event_counts.get(item.event_type, 0) + 1
    if event_counts:
        lines.append("---")
        lines.append("\n## 📁 News by Category\n")
        lines.append("| Category | Count |")
        lines.append("|----------|-------|")
        for event, count in sorted(event_counts.items(), key=lambda x: -x[1]):
            lines.append(f"| {event} | {count} |")
        lines.append("")

    lines.append("---")
    lines.append("\n*⚠️ Disclaimer: For educational purposes only. Not investment advice.*")

    return "\n".join(lines)


def format_json(items: list[NewsItem]) -> str:
    """Format news items as JSON."""
    return json.dumps(
        {
            "generated_at": datetime.now().isoformat(),
            "total_items": len(items),
            "items": [asdict(item) for item in items],
        },
        indent=2,
        ensure_ascii=False,
    )


def main():
    parser = argparse.ArgumentParser(
        description="India Market News Fetcher — Fetch and categorize Indian stock market news"
    )
    parser.add_argument(
        "--stock", type=str, default=None,
        help="Filter news for a specific stock (e.g., RELIANCE, TCS)"
    )
    parser.add_argument(
        "--sector", type=str, default=None,
        help="Filter news for a sector (e.g., banking, IT, pharma, auto)"
    )
    parser.add_argument(
        "--days", type=int, default=1,
        help="Number of days to look back (default: 1)"
    )
    parser.add_argument(
        "--format", type=str, choices=["markdown", "json"], default="markdown",
        help="Output format (default: markdown)"
    )
    parser.add_argument(
        "--output", type=str, default=None,
        help="Save output to file (default: print to stdout)"
    )
    parser.add_argument(
        "--min-impact", type=int, default=1,
        help="Minimum impact score to include (1-10, default: 1)"
    )
    parser.add_argument(
        "--limit", type=int, default=50,
        help="Maximum number of items to return (default: 50)"
    )

    args = parser.parse_args()

    # Check dependencies
    if not HAS_FEEDPARSER:
        print("ERROR: 'feedparser' package is required.")
        print("Install it with: pip install feedparser")
        sys.exit(1)

    print(f"Fetching news (last {args.days} day(s))...", file=sys.stderr)
    if args.stock:
        print(f"Filtering for stock: {args.stock}", file=sys.stderr)
    if args.sector:
        print(f"Filtering for sector: {args.sector}", file=sys.stderr)

    # Fetch and process
    items = fetch_rss_feeds(
        days_back=args.days,
        stock_filter=args.stock,
        sector_filter=args.sector,
    )

    # Apply min impact filter
    items = [i for i in items if i.impact_score >= args.min_impact]

    # Apply limit
    items = items[:args.limit]

    print(f"Found {len(items)} news items.", file=sys.stderr)

    # Format output
    if args.format == "json":
        output = format_json(items)
    else:
        output = format_markdown(items, args.stock, args.sector)

    # Output
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Report saved to: {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
