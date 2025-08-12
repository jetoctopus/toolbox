# AI Bot Access Checker

In the modern digital landscape, AI bots have become a hot topic of debate. Website owners face a critical decision: should they block AI crawlers from accessing their content, or allow them to crawl for potential mentions in AI-powered search and chat applications?

## The AI Bot Dilemma

Recent years have seen a dramatic shift in how websites handle AI bot traffic. Many major sites have implemented varying policies:

- **Some block entirely** - Concerned about content usage without compensation
- **Others allow selectively** - Hoping for visibility in AI-powered search results  
- **Many change policies frequently** - As the AI landscape evolves

The reality is that **modern large websites often employ multi-layered security systems**. Even if AI bots are explicitly allowed in `robots.txt`, they may still be blocked at other levels:

- **CDN-level blocking** (Cloudflare, AWS CloudFront, etc.)
- **Firewall rules** 
- **Rate limiting systems**
- **Geographic restrictions**
- **Dynamic bot detection**

This creates a gap between **intended policy** and **actual access**, making it difficult for website owners to know if their AI bot policies are working as intended.

## What This Tool Does

**AI Bot Access Checker** helps SEO professionals and website owners verify whether AI bots can actually access their websites. Rather than relying solely on `robots.txt` files, this tool performs real-world testing by:

**Testing Multiple AI Bot User Agents**
- OpenAI (GPTBot, ChatGPT-User, OAI-SearchBot)
- Anthropic (ClaudeBot, Claude-User)  
- Perplexity (PerplexityBot, Perplexity-User)

**Comprehensive Analysis**
- HTTP status codes (200, 403, 429, etc.)
- `robots.txt` compliance checking
- Meta robots tag analysis (including `noindex` detection)
- Response times and performance metrics

**Real-World Results**
- Tests from your actual network environment
- Reveals discrepancies between policy and reality
- Shows exactly what each AI bot encounters

## Installation

```bash
# download the archive of bots_checker.py and requirements.txt

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
python bots_checker.py <URL>
```

### Example: Testing Your Website

```bash
python bots_checker.py https://yourwebsite.com
```

**Sample Output:**
```
OpenAI GPTBot:		BLOCKED
	Status Code:	403
	Robots Meta:	No robots meta
	Robots.txt:	Allowed
	Title:		Access Denied
	Load Time:	0.25s
------------------------------------------------------------

Anthropic ClaudeBot:	Allowed
	Status Code:	200
	Robots Meta:	index, follow
	Robots.txt:	Allowed
	Title:		Your Website Title
	Load Time:	1.2s
------------------------------------------------------------
```

This output reveals that while your `robots.txt` allows GPTBot, it's actually being blocked at the firewall/CDN level (403 status), while ClaudeBot has full access.

## Understanding Results

### Status Interpretation

- **Allowed**: Bot can access and index content (Status 200, robots.txt allows, no noindex)
- **BLOCKED**: Bot is prevented from accessing content due to:
  - **403/429 Status**: Blocked by firewall, CDN, or rate limiting
  - **robots.txt**: Explicitly disallowed in robots.txt file  
  - **noindex meta**: Page accessible but marked as non-indexable

### Common Scenarios

**CDN/Firewall Blocking**
```
Status Code: 403
Robots.txt: Allowed
→ Bot blocked at infrastructure level despite robots.txt permission
```

**Policy-Based Blocking**
```
Status Code: 200  
Robots.txt: Blocked
→ Proper robots.txt compliance, bot respects disallow rules
```

**Content-Level Blocking**
```
Status Code: 200
Robots.txt: Allowed
Robots Meta: noindex
→ Bot can access but shouldn't index the content
```

## Why This Matters for SEO

### For Website Owners
- **Verify your AI bot strategy** - Ensure your intended policy is actually working
- **Identify configuration gaps** - Find discrepancies between robots.txt and actual access
- **Optimize for AI visibility** - Make informed decisions about AI bot access
- **Monitor policy changes** - Regular testing as AI bot policies evolve

### For SEO Professionals  
- **Competitive analysis** - See how competitors handle AI bot access
- **Client reporting** - Provide concrete data on AI bot accessibility
- **Technical SEO audits** - Include AI bot access in comprehensive site audits
- **Strategy development** - Make data-driven recommendations about AI bot policies

## The Broader Context

As AI-powered search and content discovery continue to grow, the relationship between websites and AI crawlers becomes increasingly important. This tool helps bridge the gap between policy intention and technical reality, ensuring that website owners can make informed decisions about their content's AI accessibility.

Whether you're trying to **maximize AI visibility** or **protect your content**, knowing the actual state of AI bot access to your site is the first step in developing an effective strategy.

## Contributing

Contributions are welcome, especially:
- Additional AI bot user agents
- Enhanced detection methods
- Reporting improvements
- Performance optimizations
