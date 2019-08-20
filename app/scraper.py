import praw
from app.models import Rapper, User, Post, import_post, check_enrolled_emails
from app import mail
from flask_mail import Message


def login():
    reddit = praw.Reddit(client_id='pjDPFK9daEi2xw',
      client_secret='6X4hy7J25X_6ggX_iz_aNzU1w9g',
      redirect_uri='http://localhost:8080',
      user_agent='hiphopupdater by /u/hiphopupdater')
    return reddit


def scrape():
    reddit = login()
    hiphopheads = reddit.subreddit('hiphopheads')
    rappers = Rapper.query.all()
    saved_posts = Post.query.with_entities(Post.post_id).all()

    for post in hiphopheads.hot(limit=20):
        # checks for duplicate posts
        if post.id not in saved_posts:
            for rapper in rappers:
                if rapper.name in post.title and 'FRESH' in post.title and check_enrolled_emails(rapper.id):
                    subscribed = User.query.filter(User.rapper_id == rapper.id)
                    send_email(subscribed, rapper.name, post.url)
            import_post(post.id)


def generate_subject(rapper_name):
    return "Fresh {} Awaits You".format(rapper_name)


def generate_html(rapper_name, post_url):
    html = """<body>
      <table style="font-size:18px; font-family:Times New Roman; text-align:center;">
        <tr>
          <td>
            <p>We know you have been waiting for it, and here it is.</p>
            <br>
            <p>FRESH {}</p>
            <p><a href='{}'>Check it Out on Reddit.</a></p>
            <br>
            <br>
            <p>Delivered to you by HipHopUpdater.</p>
          </td>
        </tr>
      </table>
    </body>""".format(rapper_name, post_url)
    return html


def send_email(subscribed, rapper_name, post_url):
    with mail.connect() as conn:
        for user in subscribed:
            subject = generate_subject(rapper_name)
            html = generate_html(rapper_name, post_url)
            msg = Message(recipients=[user.email],
              html=html, subject=subject)
            conn.send(msg)
