"""
Example usage of the Research Assistant API.

This script demonstrates how to use the API programmatically.
Make sure the server is running (python main.py) before running this script.
"""

import requests
import json
from pathlib import Path


API_BASE_URL = "http://localhost:8000/api"


def analyze_url_example():
    """Example: Analyze an article from a URL."""
    print("\n" + "="*60)
    print("Example 1: Analyzing a URL")
    print("="*60)

    url = "https://en.wikipedia.org/wiki/Artificial_intelligence"

    print(f"\nAnalyzing: {url}")
    print("Please wait, this may take 30-60 seconds...")

    response = requests.post(
        f"{API_BASE_URL}/analyze/url",
        json={"url": url, "include_related": True}
    )

    if response.status_code == 200:
        data = response.json()
        print_results(data)
    else:
        print(f"Error: {response.status_code}")
        print(response.json())


def analyze_pdf_example(pdf_path: str):
    """Example: Analyze a PDF file."""
    print("\n" + "="*60)
    print("Example 2: Analyzing a PDF")
    print("="*60)

    if not Path(pdf_path).exists():
        print(f"\nPDF not found: {pdf_path}")
        print("Please provide a valid PDF file path.")
        return

    print(f"\nAnalyzing PDF: {pdf_path}")
    print("Please wait, this may take 30-60 seconds...")

    with open(pdf_path, 'rb') as f:
        files = {'file': (Path(pdf_path).name, f, 'application/pdf')}
        response = requests.post(
            f"{API_BASE_URL}/analyze/pdf",
            files=files
        )

    if response.status_code == 200:
        data = response.json()
        print_results(data)
    else:
        print(f"Error: {response.status_code}")
        print(response.json())


def health_check_example():
    """Example: Check API health."""
    print("\n" + "="*60)
    print("Example 3: Health Check")
    print("="*60)

    response = requests.get(f"{API_BASE_URL}/health")

    if response.status_code == 200:
        data = response.json()
        print(f"\nStatus: {data['status']}")
        print(f"Models Loaded: {data['models_loaded']}")
    else:
        print(f"Error: {response.status_code}")


def print_results(data: dict):
    """Pretty print analysis results."""
    print("\n" + "-"*60)
    print("RESULTS")
    print("-"*60)

    print(f"\nTitle: {data['title']}")
    print(f"Word Count: {data['word_count']}")
    print(f"Difficulty: {data['difficulty_level']}")
    print(f"Sentiment: {data['sentiment']} ({data['sentiment_score']:.2f})")

    print(f"\n📝 Summary:")
    print(f"  {data['summary']}")

    print(f"\n🏷️  Topics:")
    for topic in data['topics']:
        print(f"  - {topic}")

    print(f"\n🔍 Critical Analysis:")
    print(f"  {data['critical_analysis']}")

    if data['logical_gaps']:
        print(f"\n⚠️  Logical Gaps:")
        for gap in data['logical_gaps']:
            print(f"  - {gap}")

    if data['unsupported_claims']:
        print(f"\n❓ Unsupported Claims:")
        for claim in data['unsupported_claims']:
            print(f"  - {claim[:100]}...")

    print(f"\n💭 Follow-up Questions:")
    for question in data['follow_up_questions']:
        print(f"  - {question}")

    print(f"\n🔗 Related Topics:")
    for topic in data['related_topics']:
        print(f"  - {topic}")

    print("\n" + "-"*60)


def save_results_to_file(data: dict, filename: str = "analysis_result.json"):
    """Save analysis results to a JSON file."""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"\n✅ Results saved to: {filename}")


if __name__ == "__main__":
    print("Research Assistant API - Usage Examples")
    print("Make sure the server is running at http://localhost:8000")

    # Example 1: Health check
    health_check_example()

    # Example 2: Analyze a URL
    # Uncomment to run:
    # analyze_url_example()

    # Example 3: Analyze a PDF
    # Uncomment and provide your PDF path:
    # analyze_pdf_example("path/to/your/document.pdf")

    print("\n" + "="*60)
    print("Examples complete!")
    print("="*60)
    print("\nTo run the URL or PDF examples, uncomment them in the code.")
    print("For PDF analysis, provide a valid PDF file path.\n")
