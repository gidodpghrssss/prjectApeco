import os
import sys
import schedule
import time
from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.blog_generator import BlogGeneratorService

# Set up logging
log_file = 'blog_scheduler.log'
logger = logging.getLogger('BlogScheduler')
logger.setLevel(logging.INFO)
handler = RotatingFileHandler(log_file, maxBytes=1024*1024, backupCount=5)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def generate_blog_posts():
    """Generate blog posts using the BlogGeneratorService"""
    try:
        logger.info("Starting blog post generation")
        blog_generator = BlogGeneratorService()
        posts = blog_generator.generate_blog_posts(num_posts=2)
        logger.info(f"Successfully generated {len(posts)} blog posts")
        
        # Log the titles of generated posts
        for post in posts:
            logger.info(f"Generated post: {post.title}")
            
    except Exception as e:
        logger.error(f"Error generating blog posts: {str(e)}")

def main():
    """Main function to run the blog post scheduler"""
    logger.info("Starting blog post scheduler")
    
    # Schedule blog post generation twice per day
    schedule.every().day.at("10:00").do(generate_blog_posts)  # Morning post
    schedule.every().day.at("15:00").do(generate_blog_posts)  # Afternoon post
    
    logger.info("Blog post scheduler is running")
    
    while True:
        try:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
        except Exception as e:
            logger.error(f"Error in scheduler loop: {str(e)}")
            time.sleep(300)  # Wait 5 minutes before retrying

if __name__ == "__main__":
    main()
