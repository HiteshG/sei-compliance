import requests
import time
from pydantic import BaseModel
from typing import List
import json

OPENAI_API_KEY = ""
AGENTQL_API_KEY = ""
FIRECRAWL_API_KEY = ""

url = "https://api.openai.com/v1/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {OPENAI_API_KEY}"  # Replace with your actual API key
}

# Analysis
def compliance_checker(structured_data):

    # Get the content of the url
    website_content = structured_data['content']

    # Use of tools to get the desired output format
    tools = {
        "type": "json_schema",
        "json_schema": {
            "name": "report",
            "description": "Create compliance report for the website url",
            "strict": False,
            "schema": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "summary": {
                        "type": "string",
                        "description": "Summary of the report for the user"
                    },
                    "solutions": {
                        "type": "string",
                        "description": "Solution steps to take when non-complaince is found"
                    },
                    "compliance_report": {
                        "type": "object",
                        "description" : "Check for each rule based on rulebook",
                        "additionalProperties": False,
                        "properties": {
                            "rule": {
                                "type": "string",
                                "description": "The compliance rule being evaluated"
                            },
                            "flag": {
                                "type": "string",
                                "description": "Whether the website content is compliant to the rule or not"
                            },
                            "reason": {
                                "type": "string",
                                "description": "If 'No' or 'Partially', provide details of the non-compliance."
                            }  
                        },
                        "required": ["rule", "flag", "reason"]
                    }
                },
            "required": ["compliance_report", "summary", "solution"]
            }
        }
    }

    # GPT Prompt for indetifying and then reporting
    
    prompt = f"""
       You are an expert finance compliance officer tasked with identifying compliance lapses according to a provided rulebook. Your job is to flag whether the given website content complies with the rules in the rulebook.

        First, carefully read the following website content:

        <website_content>
        {website_content}
        </website_content>

        Now, thoroughly review the following rulebook:

        <rulebook>
        1. Terminology Guidelines
            Approved Terms:
            These terms can be used in marketing, product descriptions, and communication:
            Money Management Account or Money Management Solution
            Cash Management Account or Cash Management Solution
            [Your Brand] Account
            Financial Services
            Financial Account
            Financial Product
            Financial Service Product
            Store of Funds
            Wallet or Open-Loop Wallet
            Stored-Value Account
            Open-Loop Stored-Value Account
            Prepaid Access Account
            Eligible for FDIC “Pass-Through” Insurance
            Funds held at [Partner Bank], Member FDIC
            Avoid:
            These terms are reserved for regulated financial institutions and should not be used in communication:
            Stripe or [Your Brand] Bank
            Bank Account
            Bank Balance
            Banking
            Banking Account
            Banking Product
            Banking Platform
            Deposits
            Mobile Banking
            [Your Brand] Pays Interest
            [Your Brand] Sets Interest Rates
            [Your Brand] Advances Funds
            Any phrases implying banking services, e.g., “Create a [Bank Partner] bank account” or “Mobile banking with [Bank Partner]”

        2. Yield Compliance
            Use:
            Always refer to yield and not interest in any marketing, product descriptions, or customer communications.
            Clearly disclose that yield is subject to change and explain under what conditions the yield may change.
            Always provide the most recent yield percentage on the dashboard for existing customers.
            Avoid:
            Do not refer to yield as interest.
            Avoid using the Fed Funds Rate as a benchmark for setting yield.
            Do not imply the yield is pass-through interest from a bank partner.

        3. FDIC Insurance Eligibility
            Overview:
            Stripe Treasury balances are stored-value accounts held for the benefit of the user at partner banks, such as Evolve Bank & Trust and Goldman Sachs Bank USA. FDIC insurance is available only under specific conditions for these accounts.
            Approved Terminology for FDIC Insurance:
            Use the following phrases when discussing FDIC insurance eligibility:
            Eligible for FDIC Insurance
            FDIC Insurance-Eligible Accounts
            Eligible for FDIC Pass-Through Insurance
            Eligible for FDIC Insurance up to $250K
            Eligible for FDIC Insurance up to the standard maximum deposit insurance per depositor in the same capacity
            Avoid:
            FDIC Insured or FDIC Insured Accounts
            FDIC Pass-Through Insurance Guaranteed
            Any phrasing that suggests direct FDIC insurance coverage for Stripe or your platform.
            Required Disclosures:
            When referencing FDIC eligibility, always include the following disclosures:
            Stripe Treasury accounts are eligible for FDIC pass-through insurance, subject to specific conditions.
            FDIC insurance is only available up to $250,000 per depositor, per financial institution, and only if the requirements for pass-through insurance are met.
            Neither Stripe nor your platform are FDIC-insured institutions.
            FDIC insurance protects against bank failure, not fraud or financial loss.

        4. Key Compliance Disclosures
            Yield Disclosure:
            Always include the statement that yield percentages are subject to change and that customers will be notified when changes occur. Include a disclaimer stating that yield is not interest.
            FDIC Insurance Disclosure:
            Always mention that Stripe Treasury accounts are eligible for FDIC pass-through insurance if the requirements are met.
            Ensure the disclosure includes the FDICs coverage limit of $250,000 per depositor per institution and that it applies only in the event of bank failure.
            Inform users that Stripe or your platform are not FDIC-insured institutions and that FDIC coverage applies only to depository institutions.

        5. Best Practices for Marketing and Content
            Clarity:
            Use clear, precise language to avoid confusion between Stripe Treasury products and actual banking services.
            Do not suggest users are receiving banking services directly from Stripe or its partners.
            Make sure that "FDIC Insurance" and "yield" are clearly defined and distinguished from banking terms.
            Consistency:
            Use approved terminology consistently across all touchpoints: website content, emails, FAQs, advertising, and user agreements.
            Regular Updates:
            Ensure that all marketing and customer-facing content is regularly updated to reflect any changes in the yield percentage or FDIC eligibility.
            Notification of Changes:
            Notify users when their yield percentage changes and display the updated yield information prominently on their dashboards.

        6. Frequently Asked Questions (FAQs)
            Is FDIC insurance impacted if a customer holds deposits in other accounts with the same institution?
            Yes, if a user holds other accounts with the same institution, FDIC insurance may aggregate the balances to determine eligibility. FDIC does not aggregate personal and business accounts.
            Does FDIC insurance protect from fraud or financial loss?
            No, FDIC insurance only applies in the event of bank failure. It does not cover fraud or other financial losses.
            How can I confirm if FDIC pass-through insurance is applicable?
            Stripe Treasury accounts are designed to meet FDIC pass-through insurance requirements. However, the FDIC makes the final determination based on specific criteria during a bank's failure.
        </rulebook>

        #Instructions:
        1. Read the website content very carefully and diligently.
        2. For each rule from rulebook, check line by line whether there is any non-compliant issue for the rule.
        3. For each rule, If 'No', provide details of the non-compliance. If 'Yes', leave empty.
        4. After analyzing all rules, provide a conclusion and steps for solutions.
        
        Remember to base your analysis solely on the provided rulebook and website content.Do not invent or hallucinate any information not present in the text.
        Remember to stick strictly to the information provided in the text. Do not add any information that is not explicitly stated or clearly implied in the given content."
    """


    data = {
        "model": "gpt-4o",
        "messages": [
            {"role": "user", "content": prompt},
          ],
        "temperature": 0.2,
        "response_format": tools
    }

    response = requests.post(url, headers=headers, json=data)
    response = response.json()

    final_response = response['choices'][0]['message']['content']

    print(final_response)

    return final_response

