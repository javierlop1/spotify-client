import os
import logging
from logging_config import setup_logging
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

setup_logging()  # Ensure the logger is set up

# Get a logger for this specific module
logger = logging.getLogger(__name__)

# SCOPES for Blogger API
SCOPES = ['https://www.googleapis.com/auth/blogger']

def get_credentials():
    """
    Obtain credentials for the Blogger API using OAuth 2.0.

    Loads the credentials from `token.json` if they exist. If not, it opens
    a browser window for the user to sign in and authorize the application.

    Returns:
        creds (google.oauth2.credentials.Credentials): OAuth 2.0 credentials.
    
    Raises:
        Exception: If any error occurs during the authentication process.
    """
    creds = None
    try:
        # Check if credentials are stored in token.json
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
            logging.info('Credentials loaded from token.json')

        # If credentials are not valid, request login
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
                logging.info('Access token refreshed.')
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'client_secret_blogger_desktop_client.json', SCOPES)
                creds = flow.run_local_server(port=0)
                logging.info('OAuth 2.0 authentication completed.')

            # Save the credentials for future use
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
                logging.info('Credentials saved to token.json.')

    except Exception as e:
        logging.error(f"Error obtaining credentials: {e}")
        raise

    return creds

class BlogPost:
    """
    A class to handle Blogger post creation using pre-obtained credentials.
    
    Attributes:
        blog_id (str): The ID of the blog to publish posts to.
        title (str): The title of the blog post.
        content (str): The HTML content of the blog post.
        creds (google.oauth2.credentials.Credentials): OAuth 2.0 credentials for API access.
    """

    def __init__(self, blog_id, title, content, creds):
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
        self.creds = creds

    def create_post(self):
        """
        Create and publish a new post in the Blogger blog.

        Uses the title and content defined in the instance to create the post.

        Returns:
            None
        
        Raises:
            HttpError: If an error occurs related to the Blogger API.
            Exception: Any other errors that occur during execution.
        """
        try:
            service = build('blogger', 'v3', credentials=self.creds)
            post_body = {
                'kind': 'blogger#post',
                'title': self.title,
                'content': self.content,
            }

            post = service.posts().insert(blogId=self.blog_id, body=post_body).execute()
            logging.info(f"Post published successfully: {post['url']}")

        except HttpError as http_err:
            logging.error(f"HTTP error while publishing post: {http_err}")
        except Exception as e:
            logging.error(f"Error while publishing post: {e}")

