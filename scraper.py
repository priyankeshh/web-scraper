import os
import random
import time
import re
import json
from datetime import datetime
from typing import List, Dict, Type
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
import logging

import pandas as pd
from bs4 import BeautifulSoup
from pydantic import BaseModel, Field, create_model
import html2text
import tiktoken

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from openai import OpenAI
import google.generativeai as genai
from groq import Groq

import httpx
from urllib3.util.retry import Retry
from tenacity import retry, stop_after_attempt, wait_exponential

# Import all necessary constants first
from assets import (
    USER_AGENTS, 
    PRICING, 
    HEADLESS_OPTIONS, 
    SYSTEM_MESSAGE, 
    USER_MESSAGE, 
    LLAMA_MODEL_FULLNAME, 
    GROQ_LLAMA_MODEL_FULLNAME,
    PROGRESS_LOG_FILE,
    REQUEST_SETTINGS,
    MAX_WORKERS,
    RETRY_SETTINGS,
    RATE_LIMIT,
    Config
)

load_dotenv()

# Optional import for Playwright
try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("Playwright not installed. Dynamic content fetching will use Selenium fallback.")

# Configure logging after importing PROGRESS_LOG_FILE
logging.basicConfig(
    filename=PROGRESS_LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

class OptimizedScraper:
    def __init__(self):
        self.client = httpx.Client()
        self.retry_strategy = Retry(
            total=REQUEST_SETTINGS["max_retries"],
            backoff_factor=REQUEST_SETTINGS["backoff_factor"],
            status_forcelist=REQUEST_SETTINGS["status_forcelist"]
        )
        
    def fetch_with_retry(self, url):
        try:
            response = self.client.get(
                url, 
                timeout=REQUEST_SETTINGS["timeout"],
                follow_redirects=True
            )
            response.raise_for_status()
            return response.text
        except Exception as e:
            logging.error(f"Error fetching {url}: {str(e)}")
            raise

@lru_cache(maxsize=100)
@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def fetch_html_selenium(url: str) -> str:
    max_retries = RETRY_SETTINGS["max_retries"]
    base_delay = RETRY_SETTINGS["base_delay"]
    exponential_base = RETRY_SETTINGS["exponential_base"]
    
    for attempt in range(max_retries):
        try:
            driver = setup_selenium()
            driver.get(url)
            time.sleep(2)
            html = driver.page_source
            driver.quit()
            return html
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            delay = min(base_delay * (exponential_base ** attempt), RETRY_SETTINGS["max_delay"])
            time.sleep(delay)

def batch_scrape(urls: List[str], max_workers: int = MAX_WORKERS) -> List[str]:
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(fetch_html_selenium, urls))
    return results

def clean_memory():
    import gc
    gc.collect()

def get_random_proxy() -> str:
    PROXY_LIST = [
        "proxy1:port",
        "proxy2:port"
    ]
    return random.choice(PROXY_LIST)

def validate_content(html_content: str) -> str:
    if not html_content or len(html_content) < 100:
        raise ValueError("Invalid or empty content received")
    return html_content

def setup_selenium():
    options = Options()
    user_agent = random.choice(USER_AGENTS)
    options.add_argument(f"user-agent={user_agent}")
    
    for option in HEADLESS_OPTIONS:
        options.add_argument(option)
        
    service = Service(ChromeDriverManager().install())
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_page_load_timeout(Config.SELENIUM_TIMEOUT)
    return driver

def click_accept_cookies(driver):
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button | //a | //div"))
        )
        
        accept_text_variations = [
            "accept", "agree", "allow", "consent", "continue", "ok", "I agree", "got it"
        ]
        
        for tag in ["button", "a", "div"]:
            for text in accept_text_variations:
                try:
                    element = driver.find_element(By.XPATH, f"//{tag}[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{text}')]")
                    if element:
                        element.click()
                        print(f"Clicked the '{text}' button.")
                        return
                except:
                    continue

        print("No 'Accept Cookies' button found.")
    
    except Exception as e:
        print(f"Error finding 'Accept Cookies' button: {e}")

def fetch_dynamic_content(url):
    if (PLAYWRIGHT_AVAILABLE):
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page()
                page.goto(url, wait_until="networkidle")
                content = page.content()
                browser.close()
                return content
        except Exception as e:
            logging.error(f"Playwright error: {e}. Falling back to Selenium.")
            return fetch_html_selenium(url)
    else:
        return fetch_html_selenium(url)

def parallel_scrape(urls):
    results = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_url = {executor.submit(fetch_html_selenium, url): url for url in urls}
        
        with tqdm(total=len(urls), desc="Scraping Progress") as pbar:
            for future in concurrent.futures.as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    data = future.result()
                    results.append(data)
                except Exception as e:
                    logging.error(f"Error scraping {url}: {str(e)}")
                pbar.update(1)
    
    return results

