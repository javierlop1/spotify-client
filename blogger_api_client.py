import os
import logging
from logging_config import setup_logging
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

setup_logging()  # Ensure the logger is set up
logger = logging.getLogger(__name__)

# SCOPES for Blogger API
SCOPES = ['https://www.googleapis.com/auth/blogger']

def get_credentials() -> Credentials:
    """
    Obtain credentials for the Blogger API using OAuth 2.0.

    Loads the credentials from `token.json` if they exist. If not, it opens
    a browser window for the user to sign in and authorize the application.

    Returns:
        google.oauth2.credentials.Credentials: OAuth 2.0 credentials.
    
    Raises:
        FileNotFoundError: If the client secret file is not found.
        Exception: If any error occurs during the authentication process.
    """
    creds = None
    try:
        # Check if credentials are stored in token.json
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
            if creds and creds.valid:
                logger.info('Valid credentials loaded from token.json')
            else:
                logger.warning('Credentials are invalid or expired.')

        # If credentials are not valid, request login
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
                logger.info('Access token refreshed.')
            else:
                if not os.path.exists('client_secret_blogger_desktop_client.json'):
                    logger.error('Client secret file not found.')
                    raise FileNotFoundError('client_secret_blogger_desktop_client.json not found.')
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    'client_secret_blogger_desktop_client.json', SCOPES)
                creds = flow.run_local_server(port=0)
                logger.info('OAuth 2.0 authentication completed.')

            # Save the credentials for future use
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
                logger.info('Credentials saved to token.json.')

    except Exception as e:
        logger.error(f"Error obtaining credentials: {e}")
        raise

    return creds


class BlogPost:
    """
    A class to handle Blogger post creation using pre-obtained credentials.
    
    Attributes:
        blog_id (str): The ID of the blog to publish posts to.
        title (str): The title of the blog post.
        content (str): The HTML content of the blog post.
        service (googleapiclient.discovery.Resource): API client for Blogger API.
    """

    def __init__(self, blog_id: str, title: str, content: str, creds: Credentials):
        """
        Initialize the BlogPost instance with the blog ID, title, content, and credentials.

        Args:
            blog_id (str): The ID of the blog.
            title (str): The title of the blog post.
            content (str): The HTML content of the blog post.
            creds (google.oauth2.credentials.Credentials): OAuth 2.0 credentials.
        """
        self.blog_id = blog_id
        self.title = title
        self.content = content
        self.service = build('blogger', 'v3', credentials=creds)

    def create_post(self) -> tuple:
        """
        Create and publish a new post in the Blogger blog.

        Uses the title and content defined in the instance to create the post.

        Returns:
            tuple: A tuple containing the ID and URL of the created post.
        
        Raises:
            HttpError: If an error occurs related to the Blogger API.
            Exception: Any other errors that occur during execution.
        """
        if not self.title.strip() or not self.content.strip():
            logger.error("Post title or content is empty.")
            raise ValueError("Title and content must not be empty.")

        try:
            post_body = {
                'kind': 'blogger#post',
                'title': self.title,
                'content': self.content,
            }

            post = self.service.posts().insert(blogId=self.blog_id, body=post_body).execute()
            logger.info(f"Post published successfully: {post['url']}")
            return post['id'], post['url']

        except HttpError as http_err:
            logger.error(f"HTTP error while publishing post: {http_err.resp.status} - {http_err.content}")
            raise
        except Exception as e:
            logger.error(f"Error while publishing post: {e}")
            raise
