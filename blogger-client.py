import os
import logging
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Configure logging
logging.basicConfig(
    filename='blogger_api.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# If you modify these SCOPES, delete the token.json file.
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
        # The token.json file stores the user's access and refresh tokens
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
            logging.info('Credentials loaded from token.json')

        # If there are no valid credentials, prompt the user to log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
                logging.info('Access token refreshed.')
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'client_secret_blogger_desktop_client.json', SCOPES)
                creds = flow.run_local_server(port=0)
                logging.info('OAuth 2.0 authentication completed.')

            # Save the credentials for future runs.
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
                logging.info('Credentials saved to token.json.')

    except Exception as e:
        logging.error(f"Error obtaining credentials: {e}")
        raise

    return creds

def create_blog_post(blog_id, title, content):
    """
    Create and publish a new post in a Blogger blog.

    Args:
        blog_id (str): The ID of the blog where the post will be published.
        title (str): The title of the post.
        content (str): The HTML content of the post.
    
    Returns:
        None
    
    Raises:
        HttpError: If an error occurs related to the Blogger API.
        Exception: Any other errors that occur during execution.
    """
    try:
        creds = get_credentials()
        service = build('blogger', 'v3', credentials=creds)
        post_body = {
            'kind': 'blogger#post',
            'title': title,
            'content': content,
        }

        post = service.posts().insert(blogId=blog_id, body=post_body).execute()
        logging.info(f"Post published successfully: {post['url']}")
        print(f"Post published: {post['url']}")

    except HttpError as http_err:
        logging.error(f"HTTP error while publishing post: {http_err}")
        print(f"HTTP error while publishing post: {http_err}")
    except Exception as e:
        logging.error(f"Error while publishing post: {e}")
        print(f"Error while publishing post: {e}")

if __name__ == "__main__":
    try:
        blog_id = '7624840374831160388'
        title = 'Título de ejemplo 5'
        content = '<p>Este es un post de prueba creado con la API de Blogger desde Python 5.</p>'
        
        create_blog_post(blog_id, title, content)
    except Exception as e:
        logging.critical(f"Critical error in main execution: {e}")
        print(f"Critical error: {e}")    