import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from .models import Post, UserProfile

def get_recommendations(user):
    # Load data
    posts = Post.objects.all().values('id', 'category')
    user_profile = UserProfile.objects.get(user=user)

    
    posts_df = pd.DataFrame(posts)
    
    
    tfidf = TfidfVectorizer()

    
    tfidf_matrix = tfidf.fit_transform(posts_df['category'])

    
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    
    liked_posts = user_profile.liked_posts.all().values_list('id', flat=True)
    followed_accounts = user_profile.followed_accounts.all()
    
    followed_posts = Post.objects.filter(user__in=followed_accounts).values_list('id', flat=True)

    
    combined_categories = posts_df[posts_df['id'].isin(liked_posts) | posts_df['id'].isin(followed_posts)]['category']

    preferred_categories = user_profile.preferred_categories.split(',')

    combined_categories = pd.concat([combined_categories, pd.Series(preferred_categories)], ignore_index=True)
    
    
    tfidf_features = tfidf.transform(combined_categories)
    
    
    cosine_similarities = linear_kernel(tfidf_features, tfidf_matrix)
    
    
    aggregate_similarities = cosine_similarities.mean(axis=0)
    
    
    similar_indices = aggregate_similarities.argsort()[-15:][::-1]  # Get top 10 similar posts
    
    recommended_post_ids = [posts_df['id'].iloc[i] for i in similar_indices]
    recommended_posts = Post.objects.filter(id__in=recommended_post_ids)
    
    return recommended_posts