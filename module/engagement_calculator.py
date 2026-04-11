def calculate_engagement_rate(posts, followers):
    if not posts or followers == 0:
        return 0.0, 0.0, 0.0

    avg_likes = sum(post["likes"] for post in posts) / len(posts)
    avg_comments = sum(post["comments"] for post in posts) / len(posts)
 
    # 100 * Followers / (Average Likes + Average Commeents) = Engagement Rate
    engagement_rate = ((avg_likes + avg_comments) / followers) * 100
    return round(engagement_rate, 2), avg_likes, avg_comments
