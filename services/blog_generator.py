import os
import requests
from datetime import datetime
from typing import List, Dict
from models.database import BlogPost, db

class BlogGeneratorService:
    def __init__(self):
        self.api_key = os.getenv('NEBIUS_API_KEY')
        self.api_url = 'https://api.studio.nebius.ai/v1/chat/completions'
        
    def generate_blog_posts(self, num_posts: int = 2) -> List[Dict]:
        """Generate new blog posts using AI"""
        topics = self._get_real_estate_topics()
        generated_posts = []
        
        for topic in topics[:num_posts]:
            try:
                content = self._generate_content(topic)
                post = BlogPost(
                    title=topic['title'],
                    content=content['body'],
                    summary=content['summary'],
                    author='AI Content Team',
                    tags=topic['tags'],
                    image_url=self._get_relevant_image(topic['title'])
                )
                db.session.add(post)
                generated_posts.append(post)
            except Exception as e:
                print(f"Error generating blog post: {str(e)}")
                continue
        
        db.session.commit()
        return generated_posts
    
    def _get_real_estate_topics(self) -> List[Dict]:
        """Get relevant real estate topics for blog posts"""
        try:
            response = requests.post(
                self.api_url,
                headers={
                    'Authorization': f'Bearer {self.api_key}',
                    'Content-Type': 'application/json'
                },
                json={
                    'model': 'meta-llama/Meta-Llama-3.1-70B-Instruct',
                    'messages': [
                        {
                            'role': 'system',
                            'content': 'You are a real estate content expert. Generate 3 trending and relevant blog post topics with titles and tags.'
                        }
                    ],
                    'temperature': 0.8,
                    'max_tokens': 200,
                    'top_p': 1,
                    'frequency_penalty': 0.2,
                    'presence_penalty': 0.2
                }
            )
            
            if response.status_code == 200:
                topics = response.json()['choices'][0]['message']['content']
                return self._process_topics(topics)
            return []
            
        except Exception as e:
            print(f"Error getting topics: {str(e)}")
            return []
    
    def _generate_content(self, topic: Dict) -> Dict:
        """Generate blog post content for a given topic"""
        try:
            response = requests.post(
                self.api_url,
                headers={
                    'Authorization': f'Bearer {self.api_key}',
                    'Content-Type': 'application/json'
                },
                json={
                    'model': 'meta-llama/Meta-Llama-3.1-70B-Instruct',
                    'messages': [
                        {
                            'role': 'system',
                            'content': 'You are a professional real estate content writer.'
                        },
                        {
                            'role': 'user',
                            'content': f'Write a detailed blog post about: {topic["title"]}'
                        }
                    ],
                    'temperature': 0.7,
                    'max_tokens': 1000,
                    'top_p': 1,
                    'frequency_penalty': 0.3,
                    'presence_penalty': 0.3
                }
            )
            
            if response.status_code == 200:
                content = response.json()['choices'][0]['message']['content']
                return {
                    'body': content,
                    'summary': self._generate_summary(content)
                }
            return None
            
        except Exception as e:
            print(f"Error generating content: {str(e)}")
            return None
    
    def _generate_summary(self, content: str) -> str:
        """Generate a summary of the blog post content"""
        try:
            response = requests.post(
                self.api_url,
                headers={
                    'Authorization': f'Bearer {self.api_key}',
                    'Content-Type': 'application/json'
                },
                json={
                    'model': 'meta-llama/Meta-Llama-3.1-70B-Instruct',
                    'messages': [
                        {
                            'role': 'system',
                            'content': 'You are a content summarizer.'
                        },
                        {
                            'role': 'user',
                            'content': f'Generate a brief summary (max 200 words) of the following content: {content}'
                        }
                    ],
                    'temperature': 0.5,
                    'max_tokens': 200,
                    'top_p': 1,
                    'frequency_penalty': 0,
                    'presence_penalty': 0
                }
            )
            
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            return ""
            
        except Exception as e:
            print(f"Error generating summary: {str(e)}")
            return ""
    
    def _get_relevant_image(self, title: str) -> str:
        """Get a relevant image URL for the blog post"""
        # Implement image search/generation logic here
        # For now, return a placeholder
        return f"https://via.placeholder.com/800x400?text={title.replace(' ', '+')}"
    
    def _process_topics(self, topics_text: str) -> List[Dict]:
        """Process and structure the generated topics"""
        try:
            response = requests.post(
                self.api_url,
                headers={
                    'Authorization': f'Bearer {self.api_key}',
                    'Content-Type': 'application/json'
                },
                json={
                    'model': 'meta-llama/Meta-Llama-3.1-70B-Instruct',
                    'messages': [
                        {
                            'role': 'system',
                            'content': 'Convert the following topics into a structured format with title and tags.'
                        },
                        {
                            'role': 'user',
                            'content': topics_text
                        }
                    ],
                    'temperature': 0.3,
                    'max_tokens': 200,
                    'response_format': {'type': 'json_object'}
                }
            )
            
            if response.status_code == 200:
                result = response.json()['choices'][0]['message']['content']
                return result.get('topics', [])
            return []
            
        except Exception as e:
            print(f"Error processing topics: {str(e)}")
            return []
