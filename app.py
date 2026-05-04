import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns
import zipfile
import io
import pandas as pd

plt.style.use('seaborn-v0_8-whitegrid')

st.set_page_config(
    page_title="WhatsApp Chat Analyzer",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def load_data(data):
    return preprocessor.preprocess(data)

st.sidebar.title("Whatsapp Chats Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is None:
    _, center, _ = st.columns([1, 6, 1])
    with center:
        st.title("💬 WhatsApp Chat Analyzer")
        st.caption("Upload your chat export to uncover insights about your conversations.")

        st.divider()

        st.subheader("🚀 How to get started")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.info("**Step 1 — Export your chat**\n\nOpen WhatsApp → tap the contact/group → More → Export Chat → Without Media")

        with col2:
            st.info("**Step 2 — Upload the file**\n\nUse the file uploader in the sidebar to select your exported .txt file")

        with col3:
            st.info("**Step 3 — Explore insights**\n\nPick a user or choose Overall, then click Show Analysis")

        st.divider()

        st.subheader("📊 What you'll get")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.success("📈 **Message Stats**\nTotal messages, words, media & links shared")
            st.success("📅 **Timelines**\nDaily and monthly message trends")

        with col2:
            st.success("🔥 **Activity Map**\nBusiest days, months & hourly heatmap")
            st.success("☁️ **Word Cloud**\nMost frequently used words visualized")

        with col3:
            st.success("😄 **Emoji Analysis**\nTop emojis and their usage breakdown")
            st.success("👤 **User Breakdown**\nWho talks the most in the group")

        st.divider()
        st.caption("⚠️ Your data never leaves your device. Everything is processed locally.")

else:
    try:
        if uploaded_file.name.endswith(".zip"):

            with zipfile.ZipFile(io.BytesIO(uploaded_file.getvalue()), 'r') as z:

                txt_files = [f for f in z.namelist() if f.endswith(".txt")]

                if len(txt_files) == 0:
                    st.error("No .txt file found inside the zip. Please export the chat again.")
                    st.stop()

                raw_data = z.read(txt_files[0])

                try:
                    data = raw_data.decode('utf-8')

                except UnicodeDecodeError:

                    try:
                        data = raw_data.decode('utf-8-sig')

                    except UnicodeDecodeError:
                        data = raw_data.decode('latin-1')

        else:

            bytes_data = uploaded_file.getvalue()

            try:
                data = bytes_data.decode('utf-8')

            except UnicodeDecodeError:

                try:
                    data = bytes_data.decode('utf-8-sig')

                except UnicodeDecodeError:
                    data = bytes_data.decode('latin-1')

        data = data.replace('\r\n', '\n')

        df = load_data(data)

        if df.empty:
            st.error("The file appears to be empty or not a valid WhatsApp chat export.")
            st.stop()

        if 'group_notification' not in df['user'].values:
            st.error("Could not parse the file. Make sure it is a valid WhatsApp chat export.")
            st.stop()

        user_list = df['user'].unique().tolist()
        user_list.remove('group_notification')
        user_list.sort()
        user_list.insert(0, "Overall")

        selected_user = st.sidebar.selectbox("show analysis wrt ", user_list)

        if st.sidebar.button("Show_Analysis"):
            with st.spinner("Analyzing your chat... please wait ⏳"):

                num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
                timeline_monthly = helper.monthly_timeline(selected_user, df)
                timeline_daily = helper.daily_timeline(selected_user, df)
                busy_day = helper.week_activity_map(selected_user, df)
                busy_month = helper.month_activity_map(selected_user, df)
                user_heatmap = helper.activity_heatmap(selected_user, df)
                df_25 = helper.top_words(selected_user, df)
                df_wc = helper.create_wordcloud(selected_user, df)
                emoji_df = helper.emoji_helper(selected_user, df)
                emoji_df.columns = ['Emoji', 'Count']

                if selected_user == 'Overall':
                    x, new_df = helper.most_busy_users(df)

                _, center, _ = st.columns([1, 6, 1])

                with center:

                    st.title("Top Statistics")
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.header("Total Message")
                        st.title(num_messages)
                    with col2:
                        st.header("Total Words")
                        st.title(words)
                    with col3:
                        st.header("Media Shared")
                        st.title(num_media_messages)
                    with col4:
                        st.header("Links Shared")
                        st.title(num_links)

                    st.divider()

                    with st.expander("📅 Monthly Timeline", expanded=False):
                        st.subheader("📅 Monthly Timeline")
                        fig, ax = plt.subplots()
                        ax.plot(timeline_monthly['time'], timeline_monthly['message'], color='#6C63FF', marker='o', linewidth=2)
                        ax.set_ylabel("Messages", fontsize=11)
                        plt.xticks(rotation='vertical')
                        st.pyplot(fig)

                    with st.expander("📆 Daily Timeline", expanded=False):
                        st.subheader("📆 Daily Timeline")
                        fig, ax = plt.subplots()
                        ax.plot(timeline_daily['only_date'], timeline_daily['message'], color='#FF6B6B', linewidth=2)
                        ax.set_ylabel("Messages", fontsize=11)
                        plt.xticks(rotation='vertical')
                        st.pyplot(fig)

                    with st.expander("🗺️ Activity Map", expanded=False):
                        st.subheader("🗺️ Activity Map")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.header("Most Busy Day")
                            fig, ax = plt.subplots()
                            ax.bar(busy_day.index, busy_day.values, color='#FFA94D', edgecolor='white')
                            ax.set_ylabel("Messages", fontsize=11)
                            plt.xticks(rotation='vertical')
                            st.pyplot(fig)
                        with col2:
                            st.header("Most Busy Month")
                            fig, ax = plt.subplots()
                            ax.bar(busy_month.index, busy_month.values, color='#CC5DE8', edgecolor='white')
                            ax.set_ylabel("Messages", fontsize=11)
                            plt.xticks(rotation='vertical')
                            st.pyplot(fig)

                    with st.expander("🔥 Weekly Activity Heatmap", expanded=False):
                        st.subheader("🔥 Weekly Activity Heatmap")
                        rows, cols = user_heatmap.shape
                        fig, ax = plt.subplots(figsize=(cols, rows))
                        ax = sns.heatmap(user_heatmap, square=True)
                        st.pyplot(fig)

                    if selected_user == 'Overall':
                        with st.expander("👤 Most Busy Users", expanded=False):
                            st.subheader("👤 Most Busy Users")
                            fig, ax = plt.subplots()
                            col1, col2 = st.columns(2)
                            with col1:
                                ax.bar(x.index, x.values, color='#FF6B6B', edgecolor='white')
                                ax.set_ylabel("Messages", fontsize=11)
                                plt.xticks(rotation='vertical')
                                st.pyplot(fig)
                            with col2:
                                st.dataframe(new_df)

                    with st.expander("☁️ WordCloud", expanded=False):
                        st.subheader("☁️ WordCloud")
                        fig, ax = plt.subplots(figsize=(10, 4))
                        ax.imshow(df_wc)
                        ax.axis('off')
                        plt.tight_layout()
                        st.pyplot(fig, use_container_width=True)

                    with st.expander("🔤 Most Frequent Words", expanded=False):
                        st.subheader("🔤 Most Frequent Words")
                        fig, ax = plt.subplots()
                        ax.barh(df_25['word'], df_25['frequency'], color='#4DABF7', edgecolor='white')
                        ax.set_xlabel("Frequency", fontsize=11)
                        ax.set_ylabel("Words", fontsize=11)
                        ax.invert_yaxis()
                        st.pyplot(fig)

                    with st.expander("😄 Emoji Analysis", expanded=False):
                        st.subheader("😄 Emoji Analysis")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.dataframe(emoji_df, use_container_width=True)
                        with col2:
                            with plt.style.context('default'):
                                fig, ax = plt.subplots()
                                wedges, texts, autotexts = ax.pie(
                                    emoji_df['Count'].head(),
                                    autopct='%0.2f%%',
                                    startangle=140,
                                    colors=['#FF6B6B', '#FFA94D', '#FFD43B', '#69DB7C', '#4DABF7'],
                                    wedgeprops={'edgecolor': 'white', 'linewidth': 2}
                                )
                                ax.legend(
                                    wedges,
                                    [f"{row['Emoji']}  {row['Count']}" for _, row in emoji_df.head().iterrows()],
                                    title="Emojis",
                                    loc="center left",
                                    bbox_to_anchor=(1, 0, 0.5, 1),
                                    prop={'family': 'Segoe UI Emoji', 'size': 14}
                                )
                                st.pyplot(fig)

                    with st.expander("📥 Download Report", expanded=False):
                        st.subheader("📥 Download Report")

                        stats_df = pd.DataFrame({
                            'Metric': ['Total Messages', 'Total Words', 'Media Shared', 'Links Shared'],
                            'Value': [num_messages, words, num_media_messages, num_links]
                        })

                        separator = pd.DataFrame({'Metric': [''], 'Value': ['']})

                        full_report = pd.concat([
                            pd.DataFrame({'Metric': ['=== STATS SUMMARY ==='], 'Value': ['']}),
                            stats_df,
                            separator,
                            pd.DataFrame({'Metric': ['=== MONTHLY TIMELINE ==='], 'Value': ['']}),
                            timeline_monthly[['time', 'message']].rename(columns={'time': 'Metric', 'message': 'Value'}),
                            separator,
                            pd.DataFrame({'Metric': ['=== MOST BUSY DAY ==='], 'Value': ['']}),
                            busy_day.reset_index().rename(columns={'day_name': 'Metric', 'count': 'Value'}),
                            separator,
                            pd.DataFrame({'Metric': ['=== MOST BUSY MONTH ==='], 'Value': ['']}),
                            busy_month.reset_index().rename(columns={'month': 'Metric', 'count': 'Value'}),
                            separator,
                            pd.DataFrame({'Metric': ['=== TOP 25 WORDS ==='], 'Value': ['']}),
                            df_25.rename(columns={'word': 'Metric', 'frequency': 'Value'}),
                        ], ignore_index=True)

                        st.download_button(
                            label="⬇️ Download Full Report",
                            data=full_report.to_csv(index=False),
                            file_name="whatsapp_full_report.csv",
                            mime='text/csv',
                            type="primary"
                        )

                        st.divider()

                        st.subheader("Download by Section")
                        download_option = st.selectbox(
                            "Select data to download",
                            ["Stats Summary", "Monthly Timeline", "Most Busy Day", "Most Busy Month", "Top 25 Words"]
                        )

                        if download_option == "Stats Summary":
                            csv = stats_df.to_csv(index=False)
                            filename = "stats_summary.csv"
                        elif download_option == "Monthly Timeline":
                            csv = timeline_monthly[['time', 'message']].to_csv(index=False)
                            filename = "monthly_timeline.csv"
                        elif download_option == "Most Busy Day":
                            csv = busy_day.reset_index().to_csv(index=False)
                            filename = "busy_day.csv"
                        elif download_option == "Most Busy Month":
                            csv = busy_month.reset_index().to_csv(index=False)
                            filename = "busy_month.csv"
                        elif download_option == "Top 25 Words":
                            csv = df_25.to_csv(index=False)
                            filename = "top_words.csv"

                        st.download_button(
                            label="⬇️ Download CSV",
                            data=csv,
                            file_name=filename,
                            mime='text/csv'
                        )

    except UnicodeDecodeError:
        st.error("Could not read the file. Make sure it is exported as a .txt or .zip from WhatsApp.")
        st.stop()
    except zipfile.BadZipFile:
        st.error("The zip file appears to be corrupted. Please try exporting your chat again.")
        st.stop()
    except Exception as e:
        st.error(f"Something went wrong: {e}")
        st.stop()