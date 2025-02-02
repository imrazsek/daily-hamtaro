# daily-hamtaro 🐹

A Python application that automates downloading images from Reddit and posting them to Instagram.

## 🌟 Features

- Automatic image downloading from multiple subreddits
- Interface for discarding images
- Automated Instagram posting

## 📋 Prerequisites

- Python 3.8 or higher
- Instagram account
- Reddit API access

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/imrazsek/daily-hamtaro
cd daily-hamtaro
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## 🔧 Configuration

### Subreddit Configuration

Modify `subreddits.txt` file with the list of subreddits you want to fetch images from:
```
hamsters
hamtaro
cutepets
```

## 💻 Usage

1. Run the application:
```bash
python daily_hamtaro.py
```

2. The application will ask you for your Reddit data. If you don't know how to get them check the [page](https://www.reddit.com/prefs/apps/)

3. The application will download images from the configured subreddits

4. An interface will open where you can:
   - View downloaded images
   - Discard the ones you don't like

5. The application will ask you for your Instagram data

6. Once introduced, the application will automatically post to Instagram


## 📬 Contact

Cesar Montero - [@imrazsek](https://twitter.com/imrazsek)

Project Link: [https://github.com/imrazsek/daily-hamtaro](https://github.com/imrazsek/daily-hamtaro)
