#!/usr/bin/env python3
"""
Demo script for Product Analytics feature
Shows how the new product-specific analytics work
"""

from src.sentiment_analyzer import SentimentAnalyzer
from src.product_catalog import ProductCatalog
from src.data_manager import DataManager
from datetime import datetime
import random


def create_sample_product_feedback():
    """Create sample feedback for different products to demo analytics"""
    print("🎤 Creating Sample Product Feedback for Analytics Demo")
    print("=" * 60)

    analyzer = SentimentAnalyzer()
    catalog = ProductCatalog()
    data_manager = DataManager()

    # Sample feedback for different products
    sample_feedback = {
        "prod_001": [  # Wireless Bluetooth Headphones
            "Amazing sound quality! Love these headphones.",
            "Great noise cancellation, perfect for work.",
            "Battery life could be better, but overall good.",
            "Excellent build quality and comfort.",
            "Best headphones I've ever owned!",
        ],
        "prod_002": [  # Smartphone Case
            "Perfect fit for my phone, great protection.",
            "Case is okay, nothing special.",
            "Dropped my phone multiple times, case saved it!",
            "Good value for money.",
        ],
        "prod_003": [  # Coffee Maker
            "Makes terrible coffee, very disappointed.",
            "Broke after just one week of use.",
            "Coffee tastes great, easy to use.",
            "Good coffee maker for the price.",
        ],
        "prod_004": [  # Running Shoes
            "Super comfortable for long runs!",
            "Great cushioning and support.",
            "Perfect fit, highly recommend.",
            "Best running shoes ever!",
        ],
        "prod_005": [  # Laptop Stand
            "Improved my posture significantly.",
            "Sturdy and adjustable, great quality.",
            "Perfect height for my setup.",
        ],
    }

    products = catalog.get_products()

    for product_id, feedbacks in sample_feedback.items():
        product_name = products[product_id]["name"]
        print(f"\n📝 Adding feedback for {product_name}:")

        for i, feedback_text in enumerate(feedbacks):
            # Analyze sentiment
            analysis = analyzer.analyze_sentiment(feedback_text)

            # Create feedback data with slight time variations
            base_time = datetime.now()
            time_offset = random.randint(-7, 0)  # Last 7 days
            timestamp = base_time.replace(day=base_time.day + time_offset)

            feedback_data = {
                "product_id": product_id,
                "product_name": product_name,
                "feedback_text": feedback_text,
                "input_method": random.choice(["Text Input", "Voice Recording"]),
                "timestamp": timestamp.isoformat(),
                "sentiment_analysis": analysis,
            }

            # Save feedback
            success = data_manager.save_feedback(feedback_data)
            sentiment_label = (
                "Positive"
                if analysis["overall_sentiment"] > 0.1
                else "Negative" if analysis["overall_sentiment"] < -0.1 else "Neutral"
            )
            print(
                f"  ✅ {sentiment_label} ({analysis['overall_sentiment']:.3f}): \"{feedback_text[:50]}...\""
            )

    print(f"\n🎉 Sample feedback created successfully!")
    print("\nNow you can:")
    print("1. Run the app: streamlit run app.py")
    print("2. Go to 'Product Catalog'")
    print("3. Click 'View Analytics' on any product")
    print("4. Explore product-specific sentiment analysis!")


def show_analytics_preview():
    """Show a preview of what the analytics will look like"""
    print("\n📊 Analytics Preview")
    print("=" * 30)

    data_manager = DataManager()
    catalog = ProductCatalog()
    products = catalog.get_products()

    for product_id, product in list(products.items())[:3]:  # Show first 3 products
        feedback = data_manager.get_feedback_by_product(product_id)
        if feedback:
            avg_sentiment = sum(f["overall_sentiment"] for f in feedback) / len(
                feedback
            )
            sentiment_label = (
                "Positive"
                if avg_sentiment > 0.1
                else "Negative" if avg_sentiment < -0.1 else "Neutral"
            )

            print(f"\n🛍️  {product['name']}")
            print(f"   📊 {len(feedback)} reviews")
            print(f"   💭 Average sentiment: {avg_sentiment:.3f} ({sentiment_label})")
            print(
                f"   📈 Analytics available: Sentiment trends, confidence analysis, comparisons"
            )


def main():
    """Main demo function"""
    try:
        create_sample_product_feedback()
        show_analytics_preview()

        print("\n" + "=" * 60)
        print("🎯 Product Analytics Feature Demo Complete!")
        print("=" * 60)
        print("\n🚀 Key Features Added:")
        print("  ✅ Product-specific analytics pages")
        print("  ✅ Clickable 'View Analytics' buttons in catalog")
        print("  ✅ Sentiment trends over time")
        print("  ✅ Confidence vs sentiment analysis")
        print("  ✅ Product comparison charts")
        print("  ✅ Recent reviews display")
        print("  ✅ Export product-specific data")
        print("  ✅ Quick feedback submission")

        print("\n📱 How to Use:")
        print("  1. Browse products in 'Product Catalog'")
        print("  2. See review summaries on each product card")
        print("  3. Click 'View Analytics' for detailed insights")
        print("  4. Navigate back using the sidebar button")

    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
