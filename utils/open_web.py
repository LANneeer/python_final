import webbrowser
import plotly.graph_objects as go
import numpy as np

data = "some request"


def get_values(data):
    # separate top_words_strategy
    top_words_strategy = data.get("top_words_strategy", {})
    top_words_strategy_keys = list(top_words_strategy.keys())  # array for keys
    top_words_strategy_values = list(top_words_strategy.values())  # array for values

    # separate top_tweets_strategy
    top_tweets_strategy = data.get("top_tweets_strategy", {})

    # top_likes
    top_likes = []
    for tweet in top_tweets_strategy.get("top_likes", []):
        tweet_data = {
            "date": tweet.get("date", ""),
            "id": tweet.get("id", ""),
            "content": tweet.get("content", ""),
            "contains_top_words": tweet.get("contains_top_words", []),
            "username": tweet.get("username", ""),
            "like_count": tweet.get("like_count", ""),
            "retweet_count": tweet.get("retweet_count", "")
        }
        top_likes.append(tweet_data)

    # top_retweets
    top_retweets = []
    for tweet in top_tweets_strategy.get("top_retweets", []):
        tweet_data = {
            "date": tweet.get("date", ""),
            "id": tweet.get("id", ""),
            "content": tweet.get("content", ""),
            "contains_top_words": tweet.get("contains_top_words", []),
            "username": tweet.get("username", ""),
            "like_count": tweet.get("like_count", ""),
            "retweet_count": tweet.get("retweet_count", "")
        }
        top_retweets.append(tweet_data)

    # top_general
    top_general = []
    for tweet in top_tweets_strategy.get("top_general", []):
        tweet_data = {
            "date": tweet.get("date", ""),
            "id": tweet.get("id", ""),
            "content": tweet.get("content", ""),
            "contains_top_words": tweet.get("contains_top_words", []),
            "username": tweet.get("username", ""),
            "like_count": tweet.get("like_count", ""),
            "retweet_count": tweet.get("retweet_count", ""),
            "popularity": tweet.get("popularity", "")
        }
        top_general.append(tweet_data)

    # separate productive_authors_strategy
    productive_authors_strategy = []
    for author in data.get("productive_authors_strategy", []):
        author_data = {
            "username": author.get("username", ""),
            "post_count": author.get("post_count", "")
        }
        productive_authors_strategy.append(author_data)

    # separate tweets_timeline
    tweets_timeline = data.get("tweets_timeline", {})
    tweets_timeline_keys = list(tweets_timeline.keys())  # array for keys
    tweets_timeline_values = list(tweets_timeline.values())  # array for values

    # return all the separated arrays
    return (
        top_words_strategy_keys, top_words_strategy_values,
        top_likes, top_retweets, top_general, productive_authors_strategy,
        tweets_timeline, tweets_timeline_keys, tweets_timeline_values
    )


def extract_dates(top):
    return [tweet.get("date", "") for tweet in top]


def extract_ids(top):
    return [tweet.get("id", "") for tweet in top]


def extract_contents(top):
    return [tweet.get("content", "") for tweet in top]


def extract_contains_top_words(top):
    return [tweet.get("contains_top_words", []) for tweet in top]


def extract_usernames(top):
    return [tweet.get("username", "") for tweet in top]


def extract_like_counts(top):
    return [tweet.get("like_count", "") for tweet in top]


def extract_retweet_counts(top):
    return [tweet.get("retweet_count", "") for tweet in top]


(top_words_strategy_keys, top_words_strategy_values, top_likes, top_retweets, top_general,
 productive_authors_strategy, tweets_timeline, tweets_timeline_keys, tweets_timeline_values) = get_values(data)

# extract usernames and counts of authors
productive_authors_usernames = [author["username"] for author in data["productive_authors_strategy"]]
productive_authors_post_counts = [author["post_count"] for author in data["productive_authors_strategy"]]

# min and max counts of tweets in this period (max, min), mean count of tweets per week
min_count_tweets = np.min(tweets_timeline_values)
max_count_tweets = np.max(tweets_timeline_values)
mean_count_tweets = np.mean(tweets_timeline_values)

reverse_tweets_timeline = {v: k for k, v in tweets_timeline.items()}

min_count_week = reverse_tweets_timeline.get(min_count_tweets)
max_count_week = reverse_tweets_timeline.get(max_count_tweets)

import plotly.graph_objects as go


