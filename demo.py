#!/usr/bin/env python3
"""
Demo script for Voice Sentiment Analyzer
Shows basic functionality without the web interface
"""

from src.sentiment_analyzer import SentimentAnalyzer
from src.product_catalog import ProductCatalog
from src.data_manager import DataManager


def demo_sentiment_analysis():
    """Demonstrate sentiment analysis functionality"""
    print("🎤 Voice Sentiment Analyzer - Demo")
    print("=" * 50)

    # Initialize analyzer
    analyzer = SentimentAnalyzer()

    # Test cases
    test_cases = [
        "This product is absolutely amazing! I love it so much!",
        "The quality is terrible and I'm very disappointed.",
        "It's okay, nothing special but does the job.",
        "Fast delivery and great customer service. Highly recommend!",
        "Overpriced and poor quality. Would not buy again.",
        "Perfect for my needs. Exactly what I was looking for.",
    ]

    print("\n📊 Sentiment Analysis Results:")
    print("-" * 50)

    for i, text in enumerate(test_cases, 1):
        result = analyzer.analyze_sentiment(text)

        sentiment_label = analyzer.get_sentiment_label(result["overall_sentiment"])
        intensity = analyzer.get_intensity_label(result["overall_sentiment"])

        print(f"\n{i}. Text: \"{text[:50]}{'...' if len(text) > 50 else ''}\"")
        print(
            f"   Overall Sentiment: {result['overall_sentiment']:.3f} ({sentiment_label} - {intensity})"
        )
        print(f"   Confidence: {result['confidence']:.1%}")
        print(
            f"   Models: TextBlob={result['textblob_sentiment']:.3f}, "
            f"VADER={result['vader_sentiment']:.3f}, "
            f"Keywords={result['keyword_sentiment']:.3f}"
        )


def demo_product_catalog():
    """Demonstrate product catalog functionality"""
    print("\n\n🛍️ Product Catalog Demo")
    print("=" * 50)

    catalog = ProductCatalog()
    products = catalog.get_products()

    print(f"Total products: {len(products)}")
    print(f"Categories: {', '.join(catalog.get_categories())}")

    print("\nSample products:")
    for i, (product_id, product) in enumerate(list(products.items())[:3]):
        print(f"{i+1}. {product['name']} - ${product['price']} ({product['category']})")


def demo_data_management():
    """Demonstrate data management functionality"""
    print("\n\n💾 Data Management Demo")
    print("=" * 50)

    data_manager = DataManager()

    # Create sample feedback
    sample_feedback = {
        "product_id": "prod_001",
        "product_name": "Wireless Bluetooth Headphones",
        "feedback_text": "Great sound quality and comfortable to wear!",
        "input_method": "Text Input",
        "timestamp": "2024-01-15T10:30:00",
        "sentiment_analysis": {
            "overall_sentiment": 0.7,
            "textblob_sentiment": 0.6,
            "vader_sentiment": 0.8,
            "keyword_sentiment": 0.5,
            "subjectivity": 0.6,
            "confidence": 0.85,
            "text_length": 45,
            "word_count": 8,
        },
    }

    # Save sample feedback
    success = data_manager.save_feedback(sample_feedback)
    print(f"Sample feedback saved: {'✅' if success else '❌'}")

    # Get statistics
    stats = data_manager.get_sentiment_statistics()
    print(f"Total feedback records: {stats['total_feedback']}")
    print(f"Average sentiment: {stats['avg_sentiment']:.3f}")
    print(f"Average confidence: {stats['avg_confidence']:.1%}")


def main():
    """Run all demos"""
    try:
        demo_sentiment_analysis()
        demo_product_catalog()
        demo_data_management()

        print("\n\n🎉 Demo completed successfully!")
        print("\nTo run the full web application:")
        print("  ./run.sh")
        print("  or")
        print("  streamlit run app.py")

    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
