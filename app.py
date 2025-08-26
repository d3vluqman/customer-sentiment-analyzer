import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import sqlite3
import os
from pathlib import Path

# Import our custom modules
from src.sentiment_analyzer import SentimentAnalyzer
from src.product_catalog import ProductCatalog
from src.data_manager import DataManager
from src.audio_processor import AudioProcessor

# Page configuration
st.set_page_config(
    page_title="Voice Sentiment Analyzer",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Initialize components
@st.cache_resource
def initialize_components():
    """Initialize all application components"""
    sentiment_analyzer = SentimentAnalyzer()
    product_catalog = ProductCatalog()
    data_manager = DataManager()
    audio_processor = AudioProcessor()
    return sentiment_analyzer, product_catalog, data_manager, audio_processor


def main():
    """Main application entry point"""
    st.title("🎤 Voice Sentiment Analyzer")
    st.markdown("Analyze customer sentiment from voice recordings and text feedback")

    # Initialize session state
    if "selected_product_id" not in st.session_state:
        st.session_state.selected_product_id = None
    if "current_page" not in st.session_state:
        st.session_state.current_page = "Feedback Collection"

    # Initialize components
    sentiment_analyzer, product_catalog, data_manager, audio_processor = (
        initialize_components()
    )

    # Sidebar navigation
    st.sidebar.title("Navigation")

    # Check if we should show product analytics
    if st.session_state.selected_product_id:
        products = product_catalog.get_products()
        selected_product = products.get(st.session_state.selected_product_id)
        if selected_product:
            st.sidebar.info(
                f"📊 Viewing analytics for:\n**{selected_product['name']}**"
            )
            if st.sidebar.button("← Back to Catalog"):
                st.session_state.selected_product_id = None
                st.session_state.current_page = "Product Catalog"
                st.rerun()

    # Main navigation
    page_options = [
        "Feedback Collection",
        "Analytics Dashboard",
        "Product Catalog",
        "Data Management",
    ]

    # Add product analytics option if a product is selected
    if st.session_state.selected_product_id:
        page_options.insert(2, "Product Analytics")
        default_page = "Product Analytics"
    else:
        default_page = st.session_state.current_page

    page = st.sidebar.selectbox(
        "Choose a page",
        page_options,
        index=page_options.index(default_page) if default_page in page_options else 0,
    )

    # Update current page
    st.session_state.current_page = page

    if page == "Feedback Collection":
        feedback_collection_page(
            sentiment_analyzer, product_catalog, data_manager, audio_processor
        )
    elif page == "Analytics Dashboard":
        analytics_dashboard_page(data_manager)
    elif page == "Product Catalog":
        product_catalog_page(product_catalog, data_manager)
    elif page == "Product Analytics":
        product_analytics_page(data_manager, product_catalog)
    elif page == "Data Management":
        data_management_page(data_manager)


def feedback_collection_page(
    sentiment_analyzer, product_catalog, data_manager, audio_processor
):
    """Feedback collection interface"""
    st.header("📝 Collect Customer Feedback")

    # Product selection
    st.subheader("1. Select Product")
    products = product_catalog.get_products()

    col1, col2 = st.columns([2, 1])
    with col1:
        selected_product = st.selectbox(
            "Choose a product for feedback",
            options=list(products.keys()),
            format_func=lambda x: f"{products[x]['name']} - ${products[x]['price']}",
        )

    with col2:
        if selected_product:
            product_info = products[selected_product]
            st.image(
                product_info.get("image", "https://via.placeholder.com/150"), width=150
            )
            st.write(f"**Category:** {product_info['category']}")
            st.write(f"**Price:** ${product_info['price']}")

    st.divider()

    # Feedback input method selection
    st.subheader("2. Provide Feedback")
    input_method = st.radio(
        "Choose input method:", ["Voice Recording", "Text Input"], horizontal=True
    )

    feedback_text = ""

    if input_method == "Voice Recording":
        st.info("🎤 Record your voice feedback using the audio recorder below")

        # Audio recording interface using the correct Streamlit method
        audio_data = st.audio_input("Record your feedback")

        if audio_data is not None:
            st.success("Audio recorded successfully!")

            # Process audio to text
            with st.spinner("Converting speech to text..."):
                try:
                    feedback_text = audio_processor.speech_to_text(audio_data)
                    st.write("**Transcribed text:**")
                    st.write(feedback_text)
                except Exception as e:
                    st.error(f"Error processing audio: {str(e)}")
                    st.info("Please try using text input instead.")

    else:  # Text Input
        feedback_text = st.text_area(
            "Enter your feedback:",
            placeholder="Share your thoughts about this product...",
            max_chars=1000,
            height=150,
        )

    # Analyze sentiment
    if feedback_text and st.button("Analyze Sentiment", type="primary"):
        with st.spinner("Analyzing sentiment..."):
            try:
                # Perform sentiment analysis
                analysis_result = sentiment_analyzer.analyze_sentiment(feedback_text)

                # Display results
                st.subheader("📊 Sentiment Analysis Results")

                col1, col2, col3 = st.columns(3)

                with col1:
                    sentiment_score = analysis_result["overall_sentiment"]
                    sentiment_label = (
                        "Positive"
                        if sentiment_score > 0.1
                        else "Negative" if sentiment_score < -0.1 else "Neutral"
                    )
                    color = (
                        "green"
                        if sentiment_score > 0.1
                        else "red" if sentiment_score < -0.1 else "orange"
                    )

                    st.metric(
                        "Overall Sentiment", sentiment_label, f"{sentiment_score:.3f}"
                    )

                with col2:
                    confidence = analysis_result["confidence"]
                    st.metric(
                        "Confidence",
                        f"{confidence:.1%}",
                        help="How confident the model is in this prediction",
                    )

                with col3:
                    subjectivity = analysis_result.get("subjectivity", 0)
                    st.metric(
                        "Subjectivity",
                        f"{subjectivity:.3f}",
                        help="0 = Objective, 1 = Subjective",
                    )

                # Detailed breakdown
                st.subheader("Detailed Analysis")
                breakdown_df = pd.DataFrame(
                    [
                        {
                            "Model": "TextBlob",
                            "Score": analysis_result["textblob_sentiment"],
                            "Type": "Polarity",
                        },
                        {
                            "Model": "VADER",
                            "Score": analysis_result["vader_sentiment"],
                            "Type": "Compound",
                        },
                        {
                            "Model": "Keyword",
                            "Score": analysis_result["keyword_sentiment"],
                            "Type": "Custom",
                        },
                    ]
                )

                fig = px.bar(
                    breakdown_df,
                    x="Model",
                    y="Score",
                    color="Score",
                    color_continuous_scale="RdYlGn",
                    title="Sentiment Scores by Model",
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)

                # Save feedback
                feedback_data = {
                    "product_id": selected_product,
                    "product_name": products[selected_product]["name"],
                    "feedback_text": feedback_text,
                    "input_method": input_method,
                    "timestamp": datetime.now().isoformat(),
                    "sentiment_analysis": analysis_result,
                }

                data_manager.save_feedback(feedback_data)
                st.success("✅ Feedback saved successfully!")

            except Exception as e:
                st.error(f"Error analyzing sentiment: {str(e)}")


def analytics_dashboard_page(data_manager):
    """Analytics dashboard interface"""
    st.header("📈 Analytics Dashboard")

    # Load feedback data
    feedback_data = data_manager.get_all_feedback()

    if not feedback_data:
        st.info("No feedback data available yet. Please collect some feedback first!")
        return

    df = pd.DataFrame(feedback_data)
    df["timestamp"] = pd.to_datetime(df["timestamp"], format="mixed")
    df["sentiment_score"] = df["sentiment_analysis"].apply(
        lambda x: x["overall_sentiment"]
    )
    df["confidence"] = df["sentiment_analysis"].apply(lambda x: x["confidence"])

    # Key metrics
    st.subheader("📊 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_feedback = len(df)
        st.metric("Total Feedback", total_feedback)

    with col2:
        avg_sentiment = df["sentiment_score"].mean()
        st.metric("Average Sentiment", f"{avg_sentiment:.3f}")

    with col3:
        positive_ratio = (df["sentiment_score"] > 0.1).mean()
        st.metric("Positive Feedback", f"{positive_ratio:.1%}")

    with col4:
        avg_confidence = df["confidence"].mean()
        st.metric("Average Confidence", f"{avg_confidence:.1%}")

    # Charts
    col1, col2 = st.columns(2)

    with col1:
        # Sentiment distribution
        st.subheader("Sentiment Distribution")
        sentiment_labels = df["sentiment_score"].apply(
            lambda x: "Positive" if x > 0.1 else "Negative" if x < -0.1 else "Neutral"
        )
        sentiment_counts = sentiment_labels.value_counts()

        fig = px.pie(
            values=sentiment_counts.values,
            names=sentiment_counts.index,
            color_discrete_map={
                "Positive": "green",
                "Negative": "red",
                "Neutral": "orange",
            },
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Sentiment by product
        st.subheader("Sentiment by Product")
        product_sentiment = (
            df.groupby("product_name")["sentiment_score"]
            .mean()
            .sort_values(ascending=True)
        )

        fig = px.bar(
            x=product_sentiment.values,
            y=product_sentiment.index,
            orientation="h",
            color=product_sentiment.values,
            color_continuous_scale="RdYlGn",
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    # Time series
    st.subheader("Sentiment Trends Over Time")
    daily_sentiment = df.set_index("timestamp").resample("D")["sentiment_score"].mean()

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=daily_sentiment.index,
            y=daily_sentiment.values,
            mode="lines+markers",
            name="Daily Average Sentiment",
        )
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

    # Recent feedback
    st.subheader("Recent Feedback")
    recent_df = df.nlargest(10, "timestamp")[
        ["product_name", "feedback_text", "sentiment_score", "confidence", "timestamp"]
    ]
    st.dataframe(recent_df, use_container_width=True)


def product_catalog_page(product_catalog, data_manager):
    """Product catalog management interface"""
    st.header("🛍️ Product Catalog")
    st.markdown(
        "Browse products and click **View Analytics** to see sentiment analysis for each product."
    )

    products = product_catalog.get_products()

    # Search and filter
    col1, col2 = st.columns([2, 1])
    with col1:
        search_term = st.text_input(
            "Search products:", placeholder="Enter product name..."
        )
    with col2:
        categories = list(set(p["category"] for p in products.values()))
        selected_category = st.selectbox("Filter by category:", ["All"] + categories)

    # Filter products
    filtered_products = products
    if search_term:
        filtered_products = {
            k: v
            for k, v in products.items()
            if search_term.lower() in v["name"].lower()
        }
    if selected_category != "All":
        filtered_products = {
            k: v
            for k, v in filtered_products.items()
            if v["category"] == selected_category
        }

    # Display products
    cols = st.columns(3)
    for i, (product_id, product) in enumerate(filtered_products.items()):
        with cols[i % 3]:
            st.image(product.get("image", "https://via.placeholder.com/200"), width=200)
            st.write(f"**{product['name']}**")
            st.write(f"Category: {product['category']}")
            st.write(f"Price: ${product['price']}")

            # Get feedback count for this product
            product_feedback = data_manager.get_feedback_by_product(product_id)
            feedback_count = len(product_feedback)

            if feedback_count > 0:
                avg_sentiment = (
                    sum(f["overall_sentiment"] for f in product_feedback)
                    / feedback_count
                )
                sentiment_label = (
                    "Positive"
                    if avg_sentiment > 0.1
                    else "Negative" if avg_sentiment < -0.1 else "Neutral"
                )
                st.write(
                    f"📊 {feedback_count} reviews • {sentiment_label} ({avg_sentiment:.2f})"
                )
            else:
                st.write("📊 No reviews yet")

            # Analytics button
            if st.button(f"📈 View Analytics", key=f"analytics_{product_id}"):
                st.session_state.selected_product_id = product_id
                st.session_state.current_page = "Product Analytics"
                try:
                    st.rerun()
                except AttributeError:
                    st.rerun()

            st.divider()


def product_analytics_page(data_manager, product_catalog):
    """Product-specific analytics interface"""
    if not st.session_state.selected_product_id:
        st.error("No product selected. Please go back to the Product Catalog.")
        return

    products = product_catalog.get_products()
    product = products.get(st.session_state.selected_product_id)

    if not product:
        st.error("Product not found. Please go back to the Product Catalog.")
        return

    # Header with product info
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image(product.get("image", "https://via.placeholder.com/200"), width=150)
    with col2:
        st.title(f"📊 {product['name']} Analytics")
        st.write(f"**Category:** {product['category']}")
        st.write(f"**Price:** ${product['price']}")
        st.write(f"**Description:** {product['description']}")

    st.divider()

    # Get product-specific feedback
    product_feedback = data_manager.get_feedback_by_product(
        st.session_state.selected_product_id
    )

    if not product_feedback:
        st.info(
            f"No feedback available for {product['name']} yet. Be the first to leave a review!"
        )

        # Quick feedback option
        st.subheader("💬 Leave Feedback")
        quick_feedback = st.text_area(
            "Share your thoughts about this product:",
            placeholder="What do you think about this product?",
        )

        if quick_feedback and st.button("Submit Feedback"):
            from src.sentiment_analyzer import SentimentAnalyzer

            analyzer = SentimentAnalyzer()
            analysis = analyzer.analyze_sentiment(quick_feedback)

            feedback_data = {
                "product_id": st.session_state.selected_product_id,
                "product_name": product["name"],
                "feedback_text": quick_feedback,
                "input_method": "Text Input",
                "timestamp": datetime.now().isoformat(),
                "sentiment_analysis": analysis,
            }

            data_manager.save_feedback(feedback_data)
            st.success("Feedback submitted successfully!")
            st.rerun()

        return

    # Convert to DataFrame for analysis
    df = pd.DataFrame(product_feedback)
    df["timestamp"] = pd.to_datetime(df["timestamp"], format="mixed")
    df["sentiment_score"] = df.apply(lambda x: x.get("overall_sentiment", 0), axis=1)
    df["confidence"] = df.apply(lambda x: x.get("confidence", 0), axis=1)

    # Key metrics for this product
    st.subheader("📈 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_feedback = len(df)
        st.metric("Total Reviews", total_feedback)

    with col2:
        avg_sentiment = df["sentiment_score"].mean()
        sentiment_trend = (
            "↗️" if avg_sentiment > 0.1 else "↘️" if avg_sentiment < -0.1 else "➡️"
        )
        st.metric("Average Sentiment", f"{avg_sentiment:.3f}", sentiment_trend)

    with col3:
        positive_ratio = (df["sentiment_score"] > 0.1).mean()
        st.metric("Positive Reviews", f"{positive_ratio:.1%}")

    with col4:
        avg_confidence = df["confidence"].mean()
        st.metric("Avg Confidence", f"{avg_confidence:.1%}")

    # Sentiment distribution for this product
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Sentiment Distribution")
        sentiment_labels = df["sentiment_score"].apply(
            lambda x: "Positive" if x > 0.1 else "Negative" if x < -0.1 else "Neutral"
        )
        sentiment_counts = sentiment_labels.value_counts()

        fig = px.pie(
            values=sentiment_counts.values,
            names=sentiment_counts.index,
            color_discrete_map={
                "Positive": "green",
                "Negative": "red",
                "Neutral": "orange",
            },
            title=f"Sentiment Breakdown for {product['name']}",
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Sentiment Over Time")
        if len(df) > 1:
            # Group by date for trend analysis
            daily_sentiment = (
                df.set_index("timestamp").resample("D")["sentiment_score"].mean()
            )

            fig = go.Figure()
            fig.add_trace(
                go.Scatter(
                    x=daily_sentiment.index,
                    y=daily_sentiment.values,
                    mode="lines+markers",
                    name="Daily Average Sentiment",
                    line=dict(color="blue"),
                )
            )
            fig.update_layout(
                title=f"Sentiment Trend for {product['name']}",
                xaxis_title="Date",
                yaxis_title="Sentiment Score",
                height=400,
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Need more reviews to show trend analysis")

    # Confidence vs Sentiment scatter plot
    st.subheader("📊 Confidence vs Sentiment Analysis")
    fig = px.scatter(
        df,
        x="confidence",
        y="sentiment_score",
        title=f"Review Confidence vs Sentiment for {product['name']}",
        labels={"confidence": "Confidence Score", "sentiment_score": "Sentiment Score"},
        color="sentiment_score",
        color_continuous_scale="RdYlGn",
    )
    fig.add_hline(y=0, line_dash="dash", line_color="gray", annotation_text="Neutral")
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

    # Recent reviews for this product
    st.subheader("💬 Recent Reviews")
    recent_reviews = df.nlargest(5, "timestamp")[
        ["feedback_text", "sentiment_score", "confidence", "timestamp", "input_method"]
    ]

    for idx, review in recent_reviews.iterrows():
        sentiment_color = (
            "green"
            if review["sentiment_score"] > 0.1
            else "red" if review["sentiment_score"] < -0.1 else "orange"
        )
        sentiment_label = (
            "Positive"
            if review["sentiment_score"] > 0.1
            else "Negative" if review["sentiment_score"] < -0.1 else "Neutral"
        )

        with st.expander(
            f"{sentiment_label} Review - {review['timestamp'].strftime('%Y-%m-%d %H:%M')} ({review['input_method']})"
        ):
            st.write(f"**Review:** {review['feedback_text']}")
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Sentiment:** {review['sentiment_score']:.3f}")
            with col2:
                st.write(f"**Confidence:** {review['confidence']:.1%}")

    # Comparison with other products
    st.subheader("🔍 Product Comparison")
    all_feedback = data_manager.get_all_feedback()

    if len(all_feedback) > len(product_feedback):
        # Calculate average sentiment for all products
        other_products_sentiment = []
        for feedback in all_feedback:
            if feedback["product_id"] != st.session_state.selected_product_id:
                other_products_sentiment.append(
                    feedback["sentiment_analysis"]["overall_sentiment"]
                )

        if other_products_sentiment:
            avg_other_sentiment = sum(other_products_sentiment) / len(
                other_products_sentiment
            )

            comparison_data = pd.DataFrame(
                {
                    "Product": [product["name"], "Other Products Average"],
                    "Average Sentiment": [avg_sentiment, avg_other_sentiment],
                    "Review Count": [
                        len(product_feedback),
                        len(other_products_sentiment),
                    ],
                }
            )

            fig = px.bar(
                comparison_data,
                x="Product",
                y="Average Sentiment",
                color="Average Sentiment",
                color_continuous_scale="RdYlGn",
                title=f"How {product['name']} Compares to Other Products",
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

    # Export product-specific data
    st.subheader("📤 Export Product Data")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Export Product Reviews (CSV)"):
            csv_data = df.to_csv(index=False)
            st.download_button(
                "Download CSV",
                csv_data,
                f"{product['name'].replace(' ', '_')}_reviews.csv",
                "text/csv",
            )

    with col2:
        if st.button("Export Product Reviews (JSON)"):
            json_data = df.to_json(orient="records", indent=2)
            st.download_button(
                "Download JSON",
                json_data,
                f"{product['name'].replace(' ', '_')}_reviews.json",
                "application/json",
            )


def data_management_page(data_manager):
    """Data management interface"""
    st.header("💾 Data Management")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Export Data")
        if st.button("Export to CSV"):
            csv_data = data_manager.export_to_csv()
            st.download_button(
                "Download CSV", csv_data, "sentiment_feedback.csv", "text/csv"
            )

        if st.button("Export to JSON"):
            json_data = data_manager.export_to_json()
            st.download_button(
                "Download JSON",
                json_data,
                "sentiment_feedback.json",
                "application/json",
            )

    with col2:
        st.subheader("Database Info")
        feedback_count = len(data_manager.get_all_feedback())
        st.metric("Total Feedback Records", feedback_count)

        if st.button("Clear All Data", type="secondary"):
            if st.checkbox("I understand this will delete all data"):
                data_manager.clear_all_data()
                st.success("All data cleared!")
                st.rerun()


if __name__ == "__main__":
    main()