def create_table(output_file="marginal_and_average_values.html"):
    """create a table and save it as an HTML file"""

    data = [
        ['Highest number of posts per week', max_count_tweets, max_count_week],
        ['Lowest number of posts per week', min_count_tweets, min_count_week],
        ['Average number of posts per week', mean_count_tweets, 'All weeks']
    ]

    fig = go.Figure(go.Table(
        header=dict(values=['<b>Metric</b>', '<b>Value</b>', '<b>Time Period</b>'],
                    fill_color='#1da1f2',
                    align='center',
                    font=dict(color='white', size=14)),
        cells=dict(values=list(zip(*data)),
                   fill_color=[['#1da1f2', 'white', 'white']] * len(data),
                   align=['left', 'center', 'center'],
                   font=dict(color='black', size=12))
    ))

    fig.update_layout(
        title='Marginal and Average Values',
        title_x=0.5,
        title_font=dict(size=20, color='#1da1f2', family="Arial, sans-serif")
    )


# strings for HTML
pie_chart_labels = "["
for word in top_words_strategy_keys:
    pie_chart_labels += "'"
    pie_chart_labels += str(word)
    pie_chart_labels += "', "
pie_chart_labels = pie_chart_labels[0:-2]
pie_chart_labels += "]"

pie_chart_data = "["
for num in top_words_strategy_values:
    pie_chart_data += str(num)
    pie_chart_data += ", "
pie_chart_data = pie_chart_data[0:-2]
pie_chart_data += "]"

try:
    with open('index.html', 'w') as file:
        message = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="author" content="Zul'yarov Diyar, Ilik Temirlan, Mashina Veronika">
    <title>Python Final Project</title>
    <link rel="icon" type="image/png" href="static/img/logo.png">
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f5f8fa;
            margin: 0;
            padding: 0;
            color: #1da1f2;
        }

        header {
            background-color: #ffffff;
            padding: 15px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        header img {
            height: 50px;
        }

        header h1 {
            font-size: 24px;
            margin: 0;
            color: #1da1f2;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
            text-align: center;
        }

        main {
            max-width: 800px;
            margin: 20px auto;
            padding: 20px;
            background-color: #ffffff;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }

        main h2, main p {
            text-align: center;
        }

        main h3 {
            font-weight: 300;
            font-style: italic;
            text-decoration: underline;
            margin: 10px;
        }

        .chart-container {
            margin-top: 20px;
            max-width: 600px;
        }
        
        #first-user{
            font-size: 18px;
            font-weight: bold;
            color: #1da1f2;
            background-color: #f0f8ff;
            padding: 20px;
            border: 3px solid #FFD700;
            border-radius: 10px;
            box-shadow: 0px 0px 15px 5px rgba(255, 223, 0, 0.7);
            text-align: center;
            transition: all 0.3s ease;
        }

        #first-user:hover {
            box-shadow: 0px 0px 25px 10px rgba(255, 223, 0, 1);
        }

        footer {
            margin-top: 30px;
            text-align: center;
            font-size: 14px;
            color: #657786;
        }

        .creator-names {
            font-style: italic;
            margin-top: 10px;
        }

        canvas {
            max-width: 100%;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            margin-bottom: 20px;
        }

        .gold {
            background-color: #ffd700;
            font-weight: bold;
            text-shadow: 1px 1px 0 #000, -1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000;
        }

        .silver {
            background-color: #c0c0c0;
            font-weight: bold;
            text-shadow: 1px 1px 0 #000, -1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000;
        }

        .bronze {
            background-color: #cd7f32;
            font-weight: bold;
            text-shadow: 1px 1px 0 #000, -1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000;
        }

        th, td {
            padding: 10px;
            text-align: left;
            border: 1px solid #ddd;
        }
    </style>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
<header>
    <img src="static/img/uni-logo.jpg" alt="University Logo">
    <h1>ChatGPT-related tweets</h1>
</header>

