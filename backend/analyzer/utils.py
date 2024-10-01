import requests
import time
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from collections import Counter
import re


def calculate_keyword_density(content, target_keyword):
    # Clean up the content by removing HTML tags and special characters
    clean_text = re.sub(r"<[^>]+>", "", content)  # Remove HTML tags
    clean_text = re.sub(
        r"[^\w\s]", "", clean_text
    )  # Remove punctuation and special chars
    words = clean_text.lower().split()

    # Count total words
    total_words = len(words)

    # Count occurrences of the target keyword
    keyword_count = words.count(target_keyword.lower())

    # Calculate keyword density
    keyword_density = (keyword_count / total_words) * 100 if total_words > 0 else 0

    return {
        "total_words": total_words,
        "keyword_count": keyword_count,
        "keyword_density": keyword_density,
    }


def analyze_seo(url, target_keyword=None):
    result = {
        "title": None,
        "meta_description": None,
        "headings": [],
        "images_without_alt": 0,
        "page_speed_ms": None,  # Page speed in milliseconds
        "ssl_certificate": False,
        "mobile_friendly": False,
        "robots_txt": False,
        "broken_links": 0,
        "favicon_present": False,
        "canonical_url": None,
        "hreflang_tags": [],
        "noindex_tag": False,
        "og_tags": {},
        "keyword_density": None,
    }

    try:
        # Start timer to measure page load time
        print(f"Starting SEO analysis for {url}")
        start_time = time.time()

        # Fetch the website content
        print("Fetching the page content...")
        response = requests.get(url, timeout=10)  # 10 seconds timeout
        print(f"Page loaded in {result['page_speed_ms']} milliseconds.")
        page_load_time = time.time() - start_time  # Calculate page speed in seconds

        soup = BeautifulSoup(response.content, "html.parser")
        print("Parsed the HTML content using BeautifulSoup.")

        # Keyword Density Check (if target keyword is provided)
        if target_keyword:
            keyword_data = calculate_keyword_density(response.text, target_keyword)
            result["keyword_density"] = keyword_data
        # Title tag
        title_tag = soup.find("title")
        result["title"] = title_tag.string if title_tag else "No title tag"

        # Meta description
        meta_description = soup.find("meta", attrs={"name": "description"})
        result["meta_description"] = (
            meta_description["content"] if meta_description else "No meta description"
        )

        # Heading tags (H1, H2, H3)
        for i in range(1, 4):
            headings = soup.find_all(f"h{i}")
            for heading in headings:
                result["headings"].append(heading.text)

        # Images without alt tags
        images = soup.find_all("img")
        for img in images:
            if not img.get("alt"):
                result["images_without_alt"] += 1

        # Page Speed (in milliseconds)
        result["page_speed_ms"] = round(
            page_load_time * 1000
        )  # Convert to milliseconds

        # Check SSL Certificate
        if urlparse(url).scheme == "https":
            result["ssl_certificate"] = (
                True  # Simple check for HTTPS (could be more advanced)
            )

        # Check for mobile-friendliness (responsive meta tag)
        viewport_meta = soup.find("meta", attrs={"name": "viewport"})
        if viewport_meta and "width=device-width" in viewport_meta.get("content", ""):
            result["mobile_friendly"] = True

        # Check robots.txt
        robots_url = f"{urlparse(url).scheme}://{urlparse(url).netloc}/robots.txt"
        robots_response = requests.get(robots_url)
        if robots_response.status_code == 200:
            result["robots_txt"] = True

        # Check for broken links
        links = soup.find_all("a", href=True)
        for link in links:
            href = link.get("href")
            if href.startswith("/"):  # Handle relative URLs
                href = f"{urlparse(url).scheme}://{urlparse(url).netloc}{href}"
            try:
                link_response = requests.get(href, timeout=5)
                if link_response.status_code != 200:
                    result["broken_links"] += 1
            except:
                result["broken_links"] += 1

        # Check for favicon
        favicon = soup.find("link", rel=lambda value: value and "icon" in value.lower())
        result["favicon_present"] = True if favicon else False

        # Check for canonical URL
        canonical = soup.find("link", rel="canonical")
        result["canonical_url"] = canonical["href"] if canonical else "No canonical tag"

        # Check for hreflang tags
        hreflang_tags = soup.find_all("link", rel="alternate", hreflang=True)
        result["hreflang_tags"] = [tag["hreflang"] for tag in hreflang_tags]

        # Check for noindex tag
        robots_meta = soup.find("meta", attrs={"name": "robots"})
        if robots_meta and "noindex" in robots_meta.get("content", ""):
            result["noindex_tag"] = True

        # Check for Open Graph (OG) tags
        og_tags = soup.find_all(
            "meta", property=lambda value: value and value.startswith("og:")
        )
        for og in og_tags:
            property_name = og.get("property")
            result["og_tags"][property_name] = og.get("content", "")

        # Simplified SEO scoring
        seo_score = 100
        if result["title"] == "No title tag":
            seo_score -= 20
        if result["meta_description"] == "No meta description":
            seo_score -= 15
        if len(result["headings"]) == 0:
            seo_score -= 10
        if result["images_without_alt"] > 0:
            seo_score -= result["images_without_alt"] * 2
        if result["page_speed_ms"] > 2000:  # Penalize if load time > 2000ms (2 seconds)
            seo_score -= 10
        if not result["ssl_certificate"]:
            seo_score -= 5
        if not result["mobile_friendly"]:
            seo_score -= 10
        if not result["robots_txt"]:
            seo_score -= 5
        if result["broken_links"] > 0:
            seo_score -= result["broken_links"] * 5  # Penalize heavily for broken links
        if not result["favicon_present"]:
            seo_score -= 2
        if not result["canonical_url"]:
            seo_score -= 3
        if len(result["hreflang_tags"]) == 0:
            seo_score -= 5
        if result["noindex_tag"]:
            seo_score -= 10

        return seo_score, result

    except Exception as e:
        return 0, {"error": str(e)}