# Scrape the single url and get the analysis done
def compliance_officer(link):

    #Extract content from this link using firecrawl/tinyFish to scrape

    # url = "https://api.agentql.com/v1/query-data"
    # headers = {
    #     "X-API-Key": AGENTQL_API_KEY ,
    #     "Content-Type": "application/json"
    # }
    # data = {
    #     "url": link,
    #     "query": "{ website_content }"
    # }

    url = "https://api.firecrawl.dev/v1/scrape"

    headers = {
        "Authorization": f"Bearer {FIRECRAWL_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "url": link,
        "formats": ["markdown"],
        "onlyMainContent": True,
        "timeout": 30000,
        "removeBase64Images": True
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    data = response.json()
                    
    if not data.get('success') or not data.get('data'):
        print(f"No content returned from Firecrawl for {url}")
        return None

    # Extract content from Firecrawl response
    content_data = data['data']
    
    # Structure the content
    structured_data = {
        "content": content_data.get('markdown', ''),
        "url": url,
    }

    # Call to GPT for indentifying and analysis
    structured_data['report'] = compliance_checker(structured_data)

    return structured_data

# Report Generator
def compliance_report(all_links):

    complete_report = []

    # Loop over all the links
    for i, link in enumerate(all_links):
        print(f"{i}. {link}")
        link_report = compliance_officer(link)
        complete_report.append(link_report)

    ## Here we could have call the GPT again to create a complete comprehensive report.
    return complete_report

# Map all the links and pass to scrape them 
def website_crawler(website_url: str):
  
    print("Inside function")
    """Find all the links using Firecrawl's map endpoint and then pass to GPT-4o to analysis"""
        
    # Normalize the URL
    if not website_url.startswith(('http://', 'https://')):
        website_url = 'https://' + website_url
        
    print(f"\nStarting crawl of {website_url}")
    print("This may take a few minutes...")

    try:
        # Step 1: Use Firecrawl's map endpoint to get ALL website links

        url = "https://api.firecrawl.dev/v1/map"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {FIRECRAWL_API_KEY}"
        }

        # Data payload can set limit of scraping
        params = {
            "url": website_url,
            'includeSubdomains': False,
            'limit': 10,
        }

        # POST request
        map_result = requests.post(url, headers=headers, json=params)

        map_result = map_result.json()
        # Output the response
        if not map_result or 'links' not in map_result:
            print("No links found in website map")
            return []

        all_links = map_result['links']
        print(f"\nFound {len(all_links)} total links")
        
        # # Step 2: Let GPT analyze all links and identify compliance policy
        time.sleep(5)
        case_studies = compliance_report(all_links)
        return case_studies

    except Exception as e:
        print(f"Error crawling website {website_url}: {str(e)}")
        return f"Error crawling website {website_url}: {str(e)}"

def main():
    """Main entry point for the complaince analyzer"""

    report = website_crawler("https://mercury.com/")
    
    return report

if __name__ == "__main__":
    main()
