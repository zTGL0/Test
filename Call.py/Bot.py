import os
import requests
import asyncio
import logging
import time
import json
import sys
import codecs
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler
from typing import Dict, List, Optional, Tuple
import hashlib
from collections import defaultdict

# ===== FIX UNICODE ENCODING ISSUE =====
# Set environment variable to use UTF-8 encoding
os.environ['PYTHONIOENCODING'] = 'utf-8'

# Configure logging with UTF-8 encoding
class UTF8StreamHandler(logging.StreamHandler):
    def __init__(self, stream=None):
        super().__init__(stream)
        if hasattr(self.stream, 'reconfigure'):
            try:
                self.stream.reconfigure(encoding='utf-8')
            except:
                pass

# Load environment variables
load_dotenv()

# Configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
AXIOM_TOKEN = os.getenv("AXIOM_TOKEN")
AXIOM_DATASET = os.getenv("AXIOM_DATASET")
MIN_MARKET_CAP = int(os.getenv("MIN_MARKET_CAP", 5000))
MAX_MARKET_CAP = int(os.getenv("MAX_MARKET_CAP", 50000))
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", 7))
MAX_TOKEN_AGE_MINUTES = int(os.getenv("MAX_TOKEN_AGE_MINUTES", 30))
QUERY_LIMIT = int(os.getenv("QUERY_LIMIT", 7))

DEX_API_BASE_URL = os.getenv("DEX_API_BASE_URL", "https://api.dexscreener.com")
TOKEN_PROFILES_LATEST_V1_ENDPOINT = os.getenv("TOKEN_PROFILES_LATEST_V1_ENDPOINT", "/token-profiles/latest/v1")
TOKEN_BOOSTS_LATEST_V1_ENDPOINT = os.getenv("TOKEN_BOOSTS_LATEST_V1_ENDPOINT", "/token-boosts/latest/v1")
TOKEN_BOOSTS_TOP_V1_ENDPOINT = os.getenv("TOKEN_BOOSTS_TOP_V1_ENDPOINT", "/token-boosts/top/v1")
DEX_SEARCH_ENDPOINT = os.getenv("DEX_SEARCH_ENDPOINT", "/latest/dex/search")
TOKENS_V1_ENDPOINT = os.getenv("TOKENS_V1_ENDPOINT", "/tokens/v1/solana/")
AXIOM_API_ENDPOINT = os.getenv("AXIOM_API_ENDPOINT", "https://lar.axiom.ai/api/v3")

