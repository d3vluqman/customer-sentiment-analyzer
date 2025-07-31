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

    # Initialize components
    sentiment_analyzer, product_catalog, data_manager, audio_processor = (
        initialize_components()
    )

    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a page",
        [
            "Feedback Collection",
            "Analytics Dashboard",
            "Product Catalog",
            "Data Management",
        ],
    )

    if page == "Feedback Collection":
        feedback_collection_page(
            sentiment_analyzer, product_catalog, data_manager, audio_processor
        )
    elif page == "Analytics Dashboard":
        analytics_dashboard_page(data_manager)
    elif page == "Product Catalog":
        product_catalog_page(product_catalog)
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


def product_catalog_page(product_catalog):
    """Product catalog management interface"""
    st.header("🛍️ Product Catalog")

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
            st.write(f"ID: {product_id}")
            st.divider()


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
                st.experimental_rerun()


if __name__ == "__main__":
    main()
