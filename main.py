import flask
import json
import io

app = flask.Flask(__name__)
app.posts = {}


@app.route('/', methods=['GET'])
def home():
    return app.posts


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


@app.route('/post/{post_id}', methods=['GET'])
def post(post_id):
    if not app.posts[post_id]['deleted']:
        return app.posts[post_id]
    else:
        page_not_found()


def load_posts():
    with open('post.json') as f:
        app.posts = json.load(f)
        app.posts['post_count'] = 0
        for post in app.posts['posts']:
            if not post['deleted']:
                post['comments'] = []
                post['comments_count'] = 0
                app.posts['post_count'] += 1
            else:
                app.posts['posts'].remove(post)
            with open('comments.json') as f:
                comments = json.load(f)['comments']
                for comment in comments:
                    if comment['post_id'] == post['id']:
                        post['comments'].append(comment)
                        post['comments_count'] += 1


if __name__ == '__main__':
    load_posts()
    app.run(port=8000, debug=True)