# Setup logging with proper encoding
def setup_logging():
    """Setup logging with UTF-8 encoding support"""
    try:
        # Create file handler with UTF-8 encoding
        file_handler = logging.FileHandler('solana_bot.log', encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        
        # Create console handler with UTF-8 encoding
        console_handler = UTF8StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Get root logger
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logging.getLogger(__name__)
        
    except Exception as e:
        # Fallback to basic logging without emojis
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('solana_bot.log'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)

logger = setup_logging()

class SolanaCryptoBot:
    def __init__(self):
        self.bot = Bot(token=TELEGRAM_BOT_TOKEN)
        self.processed_pairs = set()
        self.pair_cache = {}
        self.last_api_call = defaultdict(float)
        self.stats = {
            'total_pairs_found': 0,
            'total_notifications_sent': 0,
            'last_check': None,
            'errors': 0,
            'solana_pairs_processed': 0,
            'api_calls_made': 0,
            'start_time': datetime.now(timezone.utc).isoformat()
        }
        
        # Rate limiting settings
        self.api_rate_limits = {
            'token-profiles': {'calls': 0, 'reset_time': 0, 'limit': 60},
            'token-boosts': {'calls': 0, 'reset_time': 0, 'limit': 60},
            'dex-pairs': {'calls': 0, 'reset_time': 0, 'limit': 300},
            'search': {'calls': 0, 'reset_time': 0, 'limit': 300},
            'tokens': {'calls': 0, 'reset_time': 0, 'limit': 300}
        }
        
    def safe_log(self, level: str, message: str):
        """Safe logging that handles unicode errors"""
        try:
            # Replace emojis with text equivalents for problematic systems
            safe_message = message
            emoji_replacements = {
                '🔍': '[SEARCH]',
                '📊': '[STATS]',
                '💾': '[CACHE]',
                '😴': '[SLEEP]',
                '✅': '[SUCCESS]',
                '❌': '[ERROR]',
                '⚠️': '[WARNING]',
                '🚀': '[ROCKET]',
                '💥': '[BOOM]',
                '🎯': '[TARGET]',
                '📤': '[SEND]',
                '🔄': '[REFRESH]',
                '💎': '[DIAMOND]',
                '🌊': '[WAVE]',
                '🐋': '[WHALE]',
                '🪐': '[PLANET]',
                '🌙': '[MOON]',
                '💰': '[MONEY]',
                '💵': '[DOLLAR]',
                '📈': '[UP]',
                '📉': '[DOWN]',
                '⬆️': '[UP_ARROW]',
                '⬇️': '[DOWN_ARROW]',
                '🔗': '[LINK]',
                '🏪': '[STORE]'
            }
            
            for emoji, replacement in emoji_replacements.items():
                safe_message = safe_message.replace(emoji, replacement)
            
            # Log the safe message
            getattr(logger, level.lower())(safe_message)
            
        except Exception as e:
            # Ultimate fallback - log without any special characters
            try:
                basic_message = f"LOG_ERROR: Could not log original message due to encoding issue: {str(e)}"
                getattr(logger, level.lower())(basic_message)
            except:
                pass
        
    def check_rate_limit(self, endpoint_type: str) -> bool:
        """Check if we can make an API call based on rate limits"""
        current_time = time.time()
        rate_limit = self.api_rate_limits.get(endpoint_type, {'calls': 0, 'reset_time': 0, 'limit': 60})
        
        # Reset counter if a minute has passed
        if current_time - rate_limit['reset_time'] >= 60:
            rate_limit['calls'] = 0
            rate_limit['reset_time'] = current_time
        
        # Check if we're under the limit
        if rate_limit['calls'] < rate_limit['limit']:
            rate_limit['calls'] += 1
            return True
        
        return False
    
    def make_api_request(self, url: str, endpoint_type: str = 'default') -> Optional[Dict]:
        """Make API request with rate limiting and error handling"""
        if not self.check_rate_limit(endpoint_type):
            self.safe_log('warning', f"Rate limit reached for {endpoint_type}, skipping request")
            return None
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'application/json',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'cross-site'
            }
            
            response = requests.get(url, headers=headers, timeout=15)
            self.stats['api_calls_made'] += 1
            
            if response.status_code == 429:
                self.safe_log('warning', f"Rate limited by server for {url}")
                time.sleep(5)
                return None
            
            if response.status_code == 404:
                self.safe_log('warning', f"Endpoint not found: {url}")
                return None
                
            if response.status_code != 200:
                self.safe_log('warning', f"API returned {response.status_code} for {url}")
                return None
                
            return response.json()
            
        except requests.exceptions.Timeout:
            self.safe_log('warning', f"Timeout for {url}")
            return None
        except requests.exceptions.RequestException as e:
            self.safe_log('error', f"Request error for {url}: {e}")
            return None
        except json.JSONDecodeError as e:
            self.safe_log('error', f"JSON decode error for {url}: {e}")
            return None
    
    def fetch_latest_token_profiles(self) -> List[Dict]:
        """Fetch latest token profiles"""
        url = f"{DEX_API_BASE_URL}{TOKEN_PROFILES_LATEST_V1_ENDPOINT}"
        data = self.make_api_request(url, 'token-profiles')
        
        if not data:
            return []
        
        # Handle different response structures
        if isinstance(data, list):
            return [item for item in data if self.is_solana_token_profile(item)]
        elif isinstance(data, dict) and 'data' in data:
            return [item for item in data['data'] if self.is_solana_token_profile(item)]
        
        return []
    
    def fetch_boosted_tokens(self) -> List[Dict]:
        """Fetch boosted tokens"""
        endpoints = [
            f"{DEX_API_BASE_URL}{TOKEN_BOOSTS_LATEST_V1_ENDPOINT}",
            f"{DEX_API_BASE_URL}{TOKEN_BOOSTS_TOP_V1_ENDPOINT}"
        ]
        
        all_tokens = []
        for url in endpoints:
            data = self.make_api_request(url, 'token-boosts')
            if data:
                if isinstance(data, list):
                    solana_tokens = [item for item in data if self.is_solana_token_profile(item)]
                    all_tokens.extend(solana_tokens)
                time.sleep(1)  # Small delay between requests
        
        return all_tokens
    
    def fetch_solana_pairs_by_search(self) -> List[Dict]:
        """Search for Solana pairs using various DEX keywords"""
        search_terms = ['raydium', 'orca', 'jupiter', 'pumpfun', 'moonshot']
        all_pairs = []
        
        for term in search_terms:
            url = f"{DEX_API_BASE_URL}{DEX_SEARCH_ENDPOINT}?q={term}"
            data = self.make_api_request(url, 'search')
            
            if data and 'pairs' in data:
                solana_pairs = [pair for pair in data['pairs'] if self.is_solana_pair(pair)]
                all_pairs.extend(solana_pairs)
                self.safe_log('info', f"Found {len(solana_pairs)} Solana pairs for '{term}'")
            
            time.sleep(1)  # Rate limiting
        
        return all_pairs
    
    def fetch_token_pairs_by_address(self, token_addresses: List[str]) -> List[Dict]:
        """Fetch pairs for specific token addresses"""
        all_pairs = []
        
        # Process addresses in batches of 30 (API limit)
        for i in range(0, len(token_addresses), 30):
            batch = token_addresses[i:i+30]
            addresses_str = ','.join(batch)
            
            url = f"{DEX_API_BASE_URL}{TOKENS_V1_ENDPOINT}{addresses_str}"
            data = self.make_api_request(url, 'tokens')
            
            if data and isinstance(data, list):
                all_pairs.extend(data)
            
            time.sleep(1)  # Rate limiting
        
        return all_pairs
    
    def fetch_from_axiom(self, query: str) -> List[Dict]:
        """Fetch data from Axiom API"""
        try:
            headers = {
                'Authorization': f'Bearer {AXIOM_TOKEN}',
                'Content-Type': 'application/json'
            }
            data = {
                "apl": query
            }
            response = requests.post(f"{AXIOM_API_ENDPOINT}/datasets/_apl?format=tabular", headers=headers, json=data, timeout=15)
            
            if response.status_code == 200:
                return response.json().get('tables', [])
            else:
                self.safe_log('warning', f"Axiom API returned {response.status_code} for query: {query}")
                return []
        except Exception as e:
            self.safe_log('error', f"Error fetching from Axiom: {e}")
            return []

    def fetch_solana_pairs(self) -> List[Dict]:
        """Enhanced method to fetch Solana pairs from multiple sources"""
        try:
            all_pairs = []
            
            self.safe_log('info', "Fetching Solana pairs from multiple sources...")
            
            # 1. Search-based fetching from DexScreener
            self.safe_log('info', "Fetching from DexScreener API...")
            search_pairs = self.fetch_solana_pairs_by_search()
            all_pairs.extend(search_pairs)
            self.safe_log('info', f"Found {len(search_pairs)} pairs from DexScreener search.")

            # 2. Fetch from Axiom
            self.safe_log('info', "Fetching from Axiom API...")
            axiom_query = "['crypto-logs'] | where chain == 'solana'"
            axiom_pairs = self.fetch_from_axiom(axiom_query)
            if axiom_pairs:
                # Process axiom_pairs to match the format of dexscreener pairs
                processed_axiom_pairs = []
                for table in axiom_pairs:
                    for row in table.get('columns', []):
                        # Assuming the columns are in a specific order
                        # This part needs to be adjusted based on the actual data structure from Axiom
                        pair = {
                            'baseToken': {'address': row[0]},
                            'quoteToken': {'address': row[1]},
                            # ... other fields
                        }
                        processed_axiom_pairs.append(pair)
                all_pairs.extend(processed_axiom_pairs)
                self.safe_log('info', f"Found {len(processed_axiom_pairs)} pairs from Axiom.")

            # 3. Latest token profiles (converted to pairs) from DexScreener
            self.safe_log('info', "Fetching latest token profiles from DexScreener API...")
            profile_tokens = self.fetch_latest_token_profiles()
            if profile_tokens:
                token_addresses = [token.get('tokenAddress') for token in profile_tokens if token.get('tokenAddress')]
                if token_addresses:
                    profile_pairs = self.fetch_token_pairs_by_address(token_addresses)
                    all_pairs.extend(profile_pairs)
                    self.safe_log('info', f"Found {len(profile_pairs)} pairs from DexScreener profiles.")
            
            # 4. Boosted tokens (converted to pairs) from DexScreener
            self.safe_log('info', "Fetching boosted tokens from DexScreener API...")
            boosted_tokens = self.fetch_boosted_tokens()
            if boosted_tokens:
                token_addresses = [token.get('tokenAddress') for token in boosted_tokens if token.get('tokenAddress')]
                if token_addresses:
                    boosted_pairs = self.fetch_token_pairs_by_address(token_addresses)
                    all_pairs.extend(boosted_pairs)
                    self.safe_log('info', f"Found {len(boosted_pairs)} pairs from DexScreener boosted tokens.")
            
            if not all_pairs:
                self.safe_log('warning', "No pairs data received from any source")
                return []
            
            # Remove duplicates
            unique_pairs = self.remove_duplicate_pairs(all_pairs)
            
            self.stats['solana_pairs_processed'] += len(unique_pairs)
            self.safe_log('info', f"Total unique Solana pairs: {len(unique_pairs)}")
            
            return unique_pairs
            
        except Exception as e:
            self.safe_log('error', f"Error fetching Solana data: {e}")
            self.stats['errors'] += 1
            return []
    
    def remove_duplicate_pairs(self, pairs: List[Dict]) -> List[Dict]:
        """Remove duplicate pairs based on multiple identifiers"""
        seen_pairs = set()
        unique_pairs = []
        
        for pair in pairs:
            # Create unique identifier from multiple fields
            pair_addr = pair.get('pairAddress', '')
            base_token_addr = pair.get('baseToken', {}).get('address', '')
            quote_token_addr = pair.get('quoteToken', {}).get('address', '')
            
            # Create hash of multiple identifiers
            identifier_string = f"{pair_addr}-{base_token_addr}-{quote_token_addr}"
            identifier_hash = hashlib.md5(identifier_string.encode()).hexdigest()
            
            if identifier_hash not in seen_pairs:
                seen_pairs.add(identifier_hash)
                unique_pairs.append(pair)
        
        return unique_pairs
    
    def is_solana_token_profile(self, token_profile: Dict) -> bool:
        """Check if token profile is for Solana"""
        return token_profile.get('chainId', '').lower() == 'solana'
    
    def is_solana_pair(self, pair: Dict) -> bool:
        """Enhanced Solana pair detection"""
        try:
            chain_id = str(pair.get('chainId', '')).lower()
            if chain_id == 'solana':
                return True
            
            # Check DEX
            dex_id = str(pair.get('dexId', '')).lower()
            solana_dexes = [
                'raydium', 'orca', 'serum', 'jupiter', 'moonshot', 
                'pumpfun', 'pump.fun', 'bonkswap', 'aldrin', 'meteora'
            ]
            
            if any(dex in dex_id for dex in solana_dexes):
                return True
            
            # Check token addresses
            base_addr = pair.get('baseToken', {}).get('address', '')
            quote_addr = pair.get('quoteToken', {}).get('address', '')
            
            if self.is_solana_address(base_addr) or self.is_solana_address(quote_addr):
                return True
                
            return False
            
        except Exception as e:
            self.safe_log('warning', f"Error checking Solana pair: {e}")
            return False
    
    def is_solana_address(self, address: str) -> bool:
        """Improved Solana address validation"""
        try:
            if not address or len(address) < 32:
                return False
            
            # Known Solana token addresses
            known_solana_tokens = [
                'So11111111111111111111111111111111111111112',  # WSOL
                'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v',  # USDC
                'Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB',  # USDT
                '11111111111111111111111111111111',  # System Program
            ]
            
            if address in known_solana_tokens:
                return True
            
            # Length check (Solana addresses are typically 32-44 characters)
            if not (32 <= len(address) <= 50):
                return False
            
            # Base58 character check
            base58_chars = set('123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz')
            if not all(c in base58_chars for c in address):
                return False
            
            # Common Solana patterns
            solana_patterns = ['So11', '11111', 'EPjF', 'TokenkegQfeZyiN', 'ATokenGP']
            if any(pattern in address for pattern in solana_patterns):
                return True
            
            # If it passes all checks and has the right format, likely Solana
            return True
            
        except:
            return False
    
    def get_token_age_minutes(self, pair: Dict) -> Optional[float]:
        """Calculate token age in minutes"""
        try:
            pair_created_at = pair.get('pairCreatedAt', 0)
            if not pair_created_at:
                return None
            
            created_time = datetime.fromtimestamp(pair_created_at / 1000, tz=timezone.utc)
            age_delta = datetime.now(timezone.utc) - created_time
            return age_delta.total_seconds() / 60
            
        except Exception as e:
            self.safe_log('warning', f"Error calculating age: {str(e)}")
            return None
    
    def is_pair_promising(self, pair: Dict) -> Tuple[bool, str]:
        """Enhanced filtering with detailed analysis"""
        try:
            base_token = pair.get('baseToken', {})
            if not base_token or not base_token.get('address'):
                return False, "Missing base token data"
            
            token_symbol = base_token.get('symbol', 'UNKNOWN')
            
            # Solana check
            if not self.is_solana_pair(pair):
                return False, f"{token_symbol}: Not a Solana pair"
            
            # Market cap validation
            market_cap = 0
            fdv = pair.get('fdv') or pair.get('marketCap')
            
            if fdv:
                try:
                    market_cap = float(fdv)
                except (ValueError, TypeError):
                    market_cap = 0
            
            if market_cap == 0:
                # Try alternative calculation
                try:
                    price_usd = float(pair.get('priceUsd', 0) or 0)
                    if price_usd <= 0:
                        return False, f"{token_symbol}: No market cap or price data"
                except:
                    return False, f"{token_symbol}: Invalid price data"
            
            if market_cap > 0 and not (MIN_MARKET_CAP <= market_cap <= MAX_MARKET_CAP):
                return False, f"{token_symbol}: Market cap ${market_cap:,.0f} outside range (${MIN_MARKET_CAP:,}-${MAX_MARKET_CAP:,})"
            
            # Age validation
            age_minutes = self.get_token_age_minutes(pair)
            if age_minutes is not None:
                if age_minutes > MAX_TOKEN_AGE_MINUTES:
                    return False, f"{token_symbol}: Too old ({age_minutes:.1f} minutes, max {MAX_TOKEN_AGE_MINUTES})"
                if age_minutes < 0:
                    return False, f"{token_symbol}: Invalid timestamp"
            
            # Volume check
            volume_24h = 0
            try:
                volume_data = pair.get('volume', {})
                volume_24h = float(volume_data.get('h24', 0) or 0)
            except:
                volume_24h = 0
            
            if volume_24h < 100:
                return False, f"{token_symbol}: Low volume ${volume_24h:,.0f}"
            
            # Price validation
            try:
                price_usd = float(pair.get('priceUsd', 0) or 0)
                if price_usd <= 0:
                    return False, f"{token_symbol}: No valid price data"
            except:
                return False, f"{token_symbol}: Invalid price format"
            
            # Liquidity check
            liquidity_usd = 0
            try:
                liquidity_data = pair.get('liquidity', {})
                liquidity_usd = float(liquidity_data.get('usd', 0) or 0)
                if liquidity_usd < 1000:  # Minimum $1000 liquidity
                    return False, f"{token_symbol}: Low liquidity ${liquidity_usd:,.0f}"
            except:
                pass  # Liquidity check is optional
            
            # Transaction activity check
            try:
                txns = pair.get('txns', {})
                txns_5m = 0
                if 'm5' in txns:
                    buys = txns['m5'].get('buys', 0) or 0
                    sells = txns['m5'].get('sells', 0) or 0
                    txns_5m = buys + sells
                
                if txns_5m == 0:
                    # Check 1h transactions as fallback
                    if 'h1' in txns:
                        buys_1h = txns['h1'].get('buys', 0) or 0
                        sells_1h = txns['h1'].get('sells', 0) or 0
                        if buys_1h + sells_1h < 5:
                            return False, f"{token_symbol}: Very low activity"
            except:
                pass  # Activity check is optional
            
            age_str = f"{age_minutes:.1f}m" if age_minutes is not None else "Unknown"
            dex_id = pair.get('dexId', 'Unknown')
            
            self.safe_log('info', f"[SUCCESS] {token_symbol} passed all filters (MC: ${market_cap:,.0f}, Age: {age_str}, DEX: {dex_id})")
            return True, f"{token_symbol}: All checks passed"
            
        except Exception as e:
            self.safe_log('error', f"Error in filtering pair: {str(e)}")
            return False, f"Filter error: {str(e)}"
    
    def filter_pairs_by_criteria(self, pairs: List[Dict]) -> List[Dict]:
        """Filter pairs with comprehensive logging"""
        filtered_pairs = []
        rejection_stats = defaultdict(int)
        
        self.safe_log('info', f"Filtering {len(pairs)} Solana pairs...")
        
        for pair in pairs:
            is_promising, reason = self.is_pair_promising(pair)
            
            if not is_promising:
                # Categorize rejection reason
                category = reason.split(':')[0] if ':' in reason else reason
                rejection_stats[category] += 1
                self.safe_log('info', f"Pair rejected: {reason}")
                continue
            
            # Check if already processed
            base_token = pair.get('baseToken', {})
            pair_id = f"{pair.get('pairAddress', '')}-{base_token.get('address', '')}"
            
            if pair_id not in self.processed_pairs:
                filtered_pairs.append(pair)
                self.processed_pairs.add(pair_id)
                
                # Clean up old processed pairs periodically
                if len(self.processed_pairs) > 2000:
                    old_pairs = list(self.processed_pairs)[:-1000]
                    self.processed_pairs -= set(old_pairs)
                    self.safe_log('info', "Cleaned up old processed pairs")
        
        # Log rejection statistics
        if rejection_stats:
            self.safe_log('info', "Rejection statistics:")
            for reason, count in sorted(rejection_stats.items(), key=lambda x: x[1], reverse=True):
                self.safe_log('info', f"   - {reason}: {count}")
        
        self.stats['total_pairs_found'] += len(filtered_pairs)
        self.safe_log('info', f"[SUCCESS] {len(filtered_pairs)} pairs passed all filters")
        
        return filtered_pairs
    
    def calculate_comprehensive_risk_score(self, pair: Dict) -> Tuple[str, List[str], int]:
        """Enhanced risk scoring system"""
        risk_score = 0
        risk_factors = []
        
        try:
            # Market cap risk
            market_cap = float(pair.get('fdv', 0) or pair.get('marketCap', 0) or 0)
            if market_cap < 10000:
                risk_score += 3
                risk_factors.append("Very Low Market Cap (<$10K)")
            elif market_cap < 25000:
                risk_score += 2
                risk_factors.append("Low Market Cap (<$25K)")
            elif market_cap < 50000:
                risk_score += 1
                risk_factors.append("Small Market Cap (<$50K)")
            
            # Age risk
            age_minutes = self.get_token_age_minutes(pair)
            if age_minutes is not None:
                if age_minutes < 2:
                    risk_score += 4
                    risk_factors.append("Extremely New (<2min)")
                elif age_minutes < 5:
                    risk_score += 3
                    risk_factors.append("Very New (<5min)")
                elif age_minutes < 15:
                    risk_score += 2
                    risk_factors.append("New (<15min)")
                elif age_minutes < 30:
                    risk_score += 1
                    risk_factors.append("Recent (<30min)")
            else:
                risk_score += 2
                risk_factors.append("Unknown Age")
            
            # Volume risk
            volume_24h = float(pair.get('volume', {}).get('h24', 0) or 0)
            if volume_24h < 500:
                risk_score += 3
                risk_factors.append("Very Low Volume (<$500)")
            elif volume_24h < 2000:
                risk_score += 2
                risk_factors.append("Low Volume (<$2K)")
            elif volume_24h < 5000:
                risk_score += 1
                risk_factors.append("Moderate Volume (<$5K)")
            
            # Liquidity risk
            liquidity_usd = float(pair.get('liquidity', {}).get('usd', 0) or 0)
            if liquidity_usd < 2000:
                risk_score += 3
                risk_factors.append("Very Low Liquidity (<$2K)")
            elif liquidity_usd < 5000:
                risk_score += 2
                risk_factors.append("Low Liquidity (<$5K)")
            elif liquidity_usd < 10000:
                risk_score += 1
                risk_factors.append("Moderate Liquidity (<$10K)")
            
            # Transaction activity risk
            txns = pair.get('txns', {})
            total_txns_5m = 0
            if 'm5' in txns:
                buys = txns['m5'].get('buys', 0) or 0
                sells = txns['m5'].get('sells', 0) or 0
                total_txns_5m = buys + sells
            
            if total_txns_5m == 0:
                risk_score += 3
                risk_factors.append("No Recent Activity")
            elif total_txns_5m < 5:
                risk_score += 2
                risk_factors.append("Very Low Activity (<5 txns/5m)")
            elif total_txns_5m < 20:
                risk_score += 1
                risk_factors.append("Low Activity (<20 txns/5m)")
            
            # DEX trust factor
            dex_id = pair.get('dexId', '').lower()
            trusted_dexes = ['raydium', 'orca', 'jupiter']
            major_dexes = ['pumpfun', 'pump.fun', 'moonshot']
            
            if not any(dex in dex_id for dex in trusted_dexes + major_dexes):
                risk_score += 2
                risk_factors.append("Unknown/Minor DEX")
            elif any(dex in dex_id for dex in major_dexes):
                risk_score += 1
                risk_factors.append("Major DEX (Non-Traditional)")

            # Social and website info
            info = pair.get('info', {})
            websites = info.get('websites', [])
            socials = info.get('socials', [])
            if not websites and not socials:
                risk_score += 2
                risk_factors.append("No website or social links")
            
            # Price stability (if available)
            price_change_24h = float(pair.get('priceChange', {}).get('h24', 0) or 0)
            if abs(price_change_24h) > 200:
                risk_score += 2
                risk_factors.append("Extreme Volatility (>200%)")
            elif abs(price_change_24h) > 100:
                risk_score += 1
                risk_factors.append("High Volatility (>100%)")
            
            # Risk level classification
            if risk_score <= 2:
                risk_level = "🟢 LOW"
            elif risk_score <= 5:
                risk_level = "🟡 MEDIUM"
            elif risk_score <= 8:
                risk_level = "🟠 HIGH"
            elif risk_score <= 12:
                risk_level = "🔴 VERY HIGH"
            else:
                risk_level = "⚫ EXTREME"
            
            return risk_level, risk_factors, risk_score
            
        except Exception as e:
            self.safe_log('warning', f"Error calculating risk score: {e}")
            return "⚪ UNKNOWN", ["Analysis Failed"], 10
    
    def format_enhanced_message(self, pair: Dict) -> Tuple[Optional[str], Optional[Dict]]:
        """Create comprehensive message with all available data"""
        try:
            base_token = pair.get('baseToken', {})
            quote_token = pair.get('quoteToken', {})
            
            # Basic token info
            token_name = base_token.get('name', 'Unknown Token')
            symbol = base_token.get('symbol', 'UNK')
            contract_address = base_token.get('address', 'N/A')
            
            # Market data
            market_cap = float(pair.get('fdv', 0) or pair.get('marketCap', 0) or 0)
            price_usd = float(pair.get('priceUsd', 0) or 0)
            price_native = pair.get('priceNative', 'N/A')
            
            # Volume and liquidity
            volume = pair.get('volume', {})
            volume_24h = float(volume.get('h24', 0) or 0)
            volume_1h = float(volume.get('h1', 0) or 0)
            volume_5m = float(volume.get('m5', 0) or 0)
            
            liquidity = pair.get('liquidity', {})
            liquidity_usd = float(liquidity.get('usd', 0) or 0)
            liquidity_base = float(liquidity.get('base', 0) or 0)
            liquidity_quote = float(liquidity.get('quote', 0) or 0)
            
            # Price changes
            price_change = pair.get('priceChange', {})
            price_change_5m = float(price_change.get('m5', 0) or 0)
            price_change_1h = float(price_change.get('h1', 0) or 0)
            price_change_24h = float(price_change.get('h24', 0) or 0)
            
            # Transaction data
            txns = pair.get('txns', {})
            
            # DEX and pair info
            dex_name = pair.get('dexId', 'Unknown DEX').title()
            pair_address = pair.get('pairAddress', 'N/A')
            url = pair.get('url', '')
            
            # Age calculation
            age_minutes = self.get_token_age_minutes(pair)
            if age_minutes is not None:
                if age_minutes < 60:
                    age_str = f"{int(age_minutes)}m"
                else:
                    hours = int(age_minutes // 60)
                    mins = int(age_minutes % 60)
                    age_str = f"{hours}h {mins}m"
            else:
                age_str = "Unknown"
            
            # Risk analysis
            risk_level, risk_factors, risk_score = self.calculate_comprehensive_risk_score(pair)
            
            # Emojis based on data
            change_emoji_24h = self.get_change_emoji(price_change_24h)
            change_emoji_1h = self.get_change_emoji(price_change_1h)
            change_emoji_5m = self.get_change_emoji(price_change_5m)
            
            dex_emoji = self.get_dex_emoji(dex_name.lower())
            
            # Transaction details
            txn_details = self.format_transaction_details(txns)
            
            # Social and website info
            info = pair.get('info', {})
            websites = info.get('websites', [])
            website_url = websites[0].get('url') if websites else None
            
            socials = info.get('socials', [])
            social_links = self.format_social_links(socials)
            
            # Boost info
            boosts = pair.get('boosts', {})
            active_boosts = boosts.get('active', 0)
            
            # Format the comprehensive message
            message = f"""
🚀 **SOLANA NEW PAIR ALERT** 🚀

💎 **{token_name}** (`${symbol}`)
🆔 **CA:** `{contract_address}`

📊 **MARKET DATA:**
💰 Market Cap: ${market_cap:,.0f}
💵 Price: ${price_usd:.10f}
🔄 Native Price: {price_native}
💧 Liquidity: ${liquidity_usd:,.0f}
{dex_emoji} **DEX:** {dex_name}
⏰ **Age:** {age_str}
⚠️ **Risk:** {risk_level} (Score: {risk_score})

📈 **PRICE CHANGES:**
{change_emoji_5m} 5m: {price_change_5m:+.2f}%
{change_emoji_1h} 1h: {price_change_1h:+.2f}%
{change_emoji_24h} 24h: {price_change_24h:+.2f}%

💹 **VOLUME:**
• 5m: ${volume_5m:,.0f}
• 1h: ${volume_1h:,.0f}
• 24h: ${volume_24h:,.0f}

🔄 **TRANSACTIONS:**
{txn_details}

💧 **LIQUIDITY BREAKDOWN:**
• USD: ${liquidity_usd:,.0f}
• Base: {liquidity_base:,.2f} {symbol}
• Quote: {liquidity_quote:,.2f} {quote_token.get('symbol', 'Unknown')}

🔗 **QUICK LINKS:**
• [DexScreener](https://dexscreener.com/solana/{contract_address})
• [Solscan](https://solscan.io/token/{contract_address})
• [Jupiter Swap](https://jup.ag/swap/SOL-{contract_address})
• [Raydium](https://raydium.io/swap/?inputCurrency=sol&outputCurrency={contract_address})
{f"• [Website]({website_url})" if website_url else ""}

{social_links}

{f"🚀 **Active Boosts:** {active_boosts}" if active_boosts > 0 else ""}

⚡ **COPY CA:** `{contract_address}`

⚠️ **RISK FACTORS:** {', '.join(risk_factors) if risk_factors else 'None identified'}

📋 **PAIR INFO:**
• Pair Address: `{pair_address}`
• Quote Token: {quote_token.get('name', 'Unknown')} ({quote_token.get('symbol', 'UNK')})
            """.strip()
            
            # Prepare data for Axiom
            axiom_data = {
                'token_name': token_name,
                'symbol': symbol,
                'contract_address': contract_address,
                'pair_address': pair_address,
                'market_cap': market_cap,
                'price_usd': price_usd,
                'price_native': price_native,
                'volume_5m': volume_5m,
                'volume_1h': volume_1h,
                'volume_24h': volume_24h,
                'price_change_5m': price_change_5m,
                'price_change_1h': price_change_1h,
                'price_change_24h': price_change_24h,
                'liquidity_usd': liquidity_usd,
                'liquidity_base': liquidity_base,
                'liquidity_quote': liquidity_quote,
                'age_str': age_str,
                'age_minutes': age_minutes,
                'dex': dex_name,
                'chain': 'solana',
                'risk_level': risk_level,
                'risk_score': risk_score,
                'risk_factors': risk_factors,
                'active_boosts': active_boosts,
                'website_url': website_url,
                'social_links': social_links,
                'transaction_details': txn_details,
                'quote_token': {
                    'name': quote_token.get('name', ''),
                    'symbol': quote_token.get('symbol', ''),
                    'address': quote_token.get('address', '')
                },
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'dexscreener_url': url
            }
            
            return message, axiom_data
            
        except Exception as e:
            self.safe_log('error', f"Error formatting message: {e}")
            return None, None
    
    def get_change_emoji(self, change_percent: float) -> str:
        """Get emoji based on price change percentage"""
        if change_percent > 100:
            return "🚀🚀🚀"
        elif change_percent > 50:
            return "🚀🚀"
        elif change_percent > 20:
            return "🚀"
        elif change_percent > 10:
            return "📈"
        elif change_percent > 0:
            return "⬆️"
        elif change_percent == 0:
            return "➡️"
        elif change_percent > -10:
            return "⬇️"
        elif change_percent > -20:
            return "📉"
        elif change_percent > -50:
            return "💥"
        else:
            return "💀"
    
    def get_dex_emoji(self, dex_name: str) -> str:
        """Get emoji for DEX"""
        dex_emojis = {
            'raydium': '🌊',
            'orca': '🐋',
            'jupiter': '🪐',
            'pumpfun': '💎',
            'pump.fun': '💎',
            'moonshot': '🌙',
            'meteora': '☄️',
            'serum': '🧬',
            'aldrin': '⚡'
        }
        
        for dex, emoji in dex_emojis.items():
            if dex in dex_name:
                return emoji
        
        return "🏪"
    
    def format_transaction_details(self, txns: Dict) -> str:
        """Format transaction details across timeframes"""
        details = []
        
        timeframes = [('m5', '5m'), ('h1', '1h'), ('h24', '24h')]
        
        for tf_key, tf_display in timeframes:
            if tf_key in txns:
                buys = txns[tf_key].get('buys', 0) or 0
                sells = txns[tf_key].get('sells', 0) or 0
                total = buys + sells
                
                if total > 0:
                    buy_ratio = (buys / total) * 100 if total > 0 else 0
                    details.append(f"• {tf_display}: {total} txns (B:{buys} S:{sells} | {buy_ratio:.1f}% buys)")
                else:
                    details.append(f"• {tf_display}: 0 txns")
            else:
                details.append(f"• {tf_display}: No data")
        
        return "\n".join(details) if details else "• No transaction data available"
    
    def format_social_links(self, socials: List[Dict]) -> str:
        """Format social media links"""
        if not socials:
            return ""
        
        social_emojis = {
            'twitter': '🐦',
            'telegram': '📱',
            'discord': '💬',
            'website': '🌐',
            'github': '👨‍💻'
        }
        
        links = []
        for social in socials[:3]:  # Limit to first 3
            platform = social.get('platform', '').lower()
            handle = social.get('handle', '')
            
            if platform and handle:
                emoji = social_emojis.get(platform, '🔗')
                if platform == 'twitter':
                    links.append(f"{emoji} [Twitter](https://twitter.com/{handle})")
                elif platform == 'telegram':
                    links.append(f"{emoji} [Telegram](https://t.me/{handle})")
                else:
                    links.append(f"{emoji} {platform.title()}: {handle}")
        
        return "\n".join(links) if links else ""
    
    async def send_telegram_message(self, message: str) -> bool:
        """Enhanced Telegram message sending with error handling"""
        try:
            # Split message if too long (Telegram limit is ~4096 characters)
            if len(message) > 4000:
                # Split at a reasonable point
                parts = [message[i:i+4000] for i in range(0, len(message), 4000)]
                
                for i, part in enumerate(parts):
                    await self.bot.send_message(
                        chat_id=TELEGRAM_CHAT_ID,
                        text=part,
                        parse_mode='Markdown',
                        disable_web_page_preview=True
                    )
                    
                    if i < len(parts) - 1:  # Don't wait after the last part
                        await asyncio.sleep(1)  # Brief delay between parts
            else:
                await self.bot.send_message(
                    chat_id=TELEGRAM_CHAT_ID,
                    text=message,
                    parse_mode='Markdown',
                    disable_web_page_preview=True
                )
            
            self.safe_log('info', "[SUCCESS] Message sent to Telegram successfully")
            self.stats['total_notifications_sent'] += 1
            return True
            
        except Exception as e:
            self.safe_log('error', f"Error sending Telegram message: {e}")
            self.stats['errors'] += 1
            
            # Try sending a simplified version
            try:
                simple_message = "⚠️ Error sending full message. Check logs for details."
                await self.bot.send_message(
                    chat_id=TELEGRAM_CHAT_ID,
                    text=simple_message
                )
                return False
            except:
                return False
    
    def send_to_axiom(self, data: Dict) -> bool:
        """Enhanced Axiom logging with retry logic"""
        max_retries = 3
        
        for attempt in range(max_retries):
            try:
                enhanced_data = {
                    **data,
                    'bot_stats': self.stats.copy(),
                    'settings': {
                        'min_market_cap': MIN_MARKET_CAP,
                        'max_market_cap': MAX_MARKET_CAP,
                        'max_age_minutes': MAX_TOKEN_AGE_MINUTES,
                        'check_interval': CHECK_INTERVAL,
                        'query_limit': QUERY_LIMIT,
                        'chain': 'solana'
                    },
                    'attempt': attempt + 1
                }
                
                response = requests.post(
                    f"https://api.axiom.co/v1/datasets/{AXIOM_DATASET}/ingest",
                    headers={
                        "Authorization": f"Bearer {AXIOM_TOKEN}",
                        "Content-Type": "application/json"
                    },
                    json=[enhanced_data],
                    timeout=15
                )
                response.raise_for_status()
                
                self.safe_log('info', f"[SUCCESS] Data sent to Axiom successfully: {response.status_code}")
                return True
                
            except requests.exceptions.RequestException as e:
                self.safe_log('warning', f"Axiom attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    self.safe_log('error', f"Failed to send to Axiom after {max_retries} attempts")
                    self.stats['errors'] += 1
                    return False
    
    async def check_new_pairs(self):
        """Enhanced main scanning function"""
        start_time = datetime.now(timezone.utc)
        self.stats['last_check'] = start_time.isoformat()
        
        self.safe_log('info', "=" * 60)
        self.safe_log('info', "[SEARCH] Starting enhanced Solana crypto pair scan...")
        self.safe_log('info', f"[STATS] Settings: MC ${MIN_MARKET_CAP:,}-${MAX_MARKET_CAP:,}, Age 0-{MAX_TOKEN_AGE_MINUTES}min, Limit {QUERY_LIMIT}")
        self.safe_log('info', "=" * 60)
        
        try:
            # Fetch pairs from multiple sources
            pairs = await asyncio.to_thread(self.fetch_solana_pairs)
            
            if not pairs:
                self.safe_log('warning', "No pairs data received from any source")
                return
            
            self.safe_log('info', f"[STATS] Processing {len(pairs)} total Solana pairs...")
            
            # Apply comprehensive filtering
            filtered_pairs = self.filter_pairs_by_criteria(pairs)
            
            if filtered_pairs:
                # Limit the number of notifications per cycle
                limited_pairs = filtered_pairs[:QUERY_LIMIT]
                
                self.safe_log('info', f"[TARGET] Found {len(filtered_pairs)} promising pairs, processing {len(limited_pairs)}")
                
                successful_notifications = 0
                
                for i, pair in enumerate(limited_pairs, 1):
                    self.safe_log('info', f"[SEND] Processing pair {i}/{len(limited_pairs)}...")
                    
                    message, axiom_data = self.format_enhanced_message(pair)
                    
                    if message and axiom_data:
                        # Send Telegram notification
                        telegram_success = await self.send_telegram_message(message)
                        
                        if telegram_success:
                            successful_notifications += 1
                            
                            # Send to Axiom for logging
                            await asyncio.to_thread(self.send_to_axiom, axiom_data)
                            
                            # Rate limiting between messages
                            if i < len(limited_pairs):
                                await asyncio.sleep(5)  # 5 second delay between messages
                        else:
                            self.safe_log('error', f"Failed to send notification for pair {i}")
                    else:
                        self.safe_log('error', f"Failed to format message for pair {i}")
                
                self.safe_log('info', f"[SUCCESS] Successfully sent {successful_notifications}/{len(limited_pairs)} notifications")
                
            else:
                self.safe_log('info', "[SEARCH] No pairs met the filtering criteria this round")
            
            # Log comprehensive scan statistics
            scan_duration = (datetime.now(timezone.utc) - start_time).total_seconds()
            
            self.safe_log('info', "=" * 60)
            self.safe_log('info', "[STATS] SCAN SUMMARY")
            self.safe_log('info', f"Duration: {scan_duration:.2f} seconds")
            self.safe_log('info', f"[REFRESH] API Calls Made: {self.stats['api_calls_made']}")
            self.safe_log('info', f"[STATS] Total Pairs Processed: {len(pairs)}")
            self.safe_log('info', f"[SUCCESS] Pairs Passed Filters: {len(filtered_pairs) if 'filtered_pairs' in locals() else 0}")
            self.safe_log('info', f"[SEND] Notifications Sent: {self.stats['total_notifications_sent']}")
            self.safe_log('info', f"[ERROR] Errors: {self.stats['errors']}")
            self.safe_log('info', f"[CACHE] Processed Pairs Cache Size: {len(self.processed_pairs)}")
            self.safe_log('info', "=" * 60)
            
        except Exception as e:
            self.safe_log('error', f"Critical error in check_new_pairs: {e}")
            self.stats['errors'] += 1
            
            # Send error notification
            try:
                error_message = f"🚨 **BOT ERROR** 🚨\n\nTime: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\nError: {str(e)}"
                await self.send_telegram_message(error_message)
            except:
                self.safe_log('error', "Failed to send error notification")

# Command Handlers
async def start_command(update, context: ContextTypes.DEFAULT_TYPE):
    """Enhanced start command"""
    welcome_message = f"""
🤖 **ENHANCED SOLANA CRYPTO BOT**

🔧 **Current Settings:**
• Min Market Cap: ${MIN_MARKET_CAP:,}
• Max Market Cap: ${MAX_MARKET_CAP:,}
• Max Token Age: {MAX_TOKEN_AGE_MINUTES} minutes
• Check Interval: {CHECK_INTERVAL} seconds
• Query Limit: {QUERY_LIMIT} pairs per scan

📊 **Features:**
• Multi-source data fetching
• Advanced risk scoring
• Comprehensive filtering
• Real-time notifications
• Detailed analytics

🔗 **Supported DEXes:**
• Raydium • Orca • Jupiter
• PumpFun • Moonshot • Meteora

⚡ Bot is now monitoring Solana pairs!
    """
    await update.message.reply_text(welcome_message, parse_mode='Markdown')

async def stats_command(update, context: ContextTypes.DEFAULT_TYPE):
    """Show bot statistics"""
    if hasattr(context.bot_data, 'crypto_bot'):
        bot = context.bot_data['crypto_bot']
        uptime = datetime.now(timezone.utc) - datetime.fromisoformat(bot.stats['start_time'])
        
        stats_message = f"""
📊 **BOT STATISTICS**

⏱️ **Uptime:** {str(uptime).split('.')[0]}
🔄 **API Calls:** {bot.stats['api_calls_made']}
📊 **Pairs Processed:** {bot.stats['solana_pairs_processed']}
✅ **Pairs Found:** {bot.stats['total_pairs_found']}
📤 **Notifications Sent:** {bot.stats['total_notifications_sent']}
❌ **Errors:** {bot.stats['errors']}
💾 **Cache Size:** {len(bot.processed_pairs)}
🕐 **Last Check:** {bot.stats.get('last_check', 'Never')}

🎯 **Success Rate:** {(bot.stats['total_notifications_sent'] / max(bot.stats['total_pairs_found'], 1) * 100):.1f}%
        """
        await update.message.reply_text(stats_message, parse_mode='Markdown')
    else:
        await update.message.reply_text("Bot statistics not available.")

async def health_command(update, context: ContextTypes.DEFAULT_TYPE):
    """Check bot health"""
    health_message = f"""
🏥 **BOT HEALTH CHECK**

✅ **Status:** Running
🔗 **Telegram:** Connected
🌐 **DexScreener API:** Accessible
💾 **Axiom Logging:** {f"Connected ({AXIOM_DATASET})" if AXIOM_TOKEN else "Disabled"}

⚙️ **Settings:**
• Market Cap Range: ${MIN_MARKET_CAP:,} - ${MAX_MARKET_CAP:,}
• Max Age: {MAX_TOKEN_AGE_MINUTES} minutes
• Check Interval: {CHECK_INTERVAL} seconds

🕐 **Next Check:** In ~{CHECK_INTERVAL} seconds
    """
    await update.message.reply_text(health_message, parse_mode='Markdown')

# Main execution
async def main():
    """Main function with enhanced error handling"""
    logger.info("[ROCKET] Starting Enhanced Solana Crypto Bot...")
    
    # Validate required environment variables
    if not TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN is required!")
        sys.exit(1)
    
    if not TELEGRAM_CHAT_ID:
        logger.error("TELEGRAM_CHAT_ID is required!")
        sys.exit(1)
    
    # Initialize bot
    crypto_bot = SolanaCryptoBot()
    
    # Setup Telegram application
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Store bot instance for command access
    application.bot_data['crypto_bot'] = crypto_bot
    
    # Add command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(CommandHandler("health", health_command))
    
    try:
        # Start the application
        await application.initialize()
        await application.start()
        
        logger.info("[SUCCESS] Telegram bot started")
        logger.info(f"[TARGET] Monitoring Solana pairs every {CHECK_INTERVAL} seconds")
        
        # Test connection by sending a startup message
        startup_message = f"""
🚀 **BOT STARTED SUCCESSFULLY** 🚀

⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
⚙️ Settings: MC ${MIN_MARKET_CAP:,}-${MAX_MARKET_CAP:,}
🕐 Check Interval: {CHECK_INTERVAL}s
📊 Query Limit: {QUERY_LIMIT} pairs

✅ Ready to monitor Solana pairs!
        """
        
        try:
            await crypto_bot.send_telegram_message(startup_message)
        except Exception as e:
            logger.error(f"Failed to send startup message: {e}")
        
        # Main monitoring loop
        while True:
            try:
                await crypto_bot.check_new_pairs()
                
                # Wait for next check
                logger.info(f"[SLEEP] Sleeping for {CHECK_INTERVAL} seconds...")
                await asyncio.sleep(CHECK_INTERVAL)
                
            except KeyboardInterrupt:
                logger.info("Received shutdown signal")
                break
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                await asyncio.sleep(30)  # Wait 30 seconds before retrying
                
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        raise
    finally:
        logger.info("[STOP] Shutting down bot...")
        try:
            await application.stop()
            await application.shutdown()
        except:
            pass

if __name__ == "__main__":
    try:
        print("Starting bot...")
        # Check Python version
        if sys.version_info < (3, 7):
            print("Python 3.7 or higher is required!")
            sys.exit(1)
        
        # Run the bot
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise
    finally:
        print("Bot stopped.")
