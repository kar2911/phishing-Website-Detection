# feature_extractor.py
import re
from urllib.parse import urlparse
from datetime import datetime
import whois
import requests
from bs4 import BeautifulSoup
from difflib import SequenceMatcher
import joblib
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
FEATURE_COLUMNS = joblib.load(BASE_DIR / "feature_columns.pkl")


def extract_features_from_url(url):
    """Extracts features from a given URL and its content."""
    features = {}
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, timeout=10, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        path = parsed_url.path

        # --- URL-Based Features ---
        features['url_len'] = len(url)
        features['domain_len'] = len(domain)
        features['path_len'] = len(path)
        features['num_subdomains'] = domain.count('.')
        features['num_digits'] = sum(c.isdigit() for c in url)
        features['num_special_chars'] = len(re.findall(r'[@_!#$%^&*()<>?/\\|}{~:]', url))
        features['has_ip_in_domain'] = 1 if re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', domain) else 0
        features['is_https'] = 1 if parsed_url.scheme == 'https' else 0

        # --- Aliases for compatibility ---
        features['URLLength'] = features['url_len']
        features['DomainLength'] = features['domain_len']
        features['IsDomainIP'] = features['has_ip_in_domain']
        features['NoOfSubDomain'] = features['num_subdomains']
        features['IsHTTPS'] = features['is_https']
        features['NoOfDegitsInURL'] = features['num_digits']  # preserving typo

        # --- Advanced URL Features ---
        features['TLDLength'] = len(parsed_url.netloc.split('.')[-1])
        features['HasObfuscation'] = 1 if '%' in url else 0
        features['NoOfObfuscatedChar'] = url.count('%')
        features['ObfuscationRatio'] = features['NoOfObfuscatedChar'] / len(url) if len(url) > 0 else 0
        features['NoOfLettersInURL'] = sum(c.isalpha() for c in url)
        features['LetterRatioInURL'] = features['NoOfLettersInURL'] / len(url) if len(url) > 0 else 0
        features['DegitRatioInURL'] = features['num_digits'] / len(url) if len(url) > 0 else 0  # preserving typo
        features['NoOfEqualsInURL'] = url.count('=')
        features['NoOfQMarkInURL'] = url.count('?')
        features['NoOfAmpersandInURL'] = url.count('&')
        features['NoOfOtherSpecialCharsInURL'] = len(re.findall(r'[^a-zA-Z0-9@._\-]', url))
        features['SpacialCharRatioInURL'] = features['NoOfOtherSpecialCharsInURL'] / len(url) if len(url) > 0 else 0

        # --- Content-Based Features ---
        features['num_iframes'] = len(soup.find_all('iframe'))
        features['has_password_field'] = 1 if soup.find('input', {'type': 'password'}) else 0
        features['has_submit_button'] = 1 if soup.find('input', {'type': 'submit'}) else 0
        features['num_js_tags'] = len(soup.find_all('script'))
        features['num_css_links'] = len(soup.find_all('link', {'rel': 'stylesheet'}))
        title_tag = soup.title
        title = title_tag.string.strip() if title_tag and title_tag.string else ''
        features['domain_title_match_score'] = SequenceMatcher(None, domain, title).ratio()
        features['HasTitle'] = 1 if title_tag else 0
        features['DomainTitleMatchScore'] = features['domain_title_match_score']
        features['URLTitleMatchScore'] = SequenceMatcher(None, url, title).ratio()
        features['HasFavicon'] = 1 if soup.find('link', {'rel': ['icon', 'shortcut icon']}) else 0
        features['IsResponsive'] = 1 if soup.find('meta', {'name': 'viewport'}) else 0
        features['HasDescription'] = 1 if soup.find('meta', {'name': 'description'}) else 0
        features['HasHiddenFields'] = 1 if soup.find('input', {'type': 'hidden'}) else 0
        features['NoOfImage'] = len(soup.find_all('img'))
        features['NoOfiFrame'] = features['num_iframes']
        features['NoOfCSS'] = features['num_css_links']
        features['NoOfJS'] = features['num_js_tags']
        features['HasSubmitButton'] = features['has_submit_button']
        features['HasPasswordField'] = features['has_password_field']

        # Check for external form submits
        forms = soup.find_all('form')
        features['HasExternalFormSubmit'] = 0
        for form in forms:
            action = form.get('action', '')
            if action and not action.startswith('/') and domain not in action:
                features['HasExternalFormSubmit'] = 1
                break

        # Check for social network links
        social_keywords = ['facebook.com', 'twitter.com', 'instagram.com', 'linkedin.com', 'youtube.com']
        features['HasSocialNet'] = 0
        for link in soup.find_all('a', href=True):
            if any(kw in link['href'] for kw in social_keywords):
                features['HasSocialNet'] = 1
                break

        # Keyword-based features
        text_content = soup.get_text().lower()
        url_lower = url.lower()
        features['Bank'] = 1 if 'bank' in url_lower or 'bank' in text_content else 0
        features['Pay'] = 1 if 'pay' in url_lower or 'pay' in text_content else 0
        crypto_keywords = ['crypto', 'bitcoin', 'ethereum', 'wallet', 'binance']
        features['Crypto'] = 1 if any(kw in url_lower or kw in text_content for kw in crypto_keywords) else 0
        features['HasCopyrightInfo'] = 1 if 'copyright' in text_content or '©' in text_content else 0

        # Count self, empty, external links
        features['NoOfSelfRef'] = 0
        features['NoOfEmptyRef'] = 0
        features['NoOfExternalRef'] = 0
        for link in soup.find_all('a', href=True):
            href = link['href']
            if href in ['#', 'javascript:void(0)', '']:
                features['NoOfEmptyRef'] += 1
            elif href.startswith('/') or domain in href:
                features['NoOfSelfRef'] += 1
            else:
                features['NoOfExternalRef'] += 1

        # --- HTML Structure Features ---
        html_text = response.text
        lines = html_text.splitlines()
        features['LineOfCode'] = len(lines)
        features['LargestLineLength'] = max(len(line) for line in lines) if lines else 0

        # --- Redirect Features ---
        features['NoOfURLRedirect'] = len(response.history)
        features['NoOfSelfRedirect'] = sum(1 for r in response.history if domain in r.url)

        # --- WHOIS Features ---
        try:
            w = whois.whois(domain)
            if w.creation_date:
                creation_date = w.creation_date[0] if isinstance(w.creation_date, list) else w.creation_date
                features['domain_age_days'] = (datetime.now() - creation_date).days
            else:
                features['domain_age_days'] = 0
            features['whois_privacy'] = 1 if 'REDACTED FOR PRIVACY' in str(w) or 'Privacy' in str(w) else 0
        except Exception:
            features['domain_age_days'] = 0
            features['whois_privacy'] = 1

        # ✅ Return in the correct order
        return [features.get(col, 0) for col in FEATURE_COLUMNS]

    except Exception as e:
        print(f"Error processing {url}: {e}")
        return [0] * len(FEATURE_COLUMNS)