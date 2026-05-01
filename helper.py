from urlextract import URLExtract
extractor = URLExtract()

from wordcloud import WordCloud
from collections import Counter
import string
import pandas as pd
import emoji


def fetch_stats(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    num_messages = df.shape[0]
    words = []
    for message in df['message']:
        words.extend(message.split())

    #for no of media shared
    num_media_messages = df[df['message'] == '<Media omitted>'].shape[0]

    links = []
    for message in df['message']:
        links.extend(extractor.find_urls(message))
    
    return num_messages,len(words),num_media_messages,len(links)
        

def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0] * 100), 2).reset_index().rename(columns={'index': 'name', 'user': 'percentage'})
    return x,df




def create_wordcloud(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user'] == selected_user]

    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    df_wc = wc.generate(df['message'][df['message'] != '<Media omitted>'].str.cat(sep=" "))
    return df_wc


def top_words(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user'] == selected_user]

    # Combine all messages
    messages = df['message'][df['message'] != '<Media omitted>'].str.cat(sep=" ")
    messages = messages.lower()
    
    # Split by space
    words = messages.split(" ")

    # Remove punctuation from each word
    words = [w.strip(string.punctuation) for w in words if w.strip()]

     # Filter empty strings
    words = [w for w in words if w]
      
    # Count frequencies
    word_counts = Counter(words)
    top_25 = word_counts.most_common(25)
    
    # Convert to DataFrame
    result_df = pd.DataFrame(top_25, columns=['word', 'frequency'])
    
    return result_df






def emoji_helper(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user'] == selected_user]
    
    emojis = []
    words = []
    for message in df['message']:
        words.extend(message.split())
    for w in words:
        emojis.extend([c for c in w if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df






def monthly_timeline(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user'] == selected_user]
    
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + '-' + str(timeline['year'][i]))
    timeline['time'] = time

    return timeline



def daily_timeline(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline


def week_activity_map(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()


def month_activity_map(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()


def activity_heatmap(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap
    