#!/usr/bin/env python3

import argparse
import sys
import time
from urllib.parse import urlparse, urljoin
import requests
from bs4 import BeautifulSoup
from protego import Protego


USER_AGENTS = {
    'OpenAI': {
        'OAI-SearchBot': 'OAI-SearchBot/1.0; +https://openai.com/searchbot',
        'ChatGPT-User': 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; ChatGPT-User/1.0; +https://openai.com/bot',
        'GPTBot': 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; GPTBot/1.1; +https://openai.com/gptbot'
    },
    'Anthropic': {
        'ClaudeBot': 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; ClaudeBot/1.0; +claudebot@anthropic.com)',
        'Claude-User': 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Claude-User/1.0; +Claude-User@anthropic.com)'
    },
    'Perplexity': {
        'PerplexityBot': 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; PerplexityBot/1.0; +https://perplexity.ai/perplexitybot)',
        'Perplexity-User': 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Perplexity-User/1.0; +https://perplexity.ai/perplexity-user)'
    }
}


def validate_url(url):
    try:
        parsed = urlparse(url)
        return parsed.scheme in ('http', 'https') and parsed.netloc
    except Exception:
        return False


def get_robots_parser(url):
    try:
        parsed = urlparse(url)
        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
        
        response = requests.get(robots_url, timeout=10)
        if response.status_code == 200:
            return Protego.parse(response.text)
        return None
    except Exception:
        return None


def check_robots_permission(robots_parser, user_agent, url):
    if not robots_parser:
        return True  # No robots.txt means allowed
    
    try:
        return robots_parser.can_fetch(url, user_agent)
    except Exception:
        print("exception")
        return False  # Parse error means blocked for safety


def crawl_with_user_agents(url):
    robots_parser = get_robots_parser(url)
    
    for company, agents in USER_AGENTS.items():
        for bot_name, user_agent in agents.items():
            try:
                robots_allowed = check_robots_permission(robots_parser, user_agent, url)
                
                headers = {'User-Agent': user_agent}
                start_time = time.time()
                response = requests.get(url, headers=headers, timeout=30)
                load_time = time.time() - start_time
                
                title, robots_meta, has_noindex = parse_html(response.text)
                
                # Calculate is_allowed: status 200 + robots.txt allows + no noindex
                is_allowed = (response.status_code == 200 and robots_allowed and not has_noindex)

                is_allowed_text = "Allowed" if is_allowed else "BLOCKED"
                robots_status = "Allowed" if robots_allowed else "Blocked"
                
                
                print(f"{company} {bot_name}:\t{is_allowed_text}")
                print(f"\tStatus Code:\t{response.status_code}")
                print(f"\tRobots Meta:\t{robots_meta}")
                print(f"\tRobots.txt:\t{robots_status}")
                print(f"\tTitle:\t\t{title}")
                print(f"\tLoad Time:\t{load_time:.2f}s")
                print("-"*60)
                print("")
                
            except requests.exceptions.RequestException as e:
                robots_allowed = check_robots_permission(robots_parser, user_agent, url)
                robots_status = "Allowed" if robots_allowed else "Blocked"
                print(f"{company}/{bot_name}: Error - {str(e)}, Robots.txt='{robots_status}'")


def parse_html(html_content):
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        title_tag = soup.find('title')
        title = title_tag.get_text().strip() if title_tag else 'No title'
        
        robots_tag = soup.find('meta', attrs={'name': 'robots'})
        robots_content = robots_tag.get('content', '').strip() if robots_tag else ''
        
        if not robots_content:
            robots_meta = 'No robots meta'
            has_noindex = False
        else:
            robots_meta = robots_content
            has_noindex = 'noindex' in robots_content.lower()
        
        return title, robots_meta, has_noindex
    except Exception:
        return 'Parse error', 'Parse error', False


def main():
    parser = argparse.ArgumentParser(
        description='JetOctopus AI Bots Testing Tool - Test website accessibility for different AI bot user agents',
        add_help=False
    )
    parser.add_argument('url', nargs='?', help='URL to crawl')
    parser.add_argument('-h', '--help', action='store_true', help='Show this help message')
    
    args = parser.parse_args()
    
    if args.help or not args.url:
        print("JetOctopus AI Bots Testing Tool")
        print("=" * 35)
        print()
        print("Test website accessibility for different AI bot user agents including:")
        print("- OpenAI (GPTBot, ChatGPT-User, OAI-SearchBot)")
        print("- Anthropic (ClaudeBot, Claude-User)")
        print("- Perplexity (PerplexityBot, Perplexity-User)")
        print()
        print("Usage:")
        print(f"  python {sys.argv[0]} <URL>")
        print()
        print("Examples:")
        print(f"  python {sys.argv[0]} https://example.com")
        print(f"  python {sys.argv[0]} https://yourwebsite.com")
        print()
        print("The tool checks robots.txt compliance, meta robots tags,")
        print("and actual HTTP responses to determine real AI bot access.")
        sys.exit(0)
    
    if not validate_url(args.url):
        print(f"Error: Invalid URL '{args.url}'")
        print(f"Please provide a valid URL starting with http:// or https://")
        print(f"Example: python {sys.argv[0]} https://example.com")
        sys.exit(1)
    
    crawl_with_user_agents(args.url)


if __name__ == "__main__":
    main()