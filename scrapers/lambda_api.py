import json
import requests

FIRECRAWL_API_KEY= ""

#Analysis
def compliance_checker(structured_data):

    print("Report Generation")
    
    OPENAI_API_KEY = ""
    website_content = structured_data['content']
    
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"  # Replace with your actual API key
    }

    prompt = f"""
       You are a finance compliance officer with expertise in identifying compliance lapses according to a provided rulebook. Your task is to analyze the given website content and flag any instances of non-compliance with the rules outlined in the rulebook.

        First, carefully review the following rulebook:
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

        Now, review the following website content:
            <website_content>
            {website_content}
            </website_content>

        #Instructions:
        1. Thorough Reading:
        - Carefully read the website content and the rulebook in detail.

        2. Line-by-Line Compliance Check:
        - For each rule in the rulebook, verify compliance by checking the website content line by line.
        - Identify any instances of non-compliance for each rule.

        3. Detailed Analysis:
        - Provide a detailed analysis for each rule.
        - Clearly specify whether the website content complies with the rule.
        - Highlight specific instances of non-compliance, if any, and explain why they violate the rule.

        4. Solutions and Recommendations:
        - After completing the analysis for all rules, propose actionable solutions to address identified compliance lapses.

        Requirements for the Output:

        1. Markdown Report:
        - The final output should be a well-structured markdown report.
        - The report must include:
            a. A section for each rule with:
                - Rule Name
                - Compliance Status (Compliant/Non-Compliant)
                - Detailed Analysis
                - Specific Examples (if applicable)
            b. A section for proposed solutions and recommendations

        2. Strict Adherence:
        - Base your analysis solely on the rulebook and website content provided.
        - Do not add, assume, or hallucinate information that is not explicitly stated or implied in the given materials.

        3. Clear and Concise Language:
        - Use precise and unambiguous language to avoid misinterpretation.

        Example Output Structure:
        # Compliance Analysis Report

        ## Rule 1: [Rule Name]
        - **Compliance Status**: Compliant/Non-Compliant
        - **Analysis**:
        - [Detailed explanation of the compliance or non-compliance issue]
        - [Specific examples from website content, if applicable]

        ## Rule 2: [Rule Name]
        - **Compliance Status**: Compliant/Non-Compliant
        - **Analysis**:
        - [Detailed explanation of the compliance or non-compliance issue]
        - [Specific examples from website content, if applicable]

        ...

        ## Solutions and Recommendations
        - [Actionable steps to address non-compliance issues]
        - [Suggestions for ensuring ongoing compliance in the future]

        Please provide your compliance analysis report following this structure, ensuring a comprehensive, accurate, and actionable compliance analysis.
        
    """

    data = {
        "model": "gpt-4o",
        "messages": [
            {"role": "user", "content": prompt},
          ],
        "temperature": 0.4
    }

    response = requests.post(url, headers=headers, json=data)
    response = response.json()

    final_response = response['choices'][0]['message']['content']

    print(final_response)

    return final_response

# Scrape the link to analysis
def compliance_officer(link):

    #Extract content from this link using Firecrawl to scrape

    url = "https://api.firecrawl.dev/v1/scrape"

    headers = {
        "Authorization": f"Bearer {FIRECRAWL_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "url": link,
        "formats": ["markdown"],
        "onlyMainContent": True,
        "timeout": 10000,
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

    return compliance_checker(structured_data)

def lambda_handler(event, context):

    # Extract URL from the API request
    url = event['queryStringParameters']['url']
    print(url)

    try:
        return compliance_officer(url)

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)}),
            'headers': {
                'Content-Type': 'application/json'
            }
        }
