import streamlit as st
import matplotlib.pyplot as plt
import preprocessor,helper
from helper import daily_timeline
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data=bytes_data.decode("utf-8")
    df=preprocessor.preprocess(data)

    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,'Overall')

    selected_user = st.sidebar.selectbox("Show Analysis with respect to",user_list)

    if st.sidebar.button("Show Analysis"):
        num_messages,words,num_media,num_links = helper.fetch_stats(selected_user,df)
        st.markdown("<h1><u>Top Statistics</u></h1>",unsafe_allow_html=True)
        col1,col2,col3,col4 = st.columns([1.3,1,1,1])


        with col1:
            st.markdown("<h3 style='text-align: center;color: white;'>Total Messages</h3>", unsafe_allow_html=True)
            st.markdown(f"<h1 style='text-align: center; color: white;'>{num_messages}</h1>", unsafe_allow_html=True)
        with col2:
            st.markdown("<h3 style='text-align: center;color: white;'>Total Words</h3>", unsafe_allow_html=True)
            st.markdown(f"<h1 style='text-align: center; color: white;'>{words}</h1>", unsafe_allow_html=True)
        with col3:
            st.markdown("<h4 style='text-align: center;color: white;'>Media Shared</h3>", unsafe_allow_html=True)
            st.markdown(f"<h1 style='text-align: center; color: white;'>{num_media}</h1>", unsafe_allow_html=True)
        with col4:
            st.markdown("<h4 style='text-align: center;color: white;'>Links Shared</h3>", unsafe_allow_html=True)
            st.markdown(f"<h1 style='text-align: center; color: white;'>{num_links}</h1>", unsafe_allow_html=True)

        #monthly timeline
        st.title("Monthly Timeline")
        timeline=helper.monthly_timeline(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(timeline['time'],timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #daily timeline
        st.title("Daily Timeline")
        daily_timeline=helper.daily_timeline(selected_user,df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'],daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #activity map

        st.markdown("<h1><u>Activity Map</u></h1>", unsafe_allow_html=True)
        col1,col2=st.columns(2)

        with col1:
            st.header("Most Busy Day")
            busy_day=helper.week_activity_map(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.header("Most Busy Month")
            busy_month=helper.monthly_activity_map(selected_user,df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index,busy_month.values,color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("HeatMap")
        user_heatmap =helper.activity_heatmap(selected_user,df)
        fig,ax=plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)


        if selected_user=='Overall':
            st.title("Most Active Users")
            x,new_df=helper.most_busy_users(df)
            fig,ax=plt.subplots()
            col1,col2=st.columns(2)

            with col1:
                ax.bar(x.index,x.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        st.title("WordCloud")
        df_wc = helper.create_wordcloud(selected_user,df)
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        most_common_df= helper.most_common_words(selected_user, df)
        fig,ax=plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')

        st.title("Most Common Words")
        st.pyplot(fig)

        emoji_df=helper.emoji_helper(selected_user,df)
        st.title("Emoji Analysis")

        col1,col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax=plt.subplots()
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct='%0.2f')
            st.pyplot(fig)