def fetch_html_selenium(url):
    driver = setup_selenium()
    try:
        driver.get(url)
        
        time.sleep(1)
        driver.maximize_window()
        
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        html = driver.page_source
        return html
    finally:
        driver.quit()

def clean_html(html_content):
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        for element in soup.find_all(['script', 'style', 'iframe', 'header', 'footer']):
            element.decompose()
            
        for element in soup.find_all(class_=True):
            try:
                element.attrs['class'] = ' '.join(element.attrs['class'])
            except (KeyError, TypeError):
                continue
                
        return str(soup)
    except Exception as e:
        logging.error(f"Error cleaning HTML: {str(e)}")
        return html_content

def html_to_markdown_with_readability(html_content):
    cleaned_html = clean_html(html_content)  
    
    markdown_converter = html2text.HTML2Text()
    markdown_converter.ignore_links = False
    markdown_content = markdown_converter.handle(cleaned_html)
    
    return markdown_content

def save_raw_data(raw_data: str, timestamp: str | None = None, output_folder: str = 'output') -> tuple[str, str]:
    if timestamp is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    os.makedirs(output_folder, exist_ok=True)
    raw_output_path = os.path.join(output_folder, f'rawData_{timestamp}.md')
    
    with open(raw_output_path, 'w', encoding='utf-8') as f:
        f.write(raw_data)
    
    logging.info(f"Raw data saved to {raw_output_path}")
    return raw_output_path, timestamp

def remove_urls_from_file(file_path):
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    base, ext = os.path.splitext(file_path)
    new_file_path = f"{base}_cleaned{ext}"
    with open(file_path, 'r', encoding='utf-8') as file:
        markdown_content = file.read()
    cleaned_content = re.sub(url_pattern, '', markdown_content)
    with open(new_file_path, 'w', encoding='utf-8') as file:
        file.write(cleaned_content)
    print(f"Cleaned file saved as: {new_file_path}")
    return cleaned_content

def create_dynamic_listing_model(field_names: List[str]) -> Type[BaseModel]:
    field_definitions = {field: (str, ...) for field in field_names}
    return create_model('DynamicListingModel', **field_definitions)

def create_listings_container_model(listing_model: Type[BaseModel]) -> Type[BaseModel]:
    return create_model('DynamicListingsContainer', listings=(List[listing_model], ...))

def trim_to_token_limit(text, model, max_tokens=120000):
    encoder = tiktoken.encoding_for_model(model)
    tokens = encoder.encode(text)
    if len(tokens) > max_tokens:
        trimmed_text = encoder.decode(tokens[:max_tokens])
        return trimmed_text
    return text

def generate_system_message(listing_model: BaseModel) -> str:
    schema_info = listing_model.model_json_schema()
    field_descriptions = []
    for field_name, field_info in schema_info["properties"].items():
        field_type = field_info["type"]
        field_descriptions.append(f'"{field_name}": "{field_type}"')
    schema_structure = ",\n".join(field_descriptions)
    system_message = f"""
    You are an intelligent text extraction and conversion assistant. Your task is to extract structured information 
                        from the given text and convert it into a pure JSON format. The JSON should contain only the structured data extracted from the text, 
                        with no additional commentary, explanations, or extraneous information. 
                        You could encounter cases where you can't find the data of the fields you have to extract or the data will be in a foreign language.
                        Please process the following text and provide the output in pure JSON format with no words before or after the JSON:
    Please ensure the output strictly follows this schema:

    {{
        "listings": [
            {{
                {schema_structure}
            }}
        ]
    }} """
    return system_message