<main>
    <h2>Python Final Project</h2>
    <p>Analyze and visualize data related to tweets about ChatGPT</p>

    <div class="chart-container">
        <h3>Top keywords of a tweet</h3>
        <canvas id="pieChart"></canvas>
    </div>

    <h3>Top popular tweets by likes and reposts</h3>
    <table>
        <thead>
        <tr style="background-color: #1da1f2; color: #ffffff;">
            <th>Date</th>
            <th>ID</th>
            <th>Content</th>
            <th>Top Words</th>
            <th>Username</th>
            <th>Like Count</th>
            <th>Retweet Count</th>
        </tr>
        </thead>
        <tbody>
        <tr class="gold">
            <td>2024-12-25</td>
            <td>001</td>
            <td>"ChatGPT is revolutionizing the way we think about AI!"</td>
            <td>ChatGPT, AI, revolutionizing</td>
            <td>@tech_guru</td>
            <td>1200</td>
            <td>500</td>
        </tr>
        <tr class="silver">
            <td>2024-12-24</td>
            <td>002</td>
            <td>"Can’t imagine my workflow without ChatGPT anymore!"</td>
            <td>workflow, ChatGPT, imagine</td>
            <td>@workflow_king</td>
            <td>950</td>
            <td>420</td>
        </tr>
        <tr class="bronze">
            <td>2024-12-23</td>
            <td>003</td>
            <td>"Is ChatGPT the future of education? Looks like it!"</td>
            <td>ChatGPT, future, education</td>
            <td>@edu_innovator</td>
            <td>870</td>
            <td>380</td>
        </tr>
        <tr>
            <td>2024-12-22</td>
            <td>004</td>
            <td>"ChatGPT is great for debugging code quickly!"</td>
            <td>ChatGPT, debugging, code</td>
            <td>@coder_pro</td>
            <td>600</td>
            <td>250</td>
        </tr>
        <tr>
            <td>2024-12-21</td>
            <td>005</td>
            <td>"Writing essays has never been easier, thanks to ChatGPT."</td>
            <td>essays, easier, ChatGPT</td>
            <td>@writer_tools</td>
            <td>580</td>
            <td>200</td>
        </tr>
        </tbody>
    </table>

    <div class="chart-container">
        <h3>Tweets</h3>
        <canvas id="lineGraph"></canvas>
    </div>

    <div class="chart-container">
        <h3>Top Users by AI Tweets</h3>
        <canvas id="barChart" width="400" height="200"></canvas>
        <script>
            const ctx = document.getElementById('barChart').getContext('2d');

            const salesData = [300, 400, 200, 393];

            const months = ['January', 'February', 'March', 'dckn'];

            const sortedSales = [...salesData].sort((a, b) => b - a);
            const colorMap = salesData.map(value => {
                if (value === sortedSales[0]) {
                    return 'rgba(255, 215, 0, 0.6)';
                } else if (value === sortedSales[1]) {
                    return 'rgba(192, 192, 192, 0.6)';
                } else if (value === sortedSales[2]) {
                    return 'rgba(205, 127, 50, 0.6)';
                } else {
                    return 'rgba(29, 161, 242, 0.2)';
                }
            });

            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: months,
                    datasets: [{
                        label: 'Sales',
                        data: salesData,
                        backgroundColor: colorMap,
                        borderColor: colorMap.map(color => color === 'rgba(255, 215, 0, 0.6)' || color === 'rgba(192, 192, 192, 0.6)' || color === 'rgba(205, 127, 50, 0.6)' ? '#000' : 'rgba(29, 161, 242, 0.2)'),
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });

        </script>
    </div>
    
    <div class="chart-container">
        <h3>The most popular user</h3>
        <p id="first-user">Text</p>
    </div>

</main>

<footer>
    <p>&copy; 2024 Python Final Project</p>
    <p class="creator-names">Creators: Zul'yarov Diyar, Ilik Temirlan, Mashina Veronika</p>
</footer>

<script>
    const pieCtx = document.getElementById('pieChart').getContext('2d');
    new Chart(pieCtx, {
        type: 'pie',
        data: {
            labels: {0},
            datasets: [{
                data: {1},
                backgroundColor: ['#1da1f2', '#657786', '#aab8c2']
            }]
        },
        options: {
            responsive: true
        }
    });

    const lineCtx = document.getElementById('lineGraph').getContext('2d');
    new Chart(lineCtx, {
        type: 'line',
        data: {
            labels: ['Point1', 'Point2', 'Point3'],
            datasets: [{
                label: 'Dataset 1',
                data: [5, 15, 25],
                borderColor: '#1da1f2',
                fill: false
            }]
        },
        options: {
            responsive: true
        }
    });
</script>
</body>
</html>
"""
        message = message.format(pie_chart_labels, pie_chart_data)
        file.write(message)

    filename = 'index.html'

    webbrowser.open_new_tab(filename)

except IOError as ior:
    print(f'IOError - {ior}')
else:
    print('File was opened without any problems')
finally:
    print('Work is over')