def format_data(data, DynamicListingsContainer, DynamicListingModel, selected_model):
    token_counts = {}
    
    if selected_model in ["gpt-4o-mini", "gpt-4o-2024-08-06"]:
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        completion = client.beta.chat.completions.parse(
            model=selected_model,
            messages=[
                {"role": "system", "content": SYSTEM_MESSAGE},
                {"role": "user", "content": USER_MESSAGE + data},
            ],
            response_format=DynamicListingsContainer
        )
        encoder = tiktoken.encoding_for_model(selected_model)
        input_token_count = len(encoder.encode(USER_MESSAGE + data))
        output_token_count = len(encoder.encode(json.dumps(completion.choices[0].message.parsed.dict())))
        token_counts = {
            "input_tokens": input_token_count,
            "output_tokens": output_token_count
        }
        return completion.choices[0].message.parsed, token_counts

    elif selected_model == "gemini-1.5-flash":
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        model = genai.GenerativeModel('gemini-1.5-flash',
                generation_config={
                    "response_mime_type": "application/json",
                    "response_schema": DynamicListingsContainer
                })
        prompt = SYSTEM_MESSAGE + "\n" + USER_MESSAGE + data
        input_tokens = model.count_tokens(prompt)
        completion = model.generate_content(prompt)
        usage_metadata = completion.usage_metadata
        token_counts = {
            "input_tokens": usage_metadata.prompt_token_count,
            "output_tokens": usage_metadata.candidates_token_count
        }
        return completion.text, token_counts
    
    elif selected_model == "Llama3.1 8B":
        sys_message = generate_system_message(DynamicListingModel)
        client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
        completion = client.chat.completions.create(
            model=LLAMA_MODEL_FULLNAME,
            messages=[
                {"role": "system", "content": sys_message},
                {"role": "user", "content": USER_MESSAGE + data}
            ],
            temperature=0.7,
            
        )
        response_content = completion.choices[0].message.content
        print(response_content)
        parsed_response = json.loads(response_content)
        token_counts = {
            "input_tokens": completion.usage.prompt_tokens,
            "output_tokens": completion.usage.completion_tokens
        }
        return parsed_response, token_counts
    elif selected_model== "Groq Llama3.1 70b":
        sys_message = generate_system_message(DynamicListingModel)
        client = Groq(api_key=os.environ.get("GROQ_API_KEY"),)
        completion = client.chat.completions.create(
        messages=[
            {"role": "system","content": sys_message},
            {"role": "user","content": USER_MESSAGE + data}
        ],
        model=GROQ_LLAMA_MODEL_FULLNAME,
    )
        response_content = completion.choices[0].message.content
        parsed_response = json.loads(response_content)
        token_counts = {
            "input_tokens": completion.usage.prompt_tokens,
            "output_tokens": completion.usage.completion_tokens
        }
        return parsed_response, token_counts
    else:
        raise ValueError(f"Unsupported model: {selected_model}")

def save_formatted_data(formatted_data, timestamp, output_folder='output'):
    os.makedirs(output_folder, exist_ok=True)
    if isinstance(formatted_data, str):
        try:
            formatted_data_dict = json.loads(formatted_data)
        except json.JSONDecodeError:
            raise ValueError("The provided formatted data is a string but not valid JSON.")
    else:
        formatted_data_dict = formatted_data.dict() if hasattr(formatted_data, 'dict') else formatted_data
    json_output_path = os.path.join(output_folder, f'sorted_data_{timestamp}.json')
    with open(json_output_path, 'w', encoding='utf-8') as f:
        json.dump(formatted_data_dict, f, indent=4)
    print(f"Formatted data saved to JSON at {json_output_path}")
    if isinstance(formatted_data_dict, dict):
        data_for_df = next(iter(formatted_data_dict.values())) if len(formatted_data_dict) == 1 else formatted_data_dict
    elif isinstance(formatted_data_dict, list):
        data_for_df = formatted_data_dict
    else:
        raise ValueError("Formatted data is neither a dictionary nor a list, cannot convert to DataFrame")
    try:
        df = pd.DataFrame(data_for_df)
        print("DataFrame created successfully.")
        excel_output_path = os.path.join(output_folder, f'sorted_data_{timestamp}.xlsx')
        df.to_excel(excel_output_path, index=False)
        print(f"Formatted data saved to Excel at {excel_output_path}")
        return df
    except Exception as e:
        print(f"Error creating DataFrame or saving Excel: {str(e)}")
        return None

def calculate_price(tokens_count: dict, model: str) -> tuple[float, float, float]:
    model_config = PRICING[model]
    input_cost = tokens_count['input_tokens'] * model_config.input_price
    output_cost = tokens_count['output_tokens'] * model_config.output_price
    total_cost = input_cost + output_cost
    return input_cost, output_cost, total_cost

if __name__ == "__main__":
    url = 'https://webscraper.io/test-sites/e-commerce/static'
    fields=['Name of item', 'Price']

    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        raw_html = fetch_html_selenium(url)
        markdown = html_to_markdown_with_readability(raw_html)
        save_raw_data(markdown, timestamp)
        DynamicListingModel = create_dynamic_listing_model(fields)
        DynamicListingsContainer = create_listings_container_model(DynamicListingModel)
        formatted_data, token_counts = format_data(markdown, DynamicListingsContainer,DynamicListingModel,"Groq Llama3.1 70b")
        print(formatted_data)
        save_formatted_data(formatted_data, timestamp)
        formatted_data_text = json.dumps(formatted_data.dict() if hasattr(formatted_data, 'dict') else formatted_data) 
        input_tokens, output_tokens, total_cost = calculate_price(token_counts, "Groq Llama3.1 70b")
        print(f"Input token count: {input_tokens}")
        print(f"Output token count: {output_tokens}")
        print(f"Estimated total cost: ${total_cost:.4f}")
    except Exception as e:
        print(f"An error occurred: {e}")
